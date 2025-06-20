from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from kriscv.symtools import SymTools
from kriscv.tools import Tools
from pyk.cli.utils import bug_report_arg
from pyk.kdist import kdist

from .utils import TemplateLoader

if TYPE_CHECKING:
    from collections.abc import Callable

    from pytest import Parser


def pytest_addoption(parser: Parser) -> None:
    parser.addoption(
        '--temp-dir',
        type=Path,
        help='Directory to save temporary files',
    )
    parser.addoption(
        '--save-bug-report',
        type=bool,
        default=False,
        help='Generate bug report in the temporary directory',
    )


@pytest.fixture
def custom_temp_dir(request: pytest.FixtureRequest) -> Path:
    """Return a custom temporary directory if specified, otherwise use pytest's default tmp_path."""
    temp_dir = request.config.getoption('--temp-dir')
    if temp_dir is not None:
        assert isinstance(temp_dir, Path)
        temp_dir.mkdir(parents=True, exist_ok=True)
        return temp_dir
    return request.getfixturevalue('tmp_path')


@pytest.fixture
def save_bug_report(request: pytest.FixtureRequest) -> bool:
    return request.config.getoption('--save-bug-report')


@pytest.fixture
def load_template(custom_temp_dir: Path) -> TemplateLoader:
    return TemplateLoader(custom_temp_dir)


@pytest.fixture
def tools(custom_temp_dir: Path) -> Callable[[str], Tools]:
    def _tools(target: str) -> Tools:

        definition_dir = kdist.get(target)

        temp_dir = custom_temp_dir / 'kriscv'
        temp_dir.mkdir(exist_ok=True)
        return Tools(definition_dir, temp_dir=temp_dir)

    return _tools


@pytest.fixture
def symtools(custom_temp_dir: Path, save_bug_report: bool) -> Callable[[str, str], SymTools]:
    def _symtools(haskell_target: str, llvm_target: str) -> SymTools:
        temp_dir = custom_temp_dir / 'proofs'
        temp_dir.mkdir(exist_ok=True)

        return SymTools(
            haskell_dir=kdist.get(haskell_target),
            llvm_lib_dir=kdist.get(llvm_target),
            proof_dir=temp_dir,
            bug_report=bug_report_arg(custom_temp_dir / 'debug') if save_bug_report else None,
        )

    return _symtools
