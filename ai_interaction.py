from context_manager import context_manager
from core.ai_utils import generate_ai_response
from logger import log_conversation
import traceback

def generate_full_prompt(context, user_prompt):
    system_prompt = "You are a helpful assistant with expertise in software engineering and GitHub repository analysis."
    previous_summary = context_manager.summarize_previous_interactions()

    file_contents_summary = "Summary of analyzed file contents:\n"
    for file_path, content in context_manager.global_context["file_contents"].items():
        file_contents_summary += f"File: {file_path}\nContent: {content[:1000]}\n\n"

    # Include summaries in the prompt
    summaries = "Summaries of directories and files:\n"
    for path, summary in context_manager.global_context["summaries"].items():
        summaries += f"Path: {path}\nSummary: {summary}\n\n"

    full_prompt = f"{previous_summary}\n\n{file_contents_summary}\n\n{summaries}\n\nUser Prompt: {user_prompt}"
    print("DEBUG: Full prompt generated in generate_full_prompt:")
    print(full_prompt[:500])
    return full_prompt, system_prompt


def process_user_prompt(previous_interactions, conversation_log, context):
    try:
        user_prompt = input("Enter your prompt: ")
        context_manager.add_interaction(f"User Prompt: {user_prompt}")

        full_prompt, system_prompt = generate_full_prompt(context, user_prompt)
        ai_response, previous_interactions, tokens_used = generate_ai_response(system_prompt, full_prompt, previous_interactions)

        context_manager.add_interaction(f"AI Response: {ai_response}")

        print(ai_response)  # Replace cprint with print for debugging
        log_conversation(user_prompt, ai_response, conversation_log)

        print("DEBUG: AI response received in process_user_prompt:")
        print(ai_response[:500])
        return previous_interactions
    except Exception as e:
        print(f"Error in process_user_prompt: {e}")  # Replace cprint with print for debugging
        traceback.print_exc()
        return previous_interactions

