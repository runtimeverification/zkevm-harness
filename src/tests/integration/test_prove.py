from __future__ import annotations

from typing import TYPE_CHECKING, Final

import pytest
from pyk.kast.inner import KApply

from .utils import SP1_CONFIG, SPEC_DIR

if TYPE_CHECKING:
    from collections.abc import Callable

    from kriscv.symtools import APRProof, SymTools
    from kriscv.tools import Tools
    from pyk.kast.inner import KInner

    from .utils import BuildConfig, TemplateLoader


MAX_DEPTH: Final = 1000
MAX_ITERATIONS: Final = 1


GEN_TEST_DATA: Final[tuple[tuple[str, BuildConfig, str, dict[str, str], list[str]], ...]] = (
    ('stop-test-sp1', SP1_CONFIG, 'stop-test', {}, []),
    ('add-test-sp1', SP1_CONFIG, 'simple-2-op-test', {'opcode': '0x01'}, ['OP0', 'OP1']),
    ('mul-test-sp1', SP1_CONFIG, 'simple-2-op-test', {'opcode': '0x02'}, ['OP0', 'OP1']),
    ('sub-test-sp1', SP1_CONFIG, 'simple-2-op-test', {'opcode': '0x03'}, ['OP0', 'OP1']),
    ('div-test-sp1', SP1_CONFIG, 'simple-2-op-test', {'opcode': '0x04'}, ['OP0', 'OP1']),
    ('sdiv-test-sp1', SP1_CONFIG, 'simple-2-op-test', {'opcode': '0x05'}, ['OP0', 'OP1']),
    ('mod-test-sp1', SP1_CONFIG, 'simple-2-op-test', {'opcode': '0x06'}, ['OP0', 'OP1']),
    ('smod-test-sp1', SP1_CONFIG, 'simple-2-op-test', {'opcode': '0x07'}, ['OP0', 'OP1']),
    ('addmod-test-sp1', SP1_CONFIG, 'simple-3-op-test', {'opcode': '0x08'}, ['OP0', 'OP1', 'OP2']),
    ('mulmod-test-sp1', SP1_CONFIG, 'simple-3-op-test', {'opcode': '0x09'}, ['OP0', 'OP1', 'OP2']),
    ('exp-test-sp1', SP1_CONFIG, 'simple-2-op-test', {'opcode': '0x0a'}, ['OP0', 'OP1']),
    ('signextend-test-sp1', SP1_CONFIG, 'simple-2-op-test', {'opcode': '0x0b'}, ['OP0', 'OP1']),
    ('lt-test-sp1', SP1_CONFIG, 'simple-2-op-test', {'opcode': '0x10'}, ['OP0', 'OP1']),
    ('gt-test-sp1', SP1_CONFIG, 'simple-2-op-test', {'opcode': '0x11'}, ['OP0', 'OP1']),
    ('slt-test-sp1', SP1_CONFIG, 'simple-2-op-test', {'opcode': '0x12'}, ['OP0', 'OP1']),
    ('sgt-test-sp1', SP1_CONFIG, 'simple-2-op-test', {'opcode': '0x13'}, ['OP0', 'OP1']),
    ('eq-test-sp1', SP1_CONFIG, 'simple-2-op-test', {'opcode': '0x14'}, ['OP0', 'OP1']),
    ('iszero-test-sp1', SP1_CONFIG, 'simple-1-op-test', {'opcode': '0x15'}, ['OP0']),
    ('and-test-sp1', SP1_CONFIG, 'simple-2-op-test', {'opcode': '0x16'}, ['OP0', 'OP1']),
    ('or-test-sp1', SP1_CONFIG, 'simple-2-op-test', {'opcode': '0x17'}, ['OP0', 'OP1']),
    ('xor-test-sp1', SP1_CONFIG, 'simple-2-op-test', {'opcode': '0x18'}, ['OP0', 'OP1']),
    ('not-test-sp1', SP1_CONFIG, 'simple-1-op-test', {'opcode': '0x19'}, ['OP0']),
    ('byte-test-sp1', SP1_CONFIG, 'simple-2-op-test', {'opcode': '0x1a'}, ['OP0', 'OP1']),
    ('shl-test-sp1', SP1_CONFIG, 'simple-2-op-test', {'opcode': '0x1b'}, ['OP0', 'OP1']),
    ('shr-test-sp1', SP1_CONFIG, 'simple-2-op-test', {'opcode': '0x1c'}, ['OP0', 'OP1']),
    ('sar-test-sp1', SP1_CONFIG, 'simple-2-op-test', {'opcode': '0x1d'}, ['OP0', 'OP1']),
    ('keccak256-test-sp1', SP1_CONFIG, 'simple-2-op-test', {'opcode': '0x20'}, ['OP0', 'OP1']),
    # ...
    ('mload-test-sp1', SP1_CONFIG, 'mload-test', {}, ['OFFSET', 'VALUE']),
    ('mstore-test-sp1', SP1_CONFIG, 'mstore-test', {}, ['OFFSET', 'VALUE']),
    ('mstore8-test-sp1', SP1_CONFIG, 'mstore8-test', {}, ['OFFSET', 'VALUE']),
    ('sload-test-sp1', SP1_CONFIG, 'sload-test', {}, ['KEY', 'VALUE']),
    ('sstore-test-sp1', SP1_CONFIG, 'sstore-test', {}, ['KEY', 'VALUE']),
    # ...
    ('tload-test-sp1', SP1_CONFIG, 'tload-test', {}, ['KEY', 'VALUE']),
    ('tstore-test-sp1', SP1_CONFIG, 'tstore-test', {}, ['KEY', 'VALUE']),
    # 0x5e MCOPY
    ('push0-test-sp1', SP1_CONFIG, 'push-test', {'opcode': '0x5f', 'arity': '0', 'value': '[]'}, []),
    ('push1-test-sp1', SP1_CONFIG, 'push-test', {'opcode': '0x60', 'arity': '1', 'value': '[0x01]'}, ['OP0']),
    ('push2-test-sp1', SP1_CONFIG, 'push-test', {'opcode': '0x61', 'arity': '2', 'value': '[0x00, 0x01]'}, ['OP0']),
    (
        'push3-test-sp1',
        SP1_CONFIG,
        'push-test',
        {'opcode': '0x62', 'arity': '3', 'value': '[0x00, 0x00, 0x01]'},
        ['OP0'],
    ),
    ('dup1-test-sp1', SP1_CONFIG, 'dup-test', {'opcode': '0x80', 'n': '1'}, ['OP0']),
    ('dup2-test-sp1', SP1_CONFIG, 'dup-test', {'opcode': '0x81', 'n': '2'}, ['OP0']),
    ('dup3-test-sp1', SP1_CONFIG, 'dup-test', {'opcode': '0x82', 'n': '3'}, ['OP0']),
    ('dup4-test-sp1', SP1_CONFIG, 'dup-test', {'opcode': '0x83', 'n': '4'}, ['OP0']),
    ('swap1-test-sp1', SP1_CONFIG, 'swap-test', {'opcode': '0x90', 'n': '1'}, ['OP0', 'OP1']),
    ('swap2-test-sp1', SP1_CONFIG, 'swap-test', {'opcode': '0x91', 'n': '2'}, ['OP0', 'OP1']),
    ('swap3-test-sp1', SP1_CONFIG, 'swap-test', {'opcode': '0x92', 'n': '3'}, ['OP0', 'OP1']),
    ('swap4-test-sp1', SP1_CONFIG, 'swap-test', {'opcode': '0x93', 'n': '4'}, ['OP0', 'OP1']),
)
PROVE_TEST_DATA: Final = tuple((test_id, build_config) for test_id, build_config, *_ in GEN_TEST_DATA)


@pytest.mark.skip
@pytest.mark.parametrize(
    'test_id,build_config,project_name,context,symbolic_names',
    GEN_TEST_DATA,
    ids=[test_id for test_id, *_ in GEN_TEST_DATA],
)
def test_generate_claim(
    tools: Callable[[str], Tools],
    symtools: Callable[[str, str], SymTools],
    load_template: TemplateLoader,
    # ---
    test_id: str,
    build_config: BuildConfig,
    project_name: str,
    context: dict[str, str],
    symbolic_names: list[str],
) -> None:
    from pyk.ktool.claim_loader import ClaimLoader

    from zkevm_harness.utils import halt_claim_from_elf, spec_module_text

    from .utils import build_elf, filter_symbols

    # Given
    tool = tools(build_config.target)
    spec_file = SPEC_DIR / f'{test_id}.k'

    elf = build_elf(project_name, load_template, build_config, context=context)
    (end_symbol,) = filter_symbols(elf, build_config.end_pattern)
    claim = halt_claim_from_elf(
        tools=tool,
        elf=elf,
        label=test_id,
        end_symbol=end_symbol,
        symbolic_names=symbolic_names,
    )
    module_text = spec_module_text(
        tools=tool,
        module_name=test_id.upper(),
        claim=claim,
    ).strip()

    # When
    spec_file.write_text(module_text)

    # Then
    symtool = symtools(f'{build_config.target}-haskell', f'{build_config.target}-lib')
    claim_label = f'{test_id.upper()}.{test_id}'
    assert ClaimLoader(symtool.kprove).load_claims(
        spec_file=spec_file,
        claim_labels=[claim_label],
    )


@pytest.mark.parametrize(
    'test_id,build_config',
    PROVE_TEST_DATA,
    ids=[test_id for test_id, *_ in PROVE_TEST_DATA],
)
def test_prove_equivalence(
    symtools: Callable[[str, str], SymTools],
    # ---
    test_id: str,
    build_config: BuildConfig,
) -> None:
    if test_id != 'stop-test-sp1':
        pytest.skip(reason='Work in progress')

    # Given
    symtool = symtools(f'{build_config.target}-haskell', f'{build_config.target}-lib')

    # When
    proof = symtool.prove(
        spec_file=SPEC_DIR / f'{test_id}.k',
        spec_module=test_id.upper(),
        claim_id=test_id,
        max_depth=MAX_DEPTH,
        max_iterations=MAX_ITERATIONS,
    )

    # Then: Prove `R(S_{REVM}.initial, S_{KEVM}.initial) /\ R(S_{REVM}.final, S_{KEVM}.final)`
    # `R` is the relation between KEVM state `S_{KEVM}` and REVM State in RISC-V memory `S_{REVM}`
    report = check_proof(proof, symtool)
    report += '\n'.join(symtool.proof_show.show(proof, [node.id for node in proof.kcfg.nodes]))
    (symtool.proof_dir / f'{test_id.upper()}-proof-report.txt').write_text(report)


def collect_int2bytes(term: KInner) -> list[KInner]:
    """Collect all `Int2Bytes` in the term."""
    from pyk.kast.inner import KLabel, collect

    int2bytes_list: list[KInner] = []

    def _collect_int2bytes(kinner: KInner) -> None:
        match kinner:
            case KApply(KLabel('Int2Bytes(_,_,_)_BYTES-HOOKED_Bytes_Int_Int_Endianness')):
                int2bytes_list.append(kinner)

    collect(_collect_int2bytes, term)
    return int2bytes_list


def check_proof(proof: APRProof, symtool: SymTools) -> str:
    from kriscv.utils import kast_print

    report: list[str] = []

    for node in proof.kcfg.nodes:
        # forall cterm, there is no `Int2Bytes` in their `regs` cells
        regs = node.cterm.cell('REGS_CELL')
        int2bytes_list = collect_int2bytes(regs)
        for int2bytes in int2bytes_list:
            report.append(
                f'{node.id} has `Int2Bytes` in their `regs` cells: {kast_print(int2bytes, kprint=symtool.kprove)}'
            )

    return '\n'.join(report)
