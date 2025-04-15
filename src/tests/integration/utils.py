from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import TYPE_CHECKING, Iterator, NamedTuple

if TYPE_CHECKING:
    from typing import Final

    from elftools.elf.elffile import ELFFile  # type: ignore


TEST_DATA_DIR: Final = (Path(__file__).parent / 'test-data').resolve(strict=True)
DEPS_DIR: Final = (Path(__file__).parents[3] / 'deps').resolve(strict=True)
TEMPLATE_DIR: Final = TEST_DATA_DIR / 'templates'

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


def resolve_symbol(elf_file: Path, symbol: str) -> int:
    from kriscv.elf_parser import read_unique_symbol

    with _elf_file(file=elf_file) as elf:
        return read_unique_symbol(elf, symbol, error_loc=None)


def get_symbols(elf_file: Path, pattern: str) -> list[str]:
    import fnmatch

    with _elf_file(file=elf_file) as elf:
        symtab = elf.get_section_by_name('.symtab')
        assert symtab

        func_symbols = [
            sym.name
            for sym in symtab.iter_symbols()
            if sym['st_info']['type'] == 'STT_FUNC'  # Check if symbol type is FUNC
        ]

        return fnmatch.filter(func_symbols, pattern)


@contextmanager
def _elf_file(file: Path) -> Iterator[ELFFile]:
    from elftools.elf.elffile import ELFFile  # type: ignore

    with file.open('rb') as f:
        elf = ELFFile(f)
        yield elf
