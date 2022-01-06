// SPDX-License-Identifier: MIT

pragma solidity >=0.6.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";

// An NFT contract where the tokenURI can be one of the 3 different dogs. -> Randomly selected.

contract AdvancedCollectible is ERC721, VRFConsumerBase {
    uint256 public tokenCounter;
    bytes32 public keyhash;
    uint256 public fee;
    string public tokenURI;
    enum Breed {
        PUG,
        SHIBA_INU,
        ST_BERNARD
    }
    mapping(uint256 => Breed) public tokenIdtoBreed;
    mapping(uint256 => string) private _tokenURIs;
    mapping(bytes32 => address) public requestIdToSender;

    event requestedCollectible(bytes32 indexed requestId, address requester);
    event breedAssigned(uint256 indexed tokenId, Breed breed);
    event tokenIdToURI(uint256 indexed tokenId, string _tokenURI);

    constructor(
        address _vrfCoordinator,
        address _linkToken,
        bytes32 _keyHash,
        uint256 _fee
    )
        public
        VRFConsumerBase(_vrfCoordinator, _linkToken)
        ERC721("Doggy", "DOG")
    {
        tokenCounter = 0;
        keyhash = _keyHash;
        fee = _fee;
    }

    function createCollectible() public returns (bytes32) {
        bytes32 requestID = requestRandomness(keyhash, fee);
        requestIdToSender[requestID] = msg.sender;
        emit requestedCollectible(requestID, msg.sender);
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: caller is not owner nor Approved."
        );
        _tokenURIs[tokenId] = _tokenURI;
        emit tokenIdToURI(tokenId, _tokenURI);
    }

    function fulfillRandomness(bytes32 requestID, uint256 randomNumber)
        internal
        override
    {
        Breed breed = Breed(randomNumber % 3);
        uint256 newTokenId = tokenCounter;
        tokenIdtoBreed[newTokenId] = breed;
        emit breedAssigned(newTokenId, breed);
        address owner = requestIdToSender[requestID];
        _safeMint(owner, newTokenId);

        tokenCounter = tokenCounter + 1;
    }
}
