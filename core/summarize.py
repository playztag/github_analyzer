from core.ai_utils import generate_ai_response
from termcolor import cprint
from prompts import SYSTEM_PROMPT, USER_PROMPT_SUMMARY
import traceback

response_cache = {}  # Ensure the response_cache is defined

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

def summarize_folders(repo, branch_name, directory_path, previous_interactions):
    contents = repo.get_contents(directory_path, ref=branch_name)
    directories = [content.path for content in contents if content.type == "dir"]
    prompt = f"""
    You are analyzing a GitHub repository directory. The current directory is '{directory_path}' on branch '{branch_name}'.
    The directory contains the following structure:
    {directories}
    
    Please provide a one-paragraph summary of the important aspects of this directory and the files within it.
    """
    summary, _, _ = generate_ai_response(SYSTEM_PROMPT, prompt, previous_interactions)
    response_cache[directory_path] = summary
    return summary
