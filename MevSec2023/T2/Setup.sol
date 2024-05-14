// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.0;
import "./VaultMevSec.sol";

contract Setup {
    VaultMevSec public vms;

    constructor() payable {
        require(msg.value >= 100, "Not enough ETH to create the challenge..");
        vms = (new VaultMevSec){value: 100 ether}();
    }

    function isSolved() public view returns (bool) {
        return address(vms).balance == 0;
    }
}
