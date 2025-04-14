from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Final


TEST_DATA_DIR: Final = (Path(__file__).parent / 'test-data').resolve(strict=True)
DEPS_DIR: Final = (Path(__file__).parents[3] / 'deps').resolve(strict=True)

RISC0_VERSION: Final = (DEPS_DIR / 'risc0_release').read_text().rstrip()
SP1_VERSION: Final = (DEPS_DIR / 'sp1_release').read_text().rstrip()
