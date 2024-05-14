// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.0;
import "./HoldTheDoor.sol";

contract Setup {
    HoldTheDoor public htd;

    constructor() payable {
        htd = new HoldTheDoor();
    }

    function isSolved() public view returns (bool) {
        return htd.flagged();
    }
}
