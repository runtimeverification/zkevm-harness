from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, NamedTuple

from pyk.utils import run_process_2

if TYPE_CHECKING:
    from typing import Final

    from kriscv.elf_parser import ELF, Symbol
    from kriscv.tools import Tools
    from pyk.kast import KInner


TEST_DATA_DIR: Final = (Path(__file__).parent / 'test-data').resolve(strict=True)
DEPS_DIR: Final = (Path(__file__).parents[3] / 'deps').resolve(strict=True)
TEMPLATE_DIR: Final = TEST_DATA_DIR / 'templates'
SPEC_DIR: Final = TEST_DATA_DIR / 'specs'

RISC0_VERSION: Final = (DEPS_DIR / 'risc0_release').read_text().rstrip()
SP1_VERSION: Final = (DEPS_DIR / 'sp1_release').read_text().rstrip()


class TemplateLoader:
    """
    A class for loading templates and rendering them with context.

    Attributes:
        _path: The path to the directory containing the templates.
    """

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


class BuildConfig(NamedTuple):
    build_cmd: tuple[str, ...]
    zkvm_deps: str
    src_header: str
    elf_path: str
    end_pattern: str
    target: str


def dedent(text: str) -> str:
    import textwrap

    return textwrap.dedent(text).strip()


RISC0_CONFIG: Final = BuildConfig(
    build_cmd=('cargo', 'risczero', 'build'),
    zkvm_deps=dedent(
        f"""
        bytemuck_derive = "=1.8.1"
        risc0-zkvm = {{ version = "={RISC0_VERSION}", default-features = false }}
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
    end_pattern='sys_halt',
    target='zkevm-semantics.risc0',
)

SP1_CONFIG: Final = BuildConfig(
    build_cmd=('cargo', 'prove', 'build'),
    zkvm_deps=f'sp1-zkvm = "={SP1_VERSION}"',
    src_header=dedent(
        """
        #![no_main]
        sp1_zkvm::entrypoint!(main);
        """
    ),
    elf_path='target/elf-compilation/riscv32im-succinct-zkvm-elf/release',
    end_pattern='_ZN8sp1_zkvm8syscalls4halt12syscall_halt*',
    target='zkevm-semantics.sp1',
)


def get_symbol_value(kriscv: Tools, config: KInner, symbol: Symbol) -> bytes:
    memory = kriscv.get_memory(config)

    def read(addr: int) -> bytes:
        b = memory.get(addr)
        if b is None:
            raise ValueError(f'Uninitialized address: {addr}')
        assert 0 <= b < 256
        return bytes([b])

    return b''.join(read(i) for i in range(symbol.addr, symbol.addr + symbol.size))


def filter_symbols(elf: ELF, pattern: str) -> list[str]:
    import fnmatch

    return fnmatch.filter(elf.symbols, pattern)


def build_elf(
    project_name: str,
    load_template: TemplateLoader,
    build_config: BuildConfig,
    *,
    context: dict[str, str] | None = None,
) -> ELF:
    """
    Load the template from `templates/project_name` and build the ELF file according to the build configuration.
    Args:
        project_name: The name of the project to build.
        load_template: The template loader to use.
        build_config: The build configuration to use.
        context: Context for template instantiation
    Returns:
        The parsed ELF.
    """
    from kriscv.elf_parser import ELF

    project_dir = load_template(
        template_name=project_name,
        context={
            'zkvm_deps': build_config.zkvm_deps,
            'src_header': build_config.src_header,
            **(context or {}),
        },
    )

    run_process_2(build_config.build_cmd, cwd=project_dir)
    elf_file = project_dir / build_config.elf_path / project_name
    elf = ELF.load(elf_file)
    return elf
