// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract PrivateMapping {
    mapping(string => string) private data;

    constructor(string memory _key) {
        data["secret"] = _key;
    }
    
    function setStorage(bytes32 _slot, bytes32 _value) public {
        bytes32 s = _slot;
        assembly {
            sstore(s, _value)
        }
    }

    function getStorage(bytes32 _slot) public view returns (bytes32 value) {
        bytes32 s = _slot;
        assembly {
            value := sload(s)
        }
    }
}
