from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from .utils import RISC0_CONFIG, SP1_CONFIG, build_elf, get_memory, get_symbols, resolve_symbol

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Final

    from kriscv.tools import Tools

    from .utils import BuildConfig, TemplateLoader


CONCRETE_TEST_DATA: Final = (
    ('risc0-add', 'add-test', RISC0_CONFIG, b'\x00' * 31 + b'\x03'),
    ('sp1-add', 'add-test', SP1_CONFIG, b'\x00' * 31 + b'\x03'),
    ('risc0-sstore', 'sstore-test', RISC0_CONFIG, b'\x00' * 28 + b'\xde\xad\xbe\xef'),
    ('sp1-sstore', 'sstore-test', SP1_CONFIG, b'\x00' * 28 + b'\xde\xad\xbe\xef'),
)


@pytest.mark.parametrize(
    'test_id,project_name,build_config,expected',
    CONCRETE_TEST_DATA,
    ids=[test_id for test_id, *_ in CONCRETE_TEST_DATA],
)
def test_concrete(
    tools: Callable[[str], Tools],
    load_template: TemplateLoader,
    test_id: str,
    project_name: str,
    build_config: BuildConfig,
    expected: bytes,
) -> None:
    # Given
    elf_file = build_elf(project_name, load_template, build_config)
    result_addr = resolve_symbol(elf_file, 'RESULT')
    (end_symbol,) = get_symbols(elf_file, build_config.end_pattern)
    kriscv = tools(build_config.target)

    # When
    config = kriscv.run_elf(
        elf_file,
        regs=dict.fromkeys(range(32), 0),
        end_symbol=end_symbol,
    )
    actual = get_memory(kriscv, config, result_addr, 32)

    # Then
    assert expected == actual
