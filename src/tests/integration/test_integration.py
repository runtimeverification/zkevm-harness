from __future__ import annotations

from contextlib import contextmanager
from typing import TYPE_CHECKING, NamedTuple, cast

import pytest
from kriscv.tools import Tools, elf_parser, term_builder, ELFFile
from kriscv.symtools import SymTools
from pyk.utils import run_process_2
import itertools
from pyk.prelude.bytes import bytesToken
from pyk.prelude.kint import intToken, eqInt
from pyk.prelude.ml import mlEqualsTrue
from pyk.cterm import CTerm, CSubst, cterm_build_claim
from pyk.kast.inner import KApply, KVariable, KSort, Subst, KSequence
from pyk.proof import APRProof, APRProver
from pyk.utils import ensure_dir_path
from .utils import TEST_DATA_DIR

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator
    from pathlib import Path
    from typing import Final

    from elftools.elf.elffile import ELFFile  # type: ignore

    from zkevm_harness.solc import Contract


TEMPLATE_DIR: Final = TEST_DATA_DIR / 'templates'
CONTRACT_DIR: Final = TEST_DATA_DIR / 'contracts'


class TemplateLoader:
    """
    A class for loading templates and rendering them with context.

    Attributes:
        _path: The path to the directory containing the templates.
    """

    def __init__(self, path: Path):
        self._path = path

    def __call__(
        self,
        *,
        template_name: str,
        context: dict[str, str],
    ) -> Path:
        from jinja2 import Environment, FileSystemLoader, StrictUndefined

        src_dir = TEMPLATE_DIR / template_name
        trg_dir = self._path / template_name
        try_dir = TEST_DATA_DIR / 'try'

        template_files = [path.relative_to(src_dir) for path in src_dir.rglob('*') if path.is_file()]
        env = Environment(loader=FileSystemLoader(str(src_dir)), undefined=StrictUndefined)
        for file in template_files:
            template = env.get_template(str(file))
            rendered = template.render(context)
            out_file = trg_dir / file
            try_file = try_dir / file
            out_file.parent.mkdir(parents=True, exist_ok=True)
            try_file.parent.mkdir(parents=True, exist_ok=True)
            out_file.write_text(rendered)
            try_file.write_text(rendered)

        return trg_dir


@pytest.fixture
def load_template(tmp_path: Path) -> TemplateLoader:
    return TemplateLoader(tmp_path)


@pytest.fixture
def tools(tmp_path: Path) -> Callable[[str], Tools]:
    def _tools(target: str) -> Tools:
        from pyk.kdist import kdist

        definition_dir = kdist.get(target)

        temp_dir = tmp_path / 'kriscv'
        temp_dir.mkdir()
        return Tools(definition_dir, temp_dir=temp_dir)

    return _tools

@pytest.fixture
def sym_tools() -> SymTools:
    tmp_path = TEST_DATA_DIR / 'sym'
    tmp_path.mkdir(parents=True, exist_ok=True)
    return SymTools.default(proof_dir=tmp_path)

def solc_compile(*, contract_file: str, contract_name: str) -> Contract:
    from zkevm_harness import solc

    return solc.compile(CONTRACT_DIR / contract_file, contract_name)


def gen_u8_array(bs: bytes) -> str:
    blen = len(bs)
    bstr = ', '.join(f'0x{b:02x}' for b in bs)
    return f'[u8; {blen}] = [{bstr}];'


class BuildConfig(NamedTuple):
    build_cmd: tuple[str, ...]
    zkvm_deps: str
    src_header: str
    elf_path: str
    end_pattern: str
    target: str


def dedent(text: str) -> str:
    import textwrap

    return textwrap.dedent(text).strip()


RISC0_CONFIG: Final = BuildConfig(
    build_cmd=('cargo', 'risczero', 'build'),
    zkvm_deps=dedent(
        """
        bytemuck_derive = "=1.8.1"
        risc0-zkvm = { version = "=2.0.1", default-features = false }
        """
    ),
    src_header=dedent(
        """
        #![no_main]
        #![no_std]
        #![feature(unsafe_attributes)]
        risc0_zkvm::guest::entry!(main);
        """
    ),
    elf_path='target/riscv32im-risc0-zkvm-elf/docker',
    end_pattern='sys_halt',
    target='zkevm-semantics.risc0',
)

SP1_CONFIG: Final = BuildConfig(
    build_cmd=('cargo', 'prove', 'build'),
    zkvm_deps='sp1-zkvm = "=4.1.7"',
    src_header=dedent(
        """
        #![no_main]
        sp1_zkvm::entrypoint!(main);
        """
    ),
    elf_path='target/elf-compilation/riscv32im-succinct-zkvm-elf/release',
    end_pattern='_ZN8sp1_zkvm8syscalls4halt12syscall_halt*',
    target='zkevm-semantics.sp1',
)


ADD_TEST_DATA: Final = (
    ('risc0', RISC0_CONFIG),
    ('sp1', SP1_CONFIG),
)


@pytest.mark.parametrize(
    'test_id,build_config',
    ADD_TEST_DATA,
    ids=[test_id for test_id, *_ in ADD_TEST_DATA],
)
def test_add(
    tools: Callable[[str], Tools],
    sym_tools: SymTools,
    load_template: TemplateLoader,
    test_id: str,
    build_config: BuildConfig,
) -> None:
    # Given
    contract = solc_compile(contract_file='Add.sol', contract_name='Add')
    project_name = 'add-test'
    calldata = ('add', 1, 2)
    project_dir = load_template(
        template_name=project_name,
        context={
            'zkvm_deps': build_config.zkvm_deps,
            'src_header': build_config.src_header,
            'contract_bin_runtime': gen_u8_array(contract.bin_runtime),
            'contract_input': gen_u8_array(contract.calldata(*calldata)),
        },
    )

    # When
    run_process_2(build_config.build_cmd, cwd=project_dir)
    elf_file = project_dir / build_config.elf_path / project_name

    # Then
    assert elf_file.is_file()

    # And given
    input_addr = resolve_symbol(elf_file, 'INPUT')
    symvars = {'W0': (input_addr + 4, 32), 'W1': (input_addr + 4 + 32, 32)}
    # Sort symvars by address (first element of the tuple)
    symvars = dict(sorted(symvars.items(), key=lambda item: item[1][0]))
    result_addr = resolve_symbol(elf_file, 'RESULT')
    (end_symbol,) = get_symbols(elf_file, build_config.end_pattern)
    print(f'end_symbol: {end_symbol}')
    kriscv = tools(build_config.target)
    
    regs = dict.fromkeys(range(32), 0)
    
    with open(elf_file, 'rb') as f:
        elf = ELFFile(f)
        if end_symbol is not None:
            end_addr = elf_parser.read_unique_symbol(elf, end_symbol, error_loc=str(elf_file))
            halt_cond = term_builder.halt_at_address(term_builder.word(end_addr))
        else:
            halt_cond = term_builder.halt_never()
        config_vars = {
            '$REGS': term_builder.regs(regs or {}),
            '$MEM': elf_parser.memory(elf),
            '$PC': elf_parser.entry_point(elf),
            '$HALT': halt_cond,
        }
        memseg = elf_parser._memory_segments(elf)
    
    clean_data: list[tuple[int, bytes]] = sorted(term_builder.normalize_memory(memseg).items())

    if len(clean_data) == 0:
        return term_builder.dot_sb()

    # Collect all empty gaps between segements
    gaps = []
    start = clean_data[0][0]
    if start != 0:
        gaps.append((0, start))
    for (start1, val1), (start2, _) in itertools.pairwise(clean_data):
        end1 = start1 + len(val1)
        # normalize_memory should already have merged consecutive segments
        assert end1 < start2
        gaps.append((end1, start2 - end1))

    # Merge segments and gaps into a list of sparse bytes items
    sparse_data: list[tuple[int, int | bytes]] = sorted(
        cast('list[tuple[int, int | bytes]]', clean_data) + cast('list[tuple[int, int | bytes]]', gaps), reverse=True
    )

    sparse_k = term_builder.dot_sb()
    for addr, gap_or_val in sparse_data:
        if isinstance(gap_or_val, int):
            for varname, (varaddr, varsize) in symvars.items():
                if addr <= varaddr < addr + gap_or_val:
                    assert varaddr + varsize <= addr + gap_or_val
                    print(f'{varname} in empty gap')
            sparse_k = term_builder.sb_empty_cons(term_builder.sb_empty(intToken(gap_or_val)), sparse_k)
        elif isinstance(gap_or_val, bytes):
            todo_addr = addr
            curr_bytes = None
            for varname, (varaddr, varsize) in symvars.items():
                if addr <= varaddr < addr + len(gap_or_val):
                    assert varaddr + varsize <= addr + len(gap_or_val)
                    # Extract bytes before the variable
                    if varaddr > todo_addr:
                        tmp_bytes = bytesToken(gap_or_val[todo_addr - addr:varaddr - addr])
                        curr_bytes = tmp_bytes if curr_bytes is None else KApply('_+Bytes__BYTES-HOOKED_Bytes_Bytes_Bytes', curr_bytes, tmp_bytes)
                    
                    curr_bytes = KVariable(varname, 'Bytes') if curr_bytes is None else KApply('_+Bytes__BYTES-HOOKED_Bytes_Bytes_Bytes', curr_bytes, KVariable(varname, 'Bytes'))
                    
                    # Skip over the variable bytes
                    todo_addr = varaddr + varsize
                    
            if todo_addr < addr + len(gap_or_val):
                tmp_bytes = bytesToken(gap_or_val[todo_addr - addr:])
                curr_bytes = tmp_bytes if curr_bytes is None else KApply('_+Bytes__BYTES-HOOKED_Bytes_Bytes_Bytes', curr_bytes, tmp_bytes)
            sparse_k = term_builder.sb_bytes_cons(term_builder.sb_bytes(curr_bytes), sparse_k)
        else:
            raise AssertionError()
        
    config = kriscv.init_config(config_vars)
    config_vars['$MEM'] = sparse_k
    sym_init_config = kriscv.init_config(config_vars)
    constraints = []
    for varname, (varaddr, varsize) in symvars.items():
        constraints.append( mlEqualsTrue(eqInt(KApply('lengthBytes(_)_BYTES-HOOKED_Int_Bytes', [KVariable(varname, 'Bytes')]), intToken(varsize))) )
    init_cterm = CTerm(sym_init_config, constraints)
    sym_final_config = CTerm(sym_tools.kprove.definition.empty_config(KSort('GeneratedTopCell')))
    _final_subst = {vname: KVariable('FINAL_' + vname) for vname in sym_final_config.free_vars}
    _final_subst['INSTRS_CELL'] = KSequence([KApply('#HALT_RISCV-TERMINATION_KItem'), KVariable('FINAL_INSTRS_CELL')])
    final_subst = CSubst(Subst(_final_subst))
    final_cterm = final_subst(sym_final_config)
    kclaim = cterm_build_claim('ADD', init_cterm, final_cterm)
    proof = APRProof.from_claim(sym_tools.kprove.definition, kclaim[0], {}, sym_tools.proof_dir)
    with sym_tools.explore(id='ADD') as kcfg_explore:
        prover = APRProver(
            kcfg_explore=kcfg_explore,
            execute_depth=1,
        )
        prover.advance_proof(proof, max_iterations=49)
    
    # When
    config = kriscv.run_elf(
        elf_file,
        regs=dict.fromkeys(range(32), 0),
        end_symbol=end_symbol,
    )

    # Then
    memory = kriscv.get_memory(config)
    assert kriscv.get_memory(config)[result_addr + 31] == 3


def resolve_symbol(elf_file: Path, symbol: str) -> int:
    from kriscv.elf_parser import read_unique_symbol

    with _elf_file(file=elf_file) as elf:
        return read_unique_symbol(elf, symbol, error_loc=None)


def get_symbols(elf_file: Path, pattern: str) -> list[str]:
    import fnmatch

    with _elf_file(file=elf_file) as elf:
        symtab = elf.get_section_by_name('.symtab')
        assert symtab

        func_symbols = [
            sym.name
            for sym in symtab.iter_symbols()
            if sym['st_info']['type'] == 'STT_FUNC'  # Check if symbol type is FUNC
        ]

        return fnmatch.filter(func_symbols, pattern)


@contextmanager
def _elf_file(file: Path) -> Iterator[ELFFile]:
    from elftools.elf.elffile import ELFFile  # type: ignore

    with file.open('rb') as f:
        elf = ELFFile(f)
        yield elf
