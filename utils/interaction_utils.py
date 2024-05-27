from core.ai_utils import generate_ai_response
from termcolor import cprint
from utils.log_utils import log_conversation
import traceback

def process_user_prompt(previous_interactions, conversation_log, context):
    """Process user's AI prompt and return the response."""
    try:
        user_prompt = input("Enter your prompt: ")
        system_prompt = "You are a helpful assistant with expertise in software engineering and GitHub repository analysis."
        full_prompt = f"{context}\n\nUser Prompt: {user_prompt}"
        ai_response, previous_interactions, tokens_used = generate_ai_response(system_prompt, full_prompt, previous_interactions)
        cprint(ai_response, 'yellow')
        log_conversation(user_prompt, ai_response, conversation_log)
        return previous_interactions
    except Exception as e:
        cprint(f"Error in process_user_prompt: {e}", 'red')
        traceback.print_exc()
        return previous_interactions
