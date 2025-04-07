from __future__ import annotations

import json
from pathlib import Path
from subprocess import CalledProcessError
from typing import TYPE_CHECKING, NamedTuple

from pyk.utils import check_file_path, run_process_2

if TYPE_CHECKING:
    from typing import Any


class Contract(NamedTuple):
    """
    A named tuple representing a compiled Solidity contract.

    Attributes:
        bin_runtime: The runtime bytecode of the contract.
        abi: The ABI of the contract.
    """

    bin_runtime: bytes
    abi: dict[str, Any]

    def calldata(self, fn: str, *args: Any) -> bytes:
        """
        Encode a function call to the contract.

        Args:
            fn: The name of the function to call.
            args: The arguments to pass to the function.

        Returns:
            The calldata in hex format for the function call.
        """
        from web3 import Web3

        w3 = Web3()
        contract = w3.eth.contract(abi=self.abi)
        encoded = contract.encode_abi(fn, args)
        return bytes.fromhex(encoded[2:])


def compile(file: str | Path, contract: str) -> Contract:
    """
    Compile a Solidity contract using solc.

    Args:
        file: The path to the contract file.
        contract: The name of the contract to compile.

    Returns:
        A `Contract` named tuple containing the contract's ABI and runtime bytecode.
    """
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
