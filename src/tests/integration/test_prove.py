from __future__ import annotations

from typing import TYPE_CHECKING, Final

import pytest

from .utils import SP1_CONFIG, SPEC_DIR

if TYPE_CHECKING:
    from collections.abc import Callable

    from kriscv.symtools import SymTools
    from kriscv.tools import Tools

    from .utils import BuildConfig, TemplateLoader


MAX_DEPTH: Final = 1000
MAX_ITERATIONS: Final = 45


GEN_TEST_DATA: Final = (('add-test-sp1', SP1_CONFIG, 'add-test', ['OP0', 'OP1']),)
PROVE_TEST_DATA: Final = tuple((test_id, build_config) for test_id, build_config, *_ in GEN_TEST_DATA)


@pytest.mark.skip
@pytest.mark.parametrize(
    'test_id,build_config,project_name,symbolic_names',
    GEN_TEST_DATA,
    ids=[test_id for test_id, *_ in GEN_TEST_DATA],
)
def test_generate_claim(
    tools: Callable[[str], Tools],
    load_template: TemplateLoader,
    # ---
    test_id: str,
    build_config: BuildConfig,
    project_name: str,
    symbolic_names: list[str],
) -> None:
    from zkevm_harness.utils import halt_claim_from_elf, spec_module_text

    from .utils import build_elf, filter_symbols

    tool = tools(build_config.target)
    spec_file = SPEC_DIR / f'{test_id}.k'

    elf = build_elf(project_name, load_template, build_config)
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

    spec_file.write_text(module_text)


@pytest.mark.parametrize(
    'test_id,build_config',
    PROVE_TEST_DATA,
    ids=[test_id for test_id, *_ in PROVE_TEST_DATA],
)
def test_prove_equivalence(
    symtools: Callable[[str, str, str], SymTools],
    # ---
    test_id: str,
    build_config: BuildConfig,
) -> None:
    if test_id in ['add-test-sp1']:
        pytest.skip('Work in progress')

    # Given
    symtool = symtools(f'{build_config.target}-haskell', f'{build_config.target}-lib', 'zkevm-semantics.source')

    spec_file = SPEC_DIR / f'{test_id}.k'
    spec_module_name = test_id.upper()
    claim_id = f'{spec_module_name}.{test_id}'

    # When
    proof = symtool.prove(
        spec_file=spec_file,
        spec_module=spec_module_name,
        claim_id=claim_id,
        max_depth=MAX_DEPTH,
        max_iterations=MAX_ITERATIONS,
    )

    proof_show = symtool.proof_show
    show_result = '\n'.join(proof_show.show(proof, [node.id for node in proof.kcfg.nodes]))
    (symtool.proof_dir / f'{test_id.upper()}-proof-result.txt').write_text(show_result)

    # Then: Prove `R(S_{REVM}.initial, S_{KEVM}.initial) /\ R(S_{REVM}.final, S_{KEVM}.final)`
    # `R` is the relation between KEVM state `S_{KEVM}` and REVM State in RISC-V memory `S_{REVM}`
