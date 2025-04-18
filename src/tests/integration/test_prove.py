from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Final

import kriscv.term_builder as tb
import pytest
from kriscv.elf_parser import _memory_segments, entry_point, read_unique_symbol
from pyk.cterm import CSubst, CTerm, cterm_build_claim
from pyk.kast.inner import KApply, KSequence, KSort, KVariable, Subst
from pyk.proof.reachability import APRProof, APRProver
from pyk.proof.show import APRProofShow

from .utils import DEBUG_DIR, SP1_CONFIG, _elf_file, build_elf, get_symbols, resolve_symbol

if TYPE_CHECKING:
    from pathlib import Path

    from kriscv.symtools import SymTools
    from kriscv.tools import Tools
    from pyk.kast.inner import KInner

    from .utils import BuildConfig, TemplateLoader


def _init_config(
    symdata: dict[int, tuple[int, str]], build_config: BuildConfig, elf_file: Path, kriscv: Tools
) -> CTerm:
    # TODO: Currently, we are constructing the start state of the riscv machine by using the elf file.
    #       We might need to:
    # 1. use the `kriscv` to concrete execute the elf file until it halts.
    # 2. extract the riscv memory and made it symbolic according to the `symdata`.
    # 3. set a new halt condition
    # 4. continue the symbolic execution until the new halt condition is reached.

    data = _memory_segments(elf_file)
    sparse_bytes = tb.sparse_bytes(data, symdata)
    (end_symbol,) = get_symbols(elf_file, build_config.end_pattern)
    with _elf_file(elf_file) as elf:
        end_addr = read_unique_symbol(elf, end_symbol, error_loc=str(elf_file))
        halt_cond = tb.halt_at_address(tb.word(end_addr))
    config_vars = {
        '$REGS': tb.regs(dict.fromkeys(range(32), 0)),
        '$MEM': sparse_bytes,
        '$PC': entry_point(elf_file),
        '$HALT': halt_cond,
    }
    return CTerm(kriscv.init_config(config_vars), tb.sparse_bytes_constraints(symdata))


def _final_config(symtools: SymTools) -> CTerm:
    config = CTerm(symtools.kprove.definition.empty_config(KSort('GeneratedTopCell')))
    _final_subst: dict[str, KInner] = {vname: KVariable('FINAL_' + vname) for vname in config.free_vars}
    _final_subst['INSTRS_CELL'] = KSequence([KApply('#HALT_RISCV-TERMINATION_KItem'), KVariable('FINAL_INSTRS_CELL')])
    final_subst = CSubst(Subst(_final_subst))
    return final_subst(config)


PROVE_TEST_DATA: Final = (('add-test', 2, SP1_CONFIG),)
DEPTH: Final = 1
MAX_ITERATIONS: Final = 45


@pytest.mark.parametrize(
    'test_id,arg_count,build_config',
    PROVE_TEST_DATA,
    ids=[test_id for test_id, *_ in PROVE_TEST_DATA],
)
def test_prove_equivalence(
    symtools: SymTools,
    tools: Callable[[str], Tools],
    load_template: TemplateLoader,
    test_id: str,
    arg_count: int,
    build_config: BuildConfig,
) -> None:
    # Given
    elf_file = build_elf(test_id, load_template, build_config)
    symdata = {resolve_symbol(elf_file, f'OP{i}'): (32, f'W{i}') for i in range(0, arg_count)}

    init_config = _init_config(symdata, build_config, elf_file, tools(build_config.target))
    kclaim = cterm_build_claim(test_id.upper(), init_config, _final_config(symtools))
    proof = APRProof.from_claim(symtools.kprove.definition, kclaim[0], {}, symtools.proof_dir)

    # When
    with symtools.explore(id='ADD') as kcfg_explore:
        prover = APRProver(
            kcfg_explore=kcfg_explore,
            execute_depth=DEPTH,
        )
        prover.advance_proof(proof, max_iterations=MAX_ITERATIONS)
        proof_show = APRProofShow(symtools.kprove)
        with open(DEBUG_DIR / 'proof-result.txt', 'w') as f:
            f.write('\n'.join(proof_show.show(proof, [node.id for node in proof.kcfg.nodes])))

    # Then
    # Given the `REVM` in the riscv memory as `S_{REVM}`, and the `KEVM` state as `S_{KEVM}`
    # Define a relation `R(S_{REVM}, S_{KEVM})`
    # Prove that `R(S_{REVM}, S_{KEVM})` is valid for their initial state and final state.
    # That is `R(S_{REVM}.initial, S_{KEVM}.initial) /\ R(S_{REVM}.final, S_{KEVM}.final)` refinement verification through forward simulation.
