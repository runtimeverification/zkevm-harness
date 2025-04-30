from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from .utils import RISC0_CONFIG, SP1_CONFIG, build_elf, get_memory, get_symbols, resolve_symbol

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Final

    from kriscv.tools import Tools

    from .utils import BuildConfig, TemplateLoader


ADD_TEST_DATA: Final = (
    ('risc0', RISC0_CONFIG),
    ('sp1', SP1_CONFIG),
)


@pytest.mark.parametrize(
    'test_id,build_config',
    ADD_TEST_DATA,
    ids=[test_id for test_id, *_ in ADD_TEST_DATA],
)
def test_add(
    tools: Callable[[str], Tools],
    load_template: TemplateLoader,
    test_id: str,
    build_config: BuildConfig,
) -> None:
    # Given
    elf_file = build_elf('add-test', load_template, build_config)
    result_addr = resolve_symbol(elf_file, 'RESULT')
    (end_symbol,) = get_symbols(elf_file, build_config.end_pattern)
    kriscv = tools(build_config.target)

    # When
    config = kriscv.run_elf(
        elf_file,
        regs=dict.fromkeys(range(32), 0),
        end_symbol=end_symbol,
    )

    # Then
    assert get_memory(kriscv, config, result_addr, 32) == b'\x00' * 31 + b'\x03'


@pytest.mark.parametrize(
    'test_id,build_config',
    ADD_TEST_DATA,
    ids=[test_id for test_id, *_ in ADD_TEST_DATA],
)
def test_sstore(
    tools: Callable[[str], Tools],
    load_template: TemplateLoader,
    test_id: str,
    build_config: BuildConfig,
) -> None:
    # Given
    elf_file = build_elf('sstore-test', load_template, build_config)
    result_addr = resolve_symbol(elf_file, 'RESULT')
    (end_symbol,) = get_symbols(elf_file, build_config.end_pattern)
    kriscv = tools(build_config.target)

    # When
    config = kriscv.run_elf(
        elf_file,
        regs=dict.fromkeys(range(32), 0),
        end_symbol=end_symbol,
    )

    # Then
    assert get_memory(kriscv, config, result_addr, 32) == b'\x00' * 28 + b'\xde\xad\xbe\xef'
