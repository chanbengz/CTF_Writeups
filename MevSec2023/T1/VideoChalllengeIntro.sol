//SPDX-License-Identifier: Unlicense
pragma solidity 0.8.0;

//The VaultMEVSec contains 100ETH could you succeed to steal them?
contract VideoChallengeIntro {
	address public owner;

	modifier onlyOwner() {
		require(msg.sender == owner);
		_;
	}

	constructor() payable {
		require(msg.value == 100 ether, "100ETH required for the start the challenge");
		owner = msg.sender; // Set the Owner when we call the constructor
	}

	function balance() public view returns (uint256) {
		//Return the Balance of the contract.
		return address(this).balance;
	}

	function withdraw() public onlyOwner {
		//Only the owner can withdraw the contract balance.
		payable(owner).transfer(address(this).balance); // Transfer the balance to the owner
	}

	function setOwner() public {
		//Set the owner of the contract.
		owner = msg.sender;
	}
}
