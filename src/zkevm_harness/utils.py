from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable
    from pathlib import Path

    from kriscv.elf_parser import ELF
    from kriscv.tools import Tools
    from pyk.kast.outer import KClaim


def halt_claim_from_elf(
    tools: Tools,
    *,
    elf: str | Path | ELF,
    label: str,
    end_symbol: str | None = None,
    symbolic_names: Iterable[str] | None = None,
) -> KClaim:
    from pyk.cterm import CTerm, cterm_build_claim
    from pyk.kast.inner import KApply, KSequence, KSort, Subst

    init_config = tools.config_from_elf(
        elf,
        regs=dict.fromkeys(range(32), 0),
        end_symbol=end_symbol,
        symbolic_names=symbolic_names,
    )

    empty_config = tools.kprint.definition.empty_config(KSort('GeneratedTopCell'))
    final_config = Subst(
        {'INSTRS_CELL': KSequence(KApply('#HALT'), KApply('#EXECUTE'))},
    )(empty_config)

    init_cterm = CTerm.from_kast(init_config)
    final_cterm = CTerm.from_kast(final_config)

    claim, _ = cterm_build_claim(label, init_cterm, final_cterm)
    return claim


def spec_module_text(tools: Tools, *, module_name: str, claim: KClaim) -> str:
    from pyk.kast.manip import remove_generated_cells
    from pyk.kast.outer import KFlatModule, KImport

    claim = claim.let(body=remove_generated_cells(claim.body))
    module = KFlatModule(module_name, sentences=(claim,), imports=(KImport('RISCV'),))
    pretty = tools.kprint.pretty_print(module)
    return pretty
