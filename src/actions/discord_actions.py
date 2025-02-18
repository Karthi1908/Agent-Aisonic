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
