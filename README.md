## AI Agent: "AiSonic" - Accuracy Verification on Sonic Blockchain

**Detailed Description:**

**"AiSonic"** is an autonomous AI agent designed to operate within the Sonic blockchain ecosystem. Its primary function is to verify the accuracy of price predictions made by users and other AI agents, specifically focusing on the predictions of Ethereum (ETH) price. The agent leverages smart contract functionality on the Sonic blockchain to record, track, and compare predictions against real-time price data provided by the Allora network, a decentralized oracle.

**Key Features:**

* **Social Media Integration (Discord Focused):**
    * The agent monitors designated Discord channels for user-submitted ETH price predictions.
    * It utilizes the Zerepy framework and Discord API integrations to parse and extract relevant prediction data from messages.
    * Future implementations will extend this functionality to Twitter and Farcaster, enabling cross-platform prediction tracking.
* **Smart Contract Interaction:**
    * The agent interacts with a dedicated smart contract deployed on the Sonic blockchain.
    * This smart contract stores user registration data (Discord ID, Sonic address), records submitted predictions, and manages reward distribution.
* **Allora Oracle Integration:**
    * "AiSonic" integrates with the Allora network to obtain accurate and up-to-date ETH price data.
    * This data serves as the ground truth against which user predictions are compared.
* **Accuracy Verification:**
    * The agent compares each submitted prediction with the corresponding price data from Allora at a predefined time interval (e.g., hourly).
    * It calculates the accuracy of each prediction, typically based on the absolute difference between the predicted and actual prices.
* **Reward Distribution:**
    * Users and agents whose predictions fall within a specified accuracy threshold receive rewards in the form of a designated ERC-20 token on the Sonic blockchain.
    * The reward amount may vary based on the prediction's accuracy.
* **Zerepy Framework:**
    * The agent is built using the Zerepy framework, which facilitates the creation of autonomous agents on the blockchain.
    * Zerepy provides tools for managing agent state, interacting with smart contracts, and handling external data sources.

**Working Mechanism:**

1.  **User Registration:**
    * Users register with the smart contract by providing their Discord ID and Sonic blockchain address.
    * This registration links their social media identity with their on-chain identity.
2.  **Prediction Submission (Discord):**
    * Users post their ETH price predictions in designated Discord channels.
    * The AiSonic agent is constantly monitoring these channels.
    * The agent parses the messages, extracts the prediction data, and identifies the user's Discord ID.
3.  **Smart Contract Recording:**
    * The agent calls the smart contract's `submitPrediction` function, providing the user's Discord ID and the prediction value.
    * The smart contract stores the prediction, associating it with the user's Sonic address.
4.  **Allora Data Retrieval:**
    * At the end of each prediction round (e.g., hourly), the agent queries the Allora network for the actual ETH price.
5.  **Accuracy Calculation:**
    * The agent retrieves the stored predictions from the smart contract.
    * It calculates the absolute difference between each prediction and the actual price from Allora.
6.  **Reward Distribution:**
    * The agent calls the smart contract's `awardWinner` function, providing the actual price.
    * The smart contract identifies the user with the most accurate prediction and distributes the reward tokens.
    * The smart contract also stores the round data.
7.  **Round Cycle:**
    * The process repeats for each prediction round, with the agent continuously monitoring social media, retrieving data from Allora, and distributing rewards.

**Technology Stack:**

* **Sonic Blockchain:** The underlying blockchain infrastructure.
* **Solidity:** Smart contract development language.
* **Zerepy:** Autonomous agent framework.
* **Allora:** Decentralized oracle network.
* **Discord API:** Social media integration.
* **Twitter API:** Social media integration.
* **Farcaster:** Social media integration.
* **Python:** Agent development and API integration.

**Benefits:**

* **Decentralized Accuracy Verification:** Leverages blockchain technology for transparent and auditable prediction verification.
* **Incentivized Participation:** Rewards users and agents for accurate predictions, fostering community engagement.
* **Reliable Price Data:** Uses the Allora network for trusted and tamper-proof price data.
* **Cross-Platform Integration (Future):** Extends prediction tracking to multiple social media platforms.
* **Autonomous Operation:** The agent operates autonomously, reducing the need for manual intervention.

**Future Enhancements:**

* **Advanced Prediction Analysis:** Implement machine learning algorithms to analyze prediction patterns and identify skilled predictors.
* **Reputation System:** Develop a reputation system to track user and agent performance over time.
* **Dynamic Reward Mechanisms:** Introduce dynamic reward mechanisms based on prediction difficulty and market volatility.
* **Governance Integration:** Allow token holders to participate in the governance of the prediction platform.
* **Expand social media support.**

**"AiSonic"** aims to create a reliable and engaging prediction platform on the Sonic blockchain, promoting accurate price forecasting and rewarding participants for their expertise.