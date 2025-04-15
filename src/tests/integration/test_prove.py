from __future__ import annotations

import itertools
from pathlib import Path
from typing import TYPE_CHECKING, Callable, Final, cast

import pytest
from kriscv.elf_parser import _memory_segments, entry_point, read_unique_symbol
from kriscv.term_builder import (
    dot_sb,
    halt_at_address,
    normalize_memory,
    regs,
    sb_bytes,
    sb_bytes_cons,
    sb_empty,
    sb_empty_cons,
    word,
)
from pyk.cterm import CSubst, CTerm, cterm_build_claim
from pyk.kast.inner import KApply, KInner, KSequence, KSort, KVariable, Subst
from pyk.prelude.bytes import bytesToken
from pyk.prelude.kint import eqInt, intToken
from pyk.prelude.ml import mlEqualsTrue
from pyk.proof.reachability import APRProof, APRProver
from pyk.proof.show import APRProofShow

from .utils import DEBUG_DIR, SP1_CONFIG, _elf_file, build_elf, get_symbols, resolve_symbol

if TYPE_CHECKING:
    from kriscv.symtools import SymTools
    from kriscv.tools import Tools

    from .utils import BuildConfig, TemplateLoader

PROVE_TEST_DATA: Final = (('add-test', 2, SP1_CONFIG),)


def length_bytes(var: str) -> KInner:
    # TODO: Move to riscv semantics
    return KApply('lengthBytes(_)_BYTES-HOOKED_Int_Bytes', [KVariable(var, 'Bytes')])


def add_bytes(bytes1: KInner, bytes2: KInner) -> KInner:
    # TODO: Move to riscv semantics
    return KApply('_+Bytes__BYTES-HOOKED_Bytes_Bytes_Bytes', bytes1, bytes2)


def sparse_symbolic_bytes(data: dict[int, bytes], symbolic_bytes: dict[int, tuple[int, str]]) -> KInner:
    # TODO: Move to riscv semantics; extract reusable parts into functions
    symbolic_bytes = dict(sorted(symbolic_bytes.items(), key=lambda item: item[0]))

    clean_data: list[tuple[int, bytes]] = sorted(normalize_memory(data).items())

    if len(clean_data) == 0:
        return dot_sb()

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

    sparse_k = dot_sb()
    for addr, gap_or_val in sparse_data:
        if isinstance(gap_or_val, int):
            for symaddr, symsize, symname in symbolic_bytes.items():
                if addr <= symaddr < addr + gap_or_val:
                    assert symaddr + symsize <= addr + gap_or_val
                    assert False, 'We do not support to make empty segments with partial symbolic bytes!'
            sparse_k = sb_empty_cons(sb_empty(intToken(gap_or_val)), sparse_k)
        elif isinstance(gap_or_val, bytes):
            curr_addr = addr
            curr_bytes = None
            for symaddr, symsize, symname in symbolic_bytes.items():
                if addr <= symaddr < addr + gap_or_val:
                    assert symaddr + symsize <= addr + gap_or_val
                    # Extract bytes before the variable
                    if symaddr > curr_addr:
                        temp_bytes = bytesToken(gap_or_val[curr_addr - addr : symaddr - addr])
                        curr_bytes = add_bytes(curr_bytes, temp_bytes) if curr_bytes else temp_bytes
                    # Add the variable
                    curr_bytes = (
                        add_bytes(curr_bytes, KVariable(symname, 'Bytes'))
                        if curr_bytes
                        else KVariable(symname, 'Bytes')
                    )
                    # Skip over the variable bytes
                    curr_addr = symaddr + symsize
            if curr_addr < addr + len(gap_or_val):
                temp_bytes = bytesToken(gap_or_val[curr_addr - addr :])
                curr_bytes = add_bytes(curr_bytes, temp_bytes) if curr_bytes else temp_bytes
            sparse_k = sb_bytes_cons(sb_bytes(curr_bytes), sparse_k)
        else:
            raise AssertionError()
    return sparse_k


def _init_config(
    symbolic_bytes: dict[int, tuple[int, str]], build_config: BuildConfig, elf_file: Path, kriscv: Tools
) -> CTerm:
    sparse_bytes = sparse_symbolic_bytes(_memory_segments(elf_file), symbolic_bytes)
    (end_symbol,) = get_symbols(elf_file, build_config.end_pattern)
    with _elf_file(elf_file) as elf:
        end_addr = read_unique_symbol(elf, end_symbol, error_loc=str(elf_file))
        halt_cond = halt_at_address(word(end_addr))
    config_vars = {
        '$REGS': regs(dict.fromkeys(range(32), 0)),
        '$MEM': sparse_bytes,
        '$PC': entry_point(elf_file),
        '$HALT': halt_cond,
    }

    constraints = [mlEqualsTrue(eqInt(length_bytes(var), intToken(size))) for size, var in symbolic_bytes.items()]
    return CTerm(kriscv.init_config(config_vars), constraints)


def _final_config(symtools: SymTools) -> CTerm:
    config = CTerm(symtools.kprove.definition.empty_config(KSort('GeneratedTopCell')))
    _final_subst = {vname: KVariable('FINAL_' + vname) for vname in config.free_vars}
    _final_subst['INSTRS_CELL'] = KSequence([KApply('#HALT_RISCV-TERMINATION_KItem'), KVariable('FINAL_INSTRS_CELL')])
    final_subst = CSubst(Subst(_final_subst))
    return final_subst(config)


@pytest.mark.parametrize(
    'test_id,arg_count,build_config',
    PROVE_TEST_DATA,
    ids=[test_id for test_id, *_ in PROVE_TEST_DATA],
)
def test_add(
    symtools: SymTools,
    tools: Callable[[str], Tools],
    load_template: TemplateLoader,
    test_id: str,
    arg_count: int,
    build_config: BuildConfig,
) -> None:
    # Given
    elf_file = build_elf(test_id, load_template, build_config)
    args = {resolve_symbol(elf_file, f'OP{i}'): (32, f'W{i}') for i in range(0, arg_count)}

    init_config = _init_config(args, build_config, elf_file, tools(build_config.target))
    kclaim = cterm_build_claim(test_id.upper(), init_config, _final_config(symtools))
    proof = APRProof.from_claim(symtools.kprove.definition, kclaim[0], {}, symtools.proof_dir)

    # When
    with symtools.explore(id='ADD') as kcfg_explore:
        prover = APRProver(
            kcfg_explore=kcfg_explore,
            execute_depth=1,
        )
        prover.advance_proof(proof, max_iterations=45)
        proof_show = APRProofShow(symtools.kprove)
        with open(DEBUG_DIR / 'proof-result.txt', 'w') as f:
            f.write('\n'.join(proof_show.show(proof, [node.id for node in proof.kcfg.nodes])))

    # Then ???
