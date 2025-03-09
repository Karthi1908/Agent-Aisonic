"""
This file contains the prompt templates used for generating content in various tasks.
These templates are formatted strings that will be populated with dynamic data at runtime.
"""

#Twitter prompts
POST_TWEET_PROMPT =  ("Generate an engaging tweet. Don't include any hashtags, links or emojis. Keep it under 280 characters."
                      "The tweets should be pure commentary, do not shill any coins or projects apart from {agent_name}. Do not repeat any of the"
                      "tweets that were given as example. Avoid the words AI and crypto.")

REPLY_TWEET_PROMPT = ("Generate a friendly, engaging reply to this tweet: {tweet_text}. Keep it under 280 characters. Don't include any usernames, hashtags, links or emojis. ")


#Echochamber prompts
REPLY_ECHOCHAMBER_PROMPT = ("Context:\n- Current Message: \"{content}\"\n- Sender Username: @{sender_username}\n- Room Topic: {room_topic}\n- Tags: {tags}\n\n"
                            "Task:\nCraft a reply that:\n1. Addresses the message\n2. Aligns with topic/tags\n3. Engages participants\n4. Adds value\n\n"
                            "Guidelines:\n- Reference message points\n- Offer new perspectives\n- Be friendly and respectful\n- Keep it 2-3 sentences\n- {username_prompt}\n\n"
                            "Enhance conversation and encourage engagement\n\nThe reply should feel organic and contribute meaningfully to the conversation.")


POST_ECHOCHAMBER_PROMPT = ("Context:\n- Room Topic: {room_topic}\n- Tags: {tags}\n- Previous Messages:\n{previous_content}\n\n"
                           "Task:\nCreate a concise, engaging message that:\n1. Aligns with the room's topic and tags\n2. Builds upon Previous Messages without repeating them, or repeating greetings, introductions, or sentences.\n"
                           "3. Offers fresh insights or perspectives\n4. Maintains a natural, conversational tone\n5. Keeps length between 2-4 sentences\n\nGuidelines:\n- Be specific and relevant\n- Add value to the ongoing discussion\n- Avoid generic statements\n- Use a friendly but professional tone\n- Include a question or discussion point when appropriate\n\n"
                           "The message should feel organic and contribute meaningfully to the conversation."
                           )

#Discord prompts
POST_PROMPT =  ("Generate an engaging post on your Sonic wallet and onchain activities. Post you wallet id and any latest transactions."
                "Don't include any hashtags, links or emojis. Keep it under 280 characters."
                "The posts should be pure commentary, do not shill any coins or projects apart from {agent_name}. Do not repeat any of the tweets that were given as example."
                "Avoid the words AI and crypto.")

REPLY_PROMPT = ("Generate a friendly, engaging reply to this post: {text}. Keep it under 280 characters. Don't include any usernames, hashtags, links or emojis. ")

#WRAPCAST prompts
POST_CAST_PROMPT =  ("Generate an engaging post on your Sonic and other tokens on the SONIC blockchain."
                "Don't include any hashtags, links or emojis. Keep it under 280 characters."
                "The posts should be pure commentary, and compare the original casts market prediction with allora values." 
                "Always promote {agent_name}. Do not repeat any of the casts that were given as example."
                "Avoid the words AI and crypto.")

REPLY_CAST_PROMPT = ("Generate a friendly, engaging reply to this post: {text}." 
                "The posts should be pure commentary, and compare the original casts market prediction with allora values."
                "Keep it under 280 characters. Don't include any usernames, hashtags, links or emojis. ")

PARSING_PROMPT = ("You are an intelligent assistant tasked with parsing social media messages."
                  "The message might contain: "
                  "1. A wallet address registration (e.g., 'register my wallet 0x1234567890abcdef1234567890abcdef12345678') "
                  "2. A price prediction (e.g., 'predict BTC 50000') "
                  "3. Both commands in any order "
                  "4. Neither (just a mention or random text) "
                  "Extract the parameters for each command present in the message."
                  "For wallet registration: extract the wallet address (starts with '0x', 40 hex chars). "
                  "For price prediction: extract the asset (e.g., BTC) and price (numeric value). "
                  "Return the result as a JSON object with two keys: 'registrations' and 'predictions', each containing a list of parameter dictionaries. "
                  "If no command is found, return empty lists. Message: {text}")
