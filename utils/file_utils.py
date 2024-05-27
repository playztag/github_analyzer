from core.github_utils import analyze_file
from termcolor import cprint
from utils.log_utils import log_conversation
import traceback

def analyze_file_choice(content, previous_interactions, conversation_log, response_cache, repo, branch_name):
    """Analyze a file and return the results."""
    try:
        if content.path in response_cache:
            ai_response = response_cache[content.path]
        else:
            ai_response, previous_interactions, tokens_used = analyze_file(repo, branch_name, content.path, previous_interactions)
            response_cache[content.path] = ai_response
        
        cprint(ai_response, 'yellow')
        log_conversation(f"Analyzed file: {content.path}", ai_response, conversation_log)
        return content.path, previous_interactions
    except Exception as e:
        cprint(f"Error in analyze_file_choice: {e}", 'red')
        traceback.print_exc()
        return content.path, previous_interactions
