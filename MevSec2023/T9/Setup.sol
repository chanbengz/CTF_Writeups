pragma solidity ^0.8.0;
import './ImpossibleNFT.sol';

contract Setup {
    ImpossibleNFT public nft;

    constructor() payable {
        nft = new ImpossibleNFT();
    }

    function isSolved() public view returns (bool) {
        return nft.isSolved();
    }
}
