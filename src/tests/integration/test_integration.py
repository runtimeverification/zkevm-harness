from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from kriscv.elf_parser import ELF

from .utils import RISC0_CONFIG, SP1_CONFIG, build_elf, filter_symbols

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Final

    from kriscv.tools import Tools

    from .utils import BuildConfig, TemplateLoader


CONCRETE_TEST_DATA: Final[tuple[tuple[str, str, BuildConfig, dict[str, str]], ...]] = (
    ('risc0-add', 'simple-2-op-test', RISC0_CONFIG, {'opcode': '0x01'}),
    ('sp1-add', 'simple-2-op-test', SP1_CONFIG, {'opcode': '0x01'}),
    ('risc0-sstore', 'sstore-test', RISC0_CONFIG, {}),
    ('sp1-sstore', 'sstore-test', SP1_CONFIG, {}),
)


@pytest.mark.parametrize(
    'test_id,project_name,build_config,context',
    CONCRETE_TEST_DATA,
    ids=[test_id for test_id, *_ in CONCRETE_TEST_DATA],
)
def test_build_and_interpret(
    tools: Callable[[str], Tools],
    load_template: TemplateLoader,
    test_id: str,
    project_name: str,
    build_config: BuildConfig,
    context: dict[str, str],
) -> None:
    from pyk.cterm import CTerm
    from pyk.kast.inner import KApply, KSequence

    # Given
    elf_file = build_elf(project_name, load_template, build_config, context=context)
    elf = ELF.load(elf_file)
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
