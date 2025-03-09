import time 
import json
from src.action_handler import register_action
from src.helpers import print_h_bar
from src.prompts import POST_PROMPT, REPLY_PROMPT, PARSING_PROMPT
channel_id = "1337747758920237118"

@register_action("post-message")
def post_message(agent, **kwargs):

    
    agent.logger.info("\n📝 GENERATING NEW DISCORD POST")
    print_h_bar()

    prompt = POST_PROMPT.format(agent_name = agent.name)
    post_text = agent.prompt_llm(prompt)

    if post_text:
        agent.logger.info("\n🚀 Posting to discord:")
        agent.logger.info(f"'{post_text}'")
        agent.connection_manager.perform_action(
                connection_name="discord",
                action_name="post-message",
                params=[channel_id, post_text]
            )

        agent.logger.info("\n✅ Discord post done successfully!")
        return True
    
@register_action("reply-to-message")
def reply_to_message(agent, **kwargs):
    if "timeline_messages" in agent.state and agent.state["timeline_messages"] is not None and len(agent.state["timeline_messages"]) > 0:
        message = agent.state["timeline_messages"].pop(0)
        agent.logger.info(f"\n💬 message {message}...")
        message_id = message.get('id')
        message_message = message.get('message')[22:]
        message_author = message.get('author')
        if not message_id:
            return 

        base_prompt = PARSING_PROMPT.format(text=message_message )
        system_prompt = "You are a precise command parser."
        response  = agent.prompt_llm(prompt=base_prompt, system_prompt=system_prompt)  
        agent.logger.info(f"\n💬 LLM response {response}")

        # Assuming OpenAI returns a JSON-formatted string
        parsed_result = eval(response) if response.startswith("{") else json.loads(response)

            # Handle registrations first
        for reg in parsed_result["registrations"]:
            agent.logger.info(f"\n💬 Inside reg")
            wallet_address = reg.get("wallet_address")
            if wallet_address:
        # Direct passthrough to connection method - add your logic before/after this call!
                reply_message = agent.connection_manager.connections["sonic"].register_user(
                    discord_id=message_author,
                    user_address=wallet_address
                )
                agent.logger.info(f"\n💬 {wallet_address} is registered for {message_author} sucessfully...")
                agent.connection_manager.perform_action(
                    connection_name="discord",
                    action_name="reply-to-message",
                    params=[channel_id, message_id, reply_message]
                )

    # Handle predictions next
        for pred in parsed_result["predictions"]:
            agent.logger.info(f"\n💬 Inside pred")
            asset = pred.get("asset")
            price = pred.get("price")
            if asset and price is not None:
                reply_message = agent.connection_manager.connections["sonic"].submit_prediction(            
                    prediction=price,
                    discord_id=message_author                  
                )
                agent.logger.info(f"\n💬 Prediction for made by {message_author} for {asset} is {price} recorded sucessfully...{reply_message}")
                agent.connection_manager.perform_action(
                    connection_name="discord",
                    action_name="reply-to-message",
                    params=[channel_id, message_id, reply_message]
                )
        base_prompt = REPLY_PROMPT.format(text=message_message )
        system_prompt = agent._construct_system_prompt()
        reply_message = agent.prompt_llm(prompt=base_prompt, system_prompt=system_prompt)

        agent.logger.info(f"\n💬 GENERATING REPLY to: {message_message}...")

        if reply_message:
            agent.logger.info(f"\n🚀 Posting reply: '{reply_message}'")
            agent.connection_manager.perform_action(
                connection_name="discord",
                action_name="reply-to-message",
                params=[channel_id, message_id, reply_message]
            )
            agent.logger.info("✅ Reply posted successfully!")
            return True
    else:
        agent.logger.info("\n👀 No messages found to reply to...")
        return False
