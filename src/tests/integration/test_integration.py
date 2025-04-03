from __future__ import annotations

from contextlib import contextmanager
from typing import TYPE_CHECKING, NamedTuple

import pytest
from kriscv.tools import Tools
from pyk.utils import run_process_2

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

        template_files = [path.relative_to(src_dir) for path in src_dir.rglob('*') if path.is_file()]
        env = Environment(loader=FileSystemLoader(str(src_dir)), undefined=StrictUndefined)
        for file in template_files:
            template = env.get_template(str(file))
            rendered = template.render(context)
            out_file = trg_dir / file
            out_file.parent.mkdir(parents=True, exist_ok=True)
            out_file.write_text(rendered)

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
    result_addr = resolve_symbol(elf_file, 'RESULT')
    (end_symbol,) = get_symbols(elf_file, build_config.end_pattern)
    print(f'end_symbol: {end_symbol}')
    kriscv = tools(build_config.target)

    # When
    config = kriscv.run_elf(
        elf_file,
        regs=dict.fromkeys(range(32), 0),
        end_symbol=end_symbol,
    )

    # Then
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
