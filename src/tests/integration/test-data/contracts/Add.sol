pragma solidity ^0.8.0;

contract Add {
    function add(uint256 a, uint256 b) public pure returns (uint256 result) {
        assembly {
            result := add(a, b)
        }
    }
}
