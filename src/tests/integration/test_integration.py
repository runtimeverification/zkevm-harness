from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

import pytest
from pyk.utils import run_process_2

from .utils import TEST_DATA_DIR

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path
    from typing import Final

    from zkevm_harness.solc import Contract


TEMPLATE_DIR: Final = TEST_DATA_DIR / 'templates'
CONTRACT_DIR: Final = TEST_DATA_DIR / 'contracts'


class TemplateLoader:
    _path: Path

    def __init__(self, path: Path):
        self._path = path

    def __call__(
        self,
        *,
        template_name: str,
        context: dict[str, str],
    ) -> Path:
        from jinja2 import Environment, FileSystemLoader, StrictUndefined

        src_dir = TEMPLATE_DIR / template_name
        trg_dir = self._path / template_name

        template_files = [path.relative_to(src_dir) for path in src_dir.rglob('*') if path.is_file()]
        env = Environment(loader=FileSystemLoader(str(src_dir)), undefined=StrictUndefined)
        for file in template_files:
            template = env.get_template(str(file))
            rendered = template.render(context)
            out_file = trg_dir / file
            out_file.parent.mkdir(parents=True, exist_ok=True)
            out_file.write_text(rendered)

        return trg_dir


@pytest.fixture
def load_template(tmp_path: Path) -> TemplateLoader:
    return TemplateLoader(tmp_path)


def solc_compile(*, contract_file: str, contract_name: str) -> Contract:
    from zkevm_harness import solc

    return solc.compile(CONTRACT_DIR / contract_file, contract_name)


def gen_u8_array(bs: bytes) -> str:
    blen = len(bs)
    bstr = ', '.join(f'0x{b:02x}' for b in bs)
    return f'[u8; {blen}] = [{bstr}];'


class BuildConfig(NamedTuple):
    build_cmd: tuple[str, ...]
    zkvm_deps: str
    src_header: str
    elf_path: str


def dedent(text: str) -> str:
    import textwrap

    return textwrap.dedent(text).strip()


RISC0_CONFIG: Final = BuildConfig(
    build_cmd=('cargo', 'risczero', 'build'),
    zkvm_deps=dedent(
        """
        bytemuck_derive = "=1.8.1"
        risc0-zkvm = { version = "=2.0.1", default-features = false }
        """
    ),
    src_header=dedent(
        """
        #![no_main]
        #![no_std]
        #![feature(unsafe_attributes)]
        risc0_zkvm::guest::entry!(main);
        """
    ),
    elf_path='target/riscv32im-risc0-zkvm-elf/docker',
)

SP1_CONFIG: Final = BuildConfig(
    build_cmd=('cargo', 'prove', 'build'),
    zkvm_deps='sp1-zkvm = "=4.1.7"',
    src_header=dedent(
        """
        #![no_main]
        sp1_zkvm::entrypoint!(main);
        """
    ),
    elf_path='target/elf-compilation/riscv32im-succinct-zkvm-elf/release',
)


ADD_TEST_DATA: Final = (
    ('risc0', RISC0_CONFIG),
    ('sp1', SP1_CONFIG),
)


@pytest.mark.parametrize(
    'test_id,build_config',
    ADD_TEST_DATA,
    ids=[test_id for test_id, *_ in ADD_TEST_DATA],
)
def test_add(load_template: TemplateLoader, test_id: str, build_config: BuildConfig) -> None:
    # Given
    contract = solc_compile(contract_file='Add.sol', contract_name='Add')
    project_name = 'add-test'
    calldata = ('add', 1, 2)
    project_dir = load_template(
        template_name=project_name,
        context={
            'zkvm_deps': build_config.zkvm_deps,
            'src_header': build_config.src_header,
            'contract_bin_runtime': gen_u8_array(contract.bin_runtime),
            'contract_input': gen_u8_array(contract.calldata(*calldata)),
        },
    )
    run_process_2(build_config.build_cmd, cwd=project_dir)
    elf_file = project_dir / build_config.elf_path / project_name

    assert elf_file.is_file()
