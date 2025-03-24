from __future__ import annotations

import json
from pathlib import Path
from subprocess import CalledProcessError
from typing import TYPE_CHECKING, NamedTuple

from pyk.utils import check_file_path, run_process_2

if TYPE_CHECKING:
    from typing import Any


class Contract(NamedTuple):
    bin_runtime: bytes
    abi: dict[str, Any]


def compile(file: str | Path, contract: str) -> Contract:
    file = Path(file)
    check_file_path(file)

    try:
        proc_res = run_process_2(['solc', str(file), '--combined-json', 'abi,bin-runtime'])
    except CalledProcessError as err:
        raise RuntimeError(f'Compilation failed with status {err.returncode}: {err.stderr}') from err

    data = json.loads(proc_res.stdout)
    rel_file = file.relative_to(Path().resolve(), walk_up=True)
    contract_data = data['contracts'][f'{rel_file}:{contract}']

    abi = contract_data['abi']
    bin_runtime = bytes.fromhex(contract_data['bin-runtime'])
    return Contract(bin_runtime=bin_runtime, abi=abi)
