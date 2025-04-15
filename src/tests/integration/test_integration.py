from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from pyk.utils import run_process_2

from .utils import RISC0_CONFIG, SP1_CONFIG, get_symbols, resolve_symbol

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
    project_name = 'add-test'
    project_dir = load_template(
        template_name=project_name,
        context={
            'zkvm_deps': build_config.zkvm_deps,
            'src_header': build_config.src_header,
        },
    )

    # When
    run_process_2(build_config.build_cmd, cwd=project_dir)
    elf_file = project_dir / build_config.elf_path / project_name

    # Then
    assert elf_file.is_file()

    # And given
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
    assert kriscv.get_memory(config)[result_addr + 31] == 3
