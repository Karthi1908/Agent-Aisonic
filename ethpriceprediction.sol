// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "./PredictionToken.sol";

contract ETHPricePrediction is Ownable {
    PredictionToken public rewardToken;
    
    struct Prediction {
        uint256 predictedPrice;
        uint256 timestamp;
        string discordId;
    }
    
    struct Round {
        uint256 startTime;
        uint256 actualPrice;
        bool isRevealed;
        address winner;
        uint256 winningDifference;
        address[] participants;
    }
    
    mapping(address => string) public addressToDiscord; // ETH address to Discord ID
    mapping(string => address) public discordToAddress; // Discord ID to ETH address (new)
    mapping(uint256 => mapping(address => Prediction)) public predictions;
    mapping(uint256 => Round) public rounds;
    
    uint256 public constant PREDICTION_DURATION = 10 minutes;
    uint256 public constant WAIT_DURATION = 5 minutes;
    uint256 public constant ROUND_INTERVAL = 15 minutes;
    uint256 public constant REWARD_AMOUNT = 100; // 100 tokens
    
    uint256 public currentRound;
    uint256 public lastRoundStart;
    
    event UserRegistered(address indexed user, string discordId);
    event PredictionSubmitted(uint256 indexed round, address indexed user, uint256 predictedPrice);
    event RoundStarted(uint256 indexed round, uint256 startTime);
    event PriceRevealed(uint256 indexed round, uint256 actualPrice, address winner);
    
    constructor(address _rewardToken) Ownable(msg.sender) {
        require(_rewardToken != address(0), "Invalid token address");
        rewardToken = PredictionToken(_rewardToken);
        currentRound = 1;
        lastRoundStart = block.timestamp;
        rounds[currentRound].startTime = lastRoundStart;
        emit RoundStarted(currentRound, lastRoundStart);
    }
    
    function registerUser(address _user, string calldata _discordId) external onlyOwner {
        require(_user != address(0), "Invalid address");
        require(bytes(_discordId).length > 0, "Discord ID cannot be empty");
        require(bytes(addressToDiscord[_user]).length == 0, "Address already registered");
        require(discordToAddress[_discordId] == address(0), "Discord ID already registered");
        
        addressToDiscord[_user] = _discordId;
        discordToAddress[_discordId] = _user;
        emit UserRegistered(_user, _discordId);
    }
    
    // Modified: Only owner can submit predictions, uses Discord ID to derive address
    function submitPrediction(uint256 _predictedPrice, string calldata _discordId) external onlyOwner {
        address participant = discordToAddress[_discordId];
        require(participant != address(0), "Discord ID not registered");
        require(block.timestamp < lastRoundStart + PREDICTION_DURATION, "Prediction period ended");
        require(predictions[currentRound][participant].predictedPrice == 0, "Already predicted this round");
        
        predictions[currentRound][participant] = Prediction({
            predictedPrice: _predictedPrice,
            timestamp: block.timestamp,
            discordId: _discordId
        });
        
        Round storage current = rounds[currentRound];
        bool alreadyParticipating = false;
        for (uint256 i = 0; i < current.participants.length; i++) {
            if (current.participants[i] == participant) {
                alreadyParticipating = true;
                break;
            }
        }
        if (!alreadyParticipating) {
            current.participants.push(participant);
        }
        
        emit PredictionSubmitted(currentRound, participant, _predictedPrice);
    }
    
    function awardWinners(uint256 _actualPrice) external onlyOwner {
        require(block.timestamp >= lastRoundStart + PREDICTION_DURATION + WAIT_DURATION, 
                "Waiting period not over");
        require(!rounds[currentRound].isRevealed, "Price already revealed");
        
        Round storage current = rounds[currentRound];
        address winner = address(0);
        uint256 minDifference = type(uint256).max;
        
        for (uint256 i = 0; i < current.participants.length; i++) {
            address participant = current.participants[i];
            uint256 predictedPrice = predictions[currentRound][participant].predictedPrice;
            if (predictedPrice > 0) {
                uint256 difference = _actualPrice > predictedPrice
                    ? _actualPrice - predictedPrice
                    : predictedPrice - _actualPrice;
                if (difference < minDifference) {
                    minDifference = difference;
                    winner = participant;
                }
            }
        }
        
        current.actualPrice = _actualPrice;
        current.isRevealed = true;
        current.winner = winner;
        current.winningDifference = minDifference;
        
        if (winner != address(0)) {
            rewardToken.mint(winner, REWARD_AMOUNT); // Mint new tokens instead of transfer
        }
        
        emit PriceRevealed(currentRound, _actualPrice, winner);
        
        currentRound++;
        lastRoundStart = block.timestamp;
        rounds[currentRound].startTime = lastRoundStart;
        emit RoundStarted(currentRound, lastRoundStart);
    }
    
    function isPredictionOpen() public view returns (bool) {
        return block.timestamp < lastRoundStart + PREDICTION_DURATION;
    }
    
    function getRoundStatus() public view returns (
        uint256 roundNumber,
        uint256 timeRemainingPrediction,
        uint256 timeRemainingReveal,
        bool revealed
    ) {
        roundNumber = currentRound;
        revealed = rounds[currentRound].isRevealed;
        
        if (block.timestamp < lastRoundStart + PREDICTION_DURATION) {
            timeRemainingPrediction = (lastRoundStart + PREDICTION_DURATION) - block.timestamp;
            timeRemainingReveal = 0;
        } else if (block.timestamp < lastRoundStart + ROUND_INTERVAL) {
            timeRemainingPrediction = 0;
            timeRemainingReveal = (lastRoundStart + ROUND_INTERVAL) - block.timestamp;
        } else {
            timeRemainingPrediction = 0;
            timeRemainingReveal = 0;
        }
    }
    
    function getParticipants(uint256 round) public view returns (address[] memory) {
        return rounds[round].participants;
    }
    
    function getParticipantCount(uint256 round) public view returns (uint256) {
        return rounds[round].participants.length;
    }
}