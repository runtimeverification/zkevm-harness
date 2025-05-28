from __future__ import annotations

from typing import TYPE_CHECKING, Final

import pytest
from pyk.cterm import CSubst, CTerm, cterm_build_claim
from pyk.kast.inner import KApply, KSequence, KSort, KVariable, Subst
from pyk.kast.manip import remove_generated_cells
from pyk.proof.reachability import APRProof, APRProver
from pyk.proof.show import APRProofShow

from .utils import SP1_CONFIG, build_elf, get_symbols

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable
    from pathlib import Path

    from kriscv.symtools import SymTools
    from kriscv.tools import Tools
    from pyk.kast.inner import KInner

    from .utils import BuildConfig, TemplateLoader


def _init_config(symbolic_names: Iterable[str], build_config: BuildConfig, elf_file: Path, kriscv: Tools) -> CTerm:
    # TODO: Currently, we are constructing the start state of the riscv machine by using the elf file.
    #       We might need to:
    # 1. use the `kriscv` to concrete execute the elf file until it halts.
    # 2. extract the riscv memory and made it symbolic according to the `symdata`.
    # 3. set a new halt condition
    # 4. continue the symbolic execution until the new halt condition is reached.

    (end_symbol,) = get_symbols(elf_file, build_config.end_pattern)
    init_config = kriscv.config_from_elf(elf_file, end_symbol=end_symbol, symbolic_names=symbolic_names)
    return CTerm.from_kast(remove_generated_cells(init_config))


def _final_config(symtools: SymTools) -> CTerm:
    config = CTerm(symtools.kprove.definition.empty_config(KSort('GeneratedTopCell')))
    _final_subst: dict[str, KInner] = {vname: KVariable('FINAL_' + vname) for vname in config.free_vars}
    _final_subst['INSTRS_CELL'] = KSequence([KApply('#HALT_RISCV-TERMINATION_KItem'), KVariable('FINAL_INSTRS_CELL')])
    final_subst = CSubst(Subst(_final_subst))
    return final_subst(config)


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
    symtool = symtools(f'{build_config.target}-haskell', f'{build_config.target}-lib', 'zkevm-semantics.source')
    if APRProof.proof_data_exists(test_id.upper(), symtool.proof_dir):
        proof = APRProof.read_proof_data(proof_dir=symtool.proof_dir, id=test_id.upper())
    else:
        elf_file = build_elf(test_id, load_template, build_config)
        init_config = _init_config(
            [f'W{i}' for i in range(arg_count)], build_config, elf_file, tools(build_config.target)
        )
        kclaim = cterm_build_claim(test_id.upper(), init_config, _final_config(symtool))
        proof = APRProof.from_claim(symtool.kprove.definition, kclaim[0], {}, symtool.proof_dir)

    # When
    with symtool.explore(id=test_id.upper()) as kcfg_explore:
        prover = APRProver(
            kcfg_explore=kcfg_explore,
            execute_depth=DEPTH,
        )
        prover.advance_proof(proof, max_iterations=MAX_ITERATIONS)

    proof_show = APRProofShow(symtool.kprove.definition)
    show_result = '\n'.join(proof_show.show(proof, [node.id for node in proof.kcfg.nodes]))
    (symtool.proof_dir / f'{test_id.upper()}-proof-result.txt').write_text(show_result)

    # Then: Prove `R(S_{REVM}.initial, S_{KEVM}.initial) /\ R(S_{REVM}.final, S_{KEVM}.final)`
    # `R` is the relation between KEVM state `S_{KEVM}` and REVM State in RISC-V memory `S_{REVM}`
