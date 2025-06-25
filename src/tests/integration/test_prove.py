from __future__ import annotations

import shutil
from typing import TYPE_CHECKING, Final

import pytest
from kriscv.elf_parser import ELF
from pyk.kast.inner import KApply

from .utils import BINARY_DIR, RISC0_CONFIG, SP1_CONFIG, SPEC_DIR, filter_symbols

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

    from kriscv.symtools import APRProof, SymTools
    from kriscv.tools import Tools
    from pyk.kast.inner import KInner

    from .utils import BuildConfig, TemplateLoader


TEMPLATE_DATA: Final[tuple[tuple[str, str, dict[str, str], list[str]], ...]] = (
    ('stop-test', 'stop-test', {}, []),
    ('add-test', 'simple-2-op-test', {'opcode': '0x01'}, ['OP0', 'OP1']),
    ('mul-test', 'simple-2-op-test', {'opcode': '0x02'}, ['OP0', 'OP1']),
    ('sub-test', 'simple-2-op-test', {'opcode': '0x03'}, ['OP0', 'OP1']),
    ('div-test', 'simple-2-op-test', {'opcode': '0x04'}, ['OP0', 'OP1']),
    ('sdiv-test', 'simple-2-op-test', {'opcode': '0x05'}, ['OP0', 'OP1']),
    ('mod-test', 'simple-2-op-test', {'opcode': '0x06'}, ['OP0', 'OP1']),
    ('smod-test', 'simple-2-op-test', {'opcode': '0x07'}, ['OP0', 'OP1']),
    ('addmod-test', 'simple-3-op-test', {'opcode': '0x08'}, ['OP0', 'OP1', 'OP2']),
    ('mulmod-test', 'simple-3-op-test', {'opcode': '0x09'}, ['OP0', 'OP1', 'OP2']),
    ('exp-test', 'simple-2-op-test', {'opcode': '0x0a'}, ['OP0', 'OP1']),
    ('signextend-test', 'simple-2-op-test', {'opcode': '0x0b'}, ['OP0', 'OP1']),
    ('lt-test', 'simple-2-op-test', {'opcode': '0x10'}, ['OP0', 'OP1']),
    ('gt-test', 'simple-2-op-test', {'opcode': '0x11'}, ['OP0', 'OP1']),
    ('slt-test', 'simple-2-op-test', {'opcode': '0x12'}, ['OP0', 'OP1']),
    ('sgt-test', 'simple-2-op-test', {'opcode': '0x13'}, ['OP0', 'OP1']),
    ('eq-test', 'simple-2-op-test', {'opcode': '0x14'}, ['OP0', 'OP1']),
    ('iszero-test', 'simple-1-op-test', {'opcode': '0x15'}, ['OP0']),
    ('and-test', 'simple-2-op-test', {'opcode': '0x16'}, ['OP0', 'OP1']),
    ('or-test', 'simple-2-op-test', {'opcode': '0x17'}, ['OP0', 'OP1']),
    ('xor-test', 'simple-2-op-test', {'opcode': '0x18'}, ['OP0', 'OP1']),
    ('not-test', 'simple-1-op-test', {'opcode': '0x19'}, ['OP0']),
    ('byte-test', 'simple-2-op-test', {'opcode': '0x1a'}, ['OP0', 'OP1']),
    ('shl-test', 'simple-2-op-test', {'opcode': '0x1b'}, ['OP0', 'OP1']),
    ('shr-test', 'simple-2-op-test', {'opcode': '0x1c'}, ['OP0', 'OP1']),
    ('sar-test', 'simple-2-op-test', {'opcode': '0x1d'}, ['OP0', 'OP1']),
    ('keccak256-test', 'simple-2-op-test', {'opcode': '0x20'}, ['OP0', 'OP1']),
    ('address-test', 'address-test', {}, ['VALUE']),
    # 0x31 BALANCE - Skip: no real implementation in DummyHost
    ('origin-test', 'host-property-address-test', {'opcode': '0x30', 'property': 'env.tx.caller'}, ['VALUE']),
    ('caller-test', 'caller-test', {}, ['VALUE']),
    ('callvalue-test', 'callvalue-test', {}, ['VALUE']),
    ('calldataload-test', 'calldataload-test', {}, ['DATA', 'DATA_SIZE', 'LOAD_INDEX', 'INDEX']),
    ('calldatasize-test', 'calldatasize-test', {}, ['DATA', 'DATA_SIZE']),
    (
        'calldatacopy-test',
        'calldatacopy-test',
        {},
        ['DATA', 'DATA_SIZE', 'DEST_OFFSET', 'COPY_OFFSET', 'COPY_SIZE', 'INDEX'],
    ),
    # 0x38 CODESIZE
    # 0x39 CODECOPY
    ('gasprice-test', 'host-property-u256-test', {'opcode': '0x3a', 'property': 'env.tx.gas_price'}, ['VALUE']),
    # 0x3b EXTCODESIZE - Skip: no real implementation in DummyHost
    # 0x3c EXTCODECOPY - Skip: no real implementation in DummyHost
    ('returndatasize-test', 'returndatasize-test', {}, ['DATA', 'DATA_SIZE']),
    (
        'returndatacopy-test',
        'returndatacopy-test',
        {},
        ['DATA', 'DATA_SIZE', 'DEST_OFFSET', 'COPY_OFFSET', 'COPY_SIZE', 'INDEX'],
    ),
    # 0x3f EXTCODEHASH - Skip: no real implementation in DummyHost
    # 0x40 BLOCKHASH - Skip: no real implementation in DummyHost
    ('coinbase-test', 'host-property-address-test', {'opcode': '0x41', 'property': 'env.block.coinbase'}, ['VALUE']),
    ('timestamp-test', 'host-property-u256-test', {'opcode': '0x42', 'property': 'env.block.timestamp'}, ['VALUE']),
    ('number-test', 'host-property-u256-test', {'opcode': '0x43', 'property': 'env.block.number'}, ['VALUE']),
    ('prevrandao-test', 'prevrandao-test', {}, ['VALUE']),
    ('gaslimit-test', 'host-property-u256-test', {'opcode': '0x45', 'property': 'env.block.gas_limit'}, ['VALUE']),
    ('chainid-test', 'chainid-test', {}, ['VALUE']),
    # 0x47 SELFBALANCE - Skip: no real implementation in DummyHost
    ('basefee-test', 'host-property-u256-test', {'opcode': '0x48', 'property': 'env.block.basefee'}, ['VALUE']),
    ('blobhash-test', 'blobhash-test', {}, ['INDEX', 'VALUE']),
    ('blobbasefee-test', 'blobbasefee-test', {}, ['VALUE']),
    ('pop-test', 'pop-test', {}, ['VALUE']),
    ('mload-test', 'mload-test', {}, ['OFFSET', 'VALUE']),
    ('mload-concrete-offset-test', 'mload-test', {}, ['VALUE']),
    ('mstore-test', 'mstore-test', {}, ['OFFSET', 'VALUE']),
    ('mstore-concrete-offset-test', 'mstore-test', {}, ['VALUE']),
    ('mstore8-test', 'mstore8-test', {}, ['OFFSET', 'VALUE']),
    ('sload-test', 'sload-test', {}, ['KEY', 'VALUE']),
    ('sstore-test', 'sstore-test', {}, ['KEY', 'VALUE']),
    # 0x56 JUMP
    # 0x57 JUMPI
    # 0x58 PC
    # 0x59 MSIZE
    # 0x5a GAS
    # 0x5b JUMPDEST
    ('tload-test', 'tload-test', {}, ['KEY', 'VALUE']),
    ('tstore-test', 'tstore-test', {}, ['KEY', 'VALUE']),
    # 0x5e MCOPY
    ('push0-test', 'push-test', {'opcode': '0x5f', 'arity': '0', 'value': '[]'}, []),
    ('push1-test', 'push-test', {'opcode': '0x60', 'arity': '1', 'value': '[0x01]'}, ['OP0']),
    ('push2-test', 'push-test', {'opcode': '0x61', 'arity': '2', 'value': '[0x00, 0x01]'}, ['OP0']),
    ('push3-test', 'push-test', {'opcode': '0x62', 'arity': '3', 'value': '[0x00, 0x00, 0x01]'}, ['OP0']),
    ('dup1-test', 'dup-test', {'opcode': '0x80', 'n': '1'}, ['OP0']),
    ('dup2-test', 'dup-test', {'opcode': '0x81', 'n': '2'}, ['OP0']),
    ('dup3-test', 'dup-test', {'opcode': '0x82', 'n': '3'}, ['OP0']),
    ('dup4-test', 'dup-test', {'opcode': '0x83', 'n': '4'}, ['OP0']),
    ('swap1-test', 'swap-test', {'opcode': '0x90', 'n': '1'}, ['OP0', 'OP1']),
    ('swap2-test', 'swap-test', {'opcode': '0x91', 'n': '2'}, ['OP0', 'OP1']),
    ('swap3-test', 'swap-test', {'opcode': '0x92', 'n': '3'}, ['OP0', 'OP1']),
    ('swap4-test', 'swap-test', {'opcode': '0x93', 'n': '4'}, ['OP0', 'OP1']),
    # 0xa0 LOG0
    # 0xa1 LOG1
    # 0xa2 LOG2
    # 0xa3 LOG3
    # 0xa4 LOG4
    # 0xf0 CREATE
    # 0xf1 CALL
    # 0xf2 CALLCODE
    # 0xf3 RETURN
    # 0xf4 DELEGATECALL
    # 0xf5 CREATE2
    # 0xfa STATICCALL
    # 0xfd REVERT
    # 0xfe INVALID
    # 0xff SELFDESTRUCT
)

GEN_CLAIM_TEST_DATA: Final = tuple(
    (f'{test_id}-sp1', SP1_CONFIG, project_name, context, symbolic_names)
    for test_id, project_name, context, symbolic_names in TEMPLATE_DATA
)


@pytest.mark.skip
@pytest.mark.parametrize(
    'test_id,build_config,project_name,context,symbolic_names',
    GEN_CLAIM_TEST_DATA,
    ids=[test_id for test_id, *_ in GEN_CLAIM_TEST_DATA],
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
    binary_file = BINARY_DIR / test_id
    elf_file = build_elf(project_name, load_template, build_config, context=context)

    # When
    shutil.copy2(elf_file, binary_file)

    # And given
    symtool = symtools(f'{build_config.target}-haskell', f'{build_config.target}-lib')
    spec_file = SPEC_DIR / f'{test_id}.k'
    claim_label = f'{test_id.upper()}.{test_id}'
    elf = ELF.load(binary_file)
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
    assert ClaimLoader(symtool.kprove).load_claims(
        spec_file=spec_file,
        claim_labels=[claim_label],
    )


BIN_FILES: Final = tuple(BINARY_DIR.glob('*'))


@pytest.mark.parametrize('bin_file', BIN_FILES, ids=[bin_file.name for bin_file in BIN_FILES])
def test_concrete(
    bin_file: Path,
    build_config_for_binary: Callable[[Path], BuildConfig],
    tools: Callable[[str], Tools],
) -> None:
    from pyk.cterm import CTerm
    from pyk.kast.inner import KApply, KSequence

    # Given
    build_config = build_config_for_binary(bin_file)
    elf = ELF.load(bin_file)
    (end_symbol,) = filter_symbols(elf, build_config.end_pattern)
    kriscv = tools(build_config.target)
    init_config = kriscv.config_from_elf(
        elf,
        regs=dict.fromkeys(range(32), 0),
        end_symbol=end_symbol,
    )

    # When
    final_config = kriscv.run_config(init_config)
    final_cterm = CTerm(final_config)

    # Then
    assert final_cterm.cell('INSTRS_CELL') == KSequence(KApply('#HALT'), KApply('#EXECUTE'))


@pytest.fixture
def build_config_for_binary(
    tools: Callable[[str], Tools],
) -> Callable[[Path], BuildConfig]:
    def result(bin_file: Path) -> BuildConfig:
        toolchain = bin_file.name.split('-')[-1]
        match toolchain:
            case 'risc0':
                return RISC0_CONFIG
            case 'sp1':
                return SP1_CONFIG
            case _:
                raise AssertionError()

    return result


MAX_DEPTH: Final = 100
MAX_ITERATIONS: Final = 4000

SPEC_FILES: Final = tuple(SPEC_DIR.glob('*.k'))


@pytest.mark.parametrize('spec_file', SPEC_FILES, ids=[spec_file.name for spec_file in SPEC_FILES])
def test_symbolic(
    spec_file: Path,
    symtools_for_spec: Callable[[Path], SymTools],
) -> None:
    if spec_file.name != 'stop-test-sp1.k':
        pytest.skip(reason='Work in progress')

    # Given
    symtools = symtools_for_spec(spec_file)

    # When
    proof = symtools.prove(
        spec_file=spec_file,
        spec_module=spec_file.stem.upper(),
        claim_id=spec_file.stem,
        max_depth=MAX_DEPTH,
        max_iterations=MAX_ITERATIONS,
        optimize_kcfg=True,
    )

    # Then
    # Prove `R(S_{REVM}.initial, S_{KEVM}.initial) /\ R(S_{REVM}.final, S_{KEVM}.final)`
    # `R` is the relation between KEVM state `S_{KEVM}` and REVM State in RISC-V memory `S_{REVM}`
    generate_report(proof, symtools, spec_file)


@pytest.fixture
def symtools_for_spec(
    symtools: Callable[[str, str], SymTools],
) -> Callable[[Path], SymTools]:
    def result(spec_file: Path) -> SymTools:
        toolchain = spec_file.stem.split('-')[-1]
        assert toolchain in ['risc0', 'sp1']
        return symtools(f'zkevm-semantics.{toolchain}-haskell', f'zkevm-semantics.{toolchain}-lib')

    return result


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


def generate_report(proof: APRProof, symtools: SymTools, spec_file: Path) -> None:
    from kriscv.utils import kast_print

    report: list[str] = []

    for node in proof.kcfg.nodes:
        # forall cterm, there is no `Int2Bytes` in their `regs` cells
        regs = node.cterm.cell('REGS_CELL')
        int2bytes_list = collect_int2bytes(regs)
        for int2bytes in int2bytes_list:
            report.append(
                f'{node.id} has `Int2Bytes` in their `regs` cells: {kast_print(int2bytes, kprint=symtools.kprove)}'
            )

    report.extend(symtools.proof_show.show(proof, [node.id for node in proof.kcfg.nodes]))

    (symtools.proof_dir / f'{spec_file.name.upper()}-proof-result.txt').write_text('\n'.join(report))
