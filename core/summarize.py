from core.ai_utils import generate_ai_response
from termcolor import cprint
from prompts import SYSTEM_PROMPT, USER_PROMPT_SUMMARY
import traceback

def summarize_readme_and_structure(readme_text, repo_name, branches):
    cprint("Starting to summarize the README file and repository structure...", 'cyan')
    user_prompt = USER_PROMPT_SUMMARY.format(readme_text=readme_text, repo_name=repo_name, branches=branches)

    try:
        summary, _, tokens_used = generate_ai_response(SYSTEM_PROMPT, user_prompt)
        return summary, _, tokens_used
    except Exception as e:
        cprint(f"Error in summarize_readme_and_structure: {e}", 'red')
        traceback.print_exc()
        return f"Error during GPT-4 API call.", [], 0
