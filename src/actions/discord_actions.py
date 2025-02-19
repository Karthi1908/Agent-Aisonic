import time 
from src.action_handler import register_action
from src.helpers import print_h_bar
from src.prompts import POST_PROMPT, REPLY_PROMPT
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
        if not message_id:
            return

        agent.logger.info(f"\n💬 GENERATING REPLY to: {message.get('message', '')[22:70]}...")

        base_prompt = REPLY_PROMPT.format(text=message.get('message')[22:] )
        system_prompt = agent._construct_system_prompt()
        reply_message = agent.prompt_llm(prompt=base_prompt, system_prompt=system_prompt)

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
