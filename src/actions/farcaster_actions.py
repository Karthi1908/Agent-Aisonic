import time 
from src.action_handler import register_action
from src.helpers import print_h_bar
from src.prompts import POST_CAST_PROMPT, REPLY_CAST_PROMPT


@register_action("post-cast")
def post_cast(agent, **kwargs):

    
    agent.logger.info("\n📝 GENERATING NEW CAST")
    print_h_bar()

    prompt = POST_CAST_PROMPT.format(agent_name = agent.name)
    post_text = agent.prompt_llm(prompt)

    if post_text:
        agent.logger.info("\n🚀 Posting to Farcaster:")
        agent.logger.info(f"'{post_text}'")
        agent.connection_manager.perform_action(
                connection_name="farcaster",
                action_name="post-cast",
                params=[post_text]
            )

        agent.logger.info("\n✅ FARCASTER CAST done successfully!")
        return True
    
@register_action("reply-to-cast")
def reply_to_cast(agent, **kwargs):
    if "timeline_casts" in agent.state and agent.state["timeline_casts"] is not None and len(agent.state["timeline_casts"]) > 0:
        cast = agent.state["timeline_casts"].pop(0)
        agent.logger.info(f"\n💬 message {cast}...")
        cast_id = cast.get('id')
        if not cast_id:
            return

        agent.logger.info(f"\n💬 GENERATING REPLY to: {cast.get('message', '')[0:70]}...")

        base_prompt = REPLY_CAST_PROMPT.format(text=cast.get('message'))
        system_prompt = agent._construct_system_prompt()
        reply_message = agent.prompt_llm(prompt=base_prompt, system_prompt=system_prompt)

        if reply_message:
            agent.logger.info(f"\n🚀 Posting reply: '{reply_message}'")
            agent.connection_manager.perform_action(
                connection_name="farcaster",
                action_name="reply-to-cast",
                params=[cast_id, reply_message]
            )
            agent.logger.info("✅ Reply posted successfully!")
            return True
    else:
        agent.logger.info("\n👀 No messages found to reply to...")
        return False
