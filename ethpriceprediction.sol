// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/IERC20Metadata.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract EthPricePrediction is Ownable {
    struct User {
        uint256 prediction;
        uint256 discordId;
        bool registered;
    }

    struct Prediction {
        uint256 predictionValue;
        address userAddress;
    }

    mapping(address => User) public users;
    mapping(uint256 => Prediction) public predictions;
    uint256[] public predictionValues;
    IERC20 public rewardToken;
    uint256 public predictionWindowDuration = 45 minutes;
    uint256 public predictionInterval = 1 hours;
    uint256 public lastPredictionTime;
    uint256 public startTime;
    uint256 public currentPredictionRound;

    event UserRegistered(address indexed userAddress, uint256 discordId);
    event PredictionSubmitted(
        address indexed userAddress,
        uint256 prediction
    );
    event WinnerAwarded(address indexed winnerAddress, uint256 amount);
    event PredictionResult(uint256 actualPrice, uint256 round);

    constructor(address tokenAddress) Ownable(msg.sender) {
        rewardToken = IERC20(tokenAddress);
        lastPredictionTime = block.timestamp;
        startTime =block.timestamp ;
        currentPredictionRound = 1;
    }

    function registerUser(uint256 _discordId,address _userAddress) public {
        require(!users[_userAddress].registered, "User already registered");
        users[_userAddress] = User({
            prediction: 0,
            discordId: _discordId,
            registered: true
        });
        emit UserRegistered(_userAddress, _discordId);
    }

    function submitPrediction(address _userAddress, uint256 _prediction) public onlyOwner {
        require(users[_userAddress].registered, "User not registered");
        require(
        ((block.timestamp - startTime) % 60 minutes) < predictionWindowDuration, 
            "Prediction window is closed"
        );
        users[_userAddress].prediction = _prediction;

        if (predictions[_prediction].userAddress == address(0)) {
            predictions[_prediction] = Prediction({
                predictionValue: _prediction,
                userAddress: _userAddress
            });
            predictionValues.push(_prediction);
        }

        emit PredictionSubmitted(_userAddress, _prediction);
    }

    function awardWinners(uint256 _actualPrice) public onlyOwner {
        require(
            block.timestamp >= lastPredictionTime + predictionInterval,
            "Prediction interval not reached"
        );

        require(predictionValues.length > 0, "No predictions submitted");

        uint256[] memory absDiffs = new uint256[](predictionValues.length);
        for (uint256 i = 0; i < predictionValues.length; i++) {
            if (_actualPrice > predictionValues[i]) {
                absDiffs[i] = _actualPrice - predictionValues[i];
            } else {
                absDiffs[i] = predictionValues[i] - _actualPrice;
            }
        }

        uint256 firstMinIndex = findMinIndex(absDiffs);
        uint256 firstMinPrediction = predictionValues[firstMinIndex];
        address firstWinner = predictions[firstMinPrediction].userAddress;

        uint256 secondMinIndex = findSecondMinIndex(absDiffs, firstMinIndex);
        uint256 secondMinPrediction = predictionValues[secondMinIndex];
        address secondWinner = predictions[secondMinPrediction].userAddress;

        IERC20Metadata tokenMetadata = IERC20Metadata(address(rewardToken));

        if (firstWinner != address(0)) {
            rewardToken.transfer(
                firstWinner,
                100 * 10**tokenMetadata.decimals()
            );
            emit WinnerAwarded(firstWinner, 100 * 10**tokenMetadata.decimals());
        }

        if (secondWinner != address(0)) {
            rewardToken.transfer(
                secondWinner,
                50 * 10**tokenMetadata.decimals()
            );
            emit WinnerAwarded(secondWinner, 50 * 10**tokenMetadata.decimals());
        }

        emit PredictionResult(_actualPrice, currentPredictionRound);

        delete predictionValues;

        lastPredictionTime = block.timestamp;
        currentPredictionRound++;
    }

    function findMinIndex(uint256[] memory arr)
        internal
        pure
        returns (uint256)
    {
        uint256 minIndex = 0;
        for (uint256 i = 1; i < arr.length; i++) {
            if (arr[i] < arr[minIndex]) {
                minIndex = i;
            }
        }
        return minIndex;
    }

    function findSecondMinIndex(uint256[] memory arr, uint256 firstMinIndex)
        internal
        pure
        returns (uint256)
    {
        uint256 secondMinIndex = (firstMinIndex == 0) ? 1 : 0;
        for (uint256 i = 0; i < arr.length; i++) {
            if (i != firstMinIndex && arr[i] < arr[secondMinIndex]) {
                secondMinIndex = i;
            }
        }
        return secondMinIndex;
    }

    function setPredictionWindowDuration(uint256 _durationMinutes) public onlyOwner {
        predictionWindowDuration = _durationMinutes * 1 minutes;
    }

    function setPredictionInterval(uint256 _intervalHours) public onlyOwner {
        predictionInterval = _intervalHours * 1 hours;
    }

    function getPredictionValues() public view returns (uint256[] memory) {
        return predictionValues;
    }

    function getPredictionWindowEnd() public view returns (uint256) {
        return lastPredictionTime + predictionWindowDuration;
    }
}