// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.0;
import "./VideoChalllengeIntro.sol";

contract Setup {
	VideoChallengeIntro public vci;

	constructor() payable {
		vci = (new VideoChallengeIntro){}();
	}
}
