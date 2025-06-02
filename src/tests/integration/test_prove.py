from __future__ import annotations

from typing import TYPE_CHECKING, Final

import pytest
from pyk.proof.reachability import APRProof, APRProver

from zkevm_harness.utils import halt_claim_from_elf

from .utils import SP1_CONFIG, build_elf, filter_symbols

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

    from kriscv.symtools import SymTools
    from kriscv.tools import Tools

    from .utils import BuildConfig, TemplateLoader


PROVE_TEST_DATA: Final = (('add-test', 2, SP1_CONFIG),)
DEPTH: Final = 1000
MAX_ITERATIONS: Final = 45


@pytest.mark.parametrize(
    'test_id,arg_count,build_config',
    PROVE_TEST_DATA,
    ids=[test_id for test_id, *_ in PROVE_TEST_DATA],
)
def test_prove_equivalence(
    custom_temp_dir: Path,
    symtools: Callable[[str, str, str], SymTools],
    tools: Callable[[str], Tools],
    load_template: TemplateLoader,
    test_id: str,
    arg_count: int,
    build_config: BuildConfig,
) -> None:
    if test_id in ['add-test']:
        pytest.skip(f'Skipping {test_id} because we are still working on it')

    # Given
    tool = tools(build_config.target)
    symtool = symtools(f'{build_config.target}-haskell', f'{build_config.target}-lib', 'zkevm-semantics.source')
    if APRProof.proof_data_exists(test_id.upper(), symtool.proof_dir):
        proof = APRProof.read_proof_data(proof_dir=symtool.proof_dir, id=test_id.upper())
    else:
        elf = build_elf(test_id, load_template, build_config)
        (end_symbol,) = filter_symbols(elf, build_config.end_pattern)
        kclaim = halt_claim_from_elf(
            tools=tool,
            elf=elf,
            label=test_id.upper(),
            end_symbol=end_symbol,
            symbolic_names=[f'OP{i}' for i in range(arg_count)],
        )
        proof = APRProof.from_claim(symtool.kprove.definition, kclaim, {}, symtool.proof_dir)

    # When
    with symtool.explore(id=test_id.upper()) as kcfg_explore:
        prover = APRProver(
            kcfg_explore=kcfg_explore,
            execute_depth=DEPTH,
        )
        prover.advance_proof(proof, max_iterations=MAX_ITERATIONS)

    proof_show = symtool.proof_show
    show_result = '\n'.join(proof_show.show(proof, [node.id for node in proof.kcfg.nodes]))
    (symtool.proof_dir / f'{test_id.upper()}-proof-result.txt').write_text(show_result)

    # Then: Prove `R(S_{REVM}.initial, S_{KEVM}.initial) /\ R(S_{REVM}.final, S_{KEVM}.final)`
    # `R` is the relation between KEVM state `S_{KEVM}` and REVM State in RISC-V memory `S_{REVM}`
