from core.github_utils import estimate_code_size, analyze_directory
from termcolor import cprint
from utils.log_utils import log_conversation
import traceback

def analyze_directory_choice(repo, branch_name, directory_path, previous_interactions, conversation_log, response_cache):
    """Analyze the current directory and return the results."""
    try:
        if directory_path in response_cache:
            ai_response = response_cache[directory_path]
        else:
            ai_response, previous_interactions, tokens_used = analyze_directory(repo, branch_name, directory_path, previous_interactions)
            response_cache[directory_path] = ai_response
        
        cprint(ai_response, 'yellow')
        log_conversation("Directory Analysis", ai_response, conversation_log)
        return directory_path, previous_interactions
    except Exception as e:
        cprint(f"Error in analyze_directory_choice: {e}", 'red')
        traceback.print_exc()
        return directory_path, previous_interactions
