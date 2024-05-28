from core.ai_utils import generate_ai_response
from context_manager import context_manager
from logger import log_conversation
from termcolor import cprint
import traceback

def generate_full_prompt(context, user_prompt):
    system_prompt = "You are a helpful assistant with expertise in software engineering and GitHub repository analysis."
    previous_summary = context_manager.summarize_previous_interactions()
    return f"{context}\n\n{previous_summary}\n\nUser Prompt: {user_prompt}", system_prompt

def process_user_prompt(previous_interactions, conversation_log, context):
    try:
        user_prompt = input("Enter your prompt: ")
        full_prompt, system_prompt = generate_full_prompt(context, user_prompt)
        ai_response, previous_interactions, tokens_used = generate_ai_response(system_prompt, full_prompt, previous_interactions)
        cprint(ai_response, 'yellow')
        log_conversation(user_prompt, ai_response, conversation_log)
        return previous_interactions
    except Exception as e:
        cprint(f"Error in process_user_prompt: {e}", 'red')
        traceback.print_exc()
        return previous_interactions
