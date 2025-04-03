from __future__ import annotations

import shutil
from pathlib import Path
from typing import TYPE_CHECKING

from pyk.kbuild.utils import k_version
from pyk.kdist.api import Target
from pyk.ktool.kompile import PykBackend, kompile

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping
    from typing import Any, Final


class SourceTarget(Target):
    SRC_DIR: Final = Path(__file__).parent

    def build(self, output_dir: Path, deps: dict[str, Path], args: dict[str, Any], verbose: bool) -> None:
        shutil.copytree(deps['riscv-semantics.source'] / 'riscv-semantics', output_dir / 'riscv-semantics')
        shutil.copytree(self.SRC_DIR / 'zkevm-semantics', output_dir / 'zkevm-semantics')

    def source(self) -> tuple[Path, ...]:
        return (self.SRC_DIR,)

    def deps(self) -> tuple[str]:
        return ('riscv-semantics.source',)


class KompileTarget(Target):
    _kompile_args: Callable[[Path], Mapping[str, Any]]

    def __init__(self, kompile_args: Callable[[Path], Mapping[str, Any]]):
        self._kompile_args = kompile_args

    def build(self, output_dir: Path, deps: dict[str, Path], args: dict[str, Any], verbose: bool) -> None:
        kompile_args = self._kompile_args(deps['zkevm-semantics.source'])
        kompile(output_dir=output_dir, verbose=verbose, **kompile_args)

    def context(self) -> dict[str, str]:
        return {'k-version': k_version().text}

    def deps(self) -> tuple[str]:
        return ('zkevm-semantics.source',)


__TARGETS__: Final = {
    'source': SourceTarget(),
    'risc0': KompileTarget(
        lambda src_dir: {
            'main_file': src_dir / 'zkevm-semantics/risc0.k',
            'backend': PykBackend.LLVM,
            'include_dirs': [src_dir],
            'syntax_module': 'RISCV',
            'md_selector': 'k',
            'warnings_to_errors': True,
        },
    ),
    'sp1': KompileTarget(
        lambda src_dir: {
            'main_file': src_dir / 'zkevm-semantics/sp1.k',
            'backend': PykBackend.LLVM,
            'include_dirs': [src_dir],
            'syntax_module': 'RISCV',
            'md_selector': 'k',
            'warnings_to_errors': True,
        },
    ),
}
