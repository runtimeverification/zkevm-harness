from __future__ import annotations

from typing import TYPE_CHECKING
from collections.abc import Callable

import pytest
from kriscv.symtools import SymTools
from kriscv.tools import Tools

from .utils import TemplateLoader

if TYPE_CHECKING:
    from pathlib import Path


@pytest.fixture
def load_template(tmp_path: Path) -> TemplateLoader:
    return TemplateLoader(tmp_path)


@pytest.fixture
def tools(tmp_path: Path) -> Callable[[str], Tools]:
    def _tools(target: str) -> Tools:
        from pyk.kdist import kdist

        definition_dir = kdist.get(target)

        temp_dir = tmp_path / 'kriscv'
        temp_dir.mkdir()
        return Tools(definition_dir, temp_dir=temp_dir)

    return _tools


@pytest.fixture
def symtools(tmp_path: Path) -> SymTools:
    return SymTools.default(proof_dir=tmp_path)
