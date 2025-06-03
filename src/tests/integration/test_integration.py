from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from .utils import RISC0_CONFIG, SP1_CONFIG, build_elf, filter_symbols, get_symbol_value

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Final

    from kriscv.tools import Tools

    from .utils import BuildConfig, TemplateLoader


CONCRETE_TEST_DATA: Final[tuple[tuple[str, str, BuildConfig, dict[str, str], bytes], ...]] = (
    ('risc0-add', 'simple-2-op-test', RISC0_CONFIG, {'opcode': '0x01'}, b'\x00' * 31 + b'\x03'),
    ('sp1-add', 'simple-2-op-test', SP1_CONFIG, {'opcode': '0x01'}, b'\x00' * 31 + b'\x03'),
    ('risc0-sstore', 'sstore-test', RISC0_CONFIG, {}, b'\x00' * 28 + b'\xde\xad\xbe\xef'),
    ('sp1-sstore', 'sstore-test', SP1_CONFIG, {}, b'\x00' * 28 + b'\xde\xad\xbe\xef'),
)


@pytest.mark.parametrize(
    'test_id,project_name,build_config,context,expected',
    CONCRETE_TEST_DATA,
    ids=[test_id for test_id, *_ in CONCRETE_TEST_DATA],
)
def test_concrete(
    tools: Callable[[str], Tools],
    load_template: TemplateLoader,
    test_id: str,
    project_name: str,
    build_config: BuildConfig,
    context: dict[str, str],
    expected: bytes,
) -> None:
    # Given
    elf = build_elf(project_name, load_template, build_config, context=context)
    result = elf.unique_symbol('RESULT')
    (end_symbol,) = filter_symbols(elf, build_config.end_pattern)
    kriscv = tools(build_config.target)
    init_config = kriscv.config_from_elf(
        elf,
        regs=dict.fromkeys(range(32), 0),
        end_symbol=end_symbol,
    )

    # When
    final_config = kriscv.run_config(init_config)
    actual = get_symbol_value(kriscv, final_config, result)

    # Then
    assert expected == actual
