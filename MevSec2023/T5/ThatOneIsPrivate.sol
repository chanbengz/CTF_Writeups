// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract ThatOneIsPrivate {
    string private flag;

    constructor(string memory _key) {
        flag = _key;
    }
}
