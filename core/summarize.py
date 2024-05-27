from core.ai_utils import generate_ai_response
from termcolor import cprint
from prompts import SYSTEM_PROMPT
import traceback

response_cache = {}  # Ensure the response_cache is defined

def summarize_directory(repo, directory_path, contents, previous_interactions, summary_cache):
    cprint(f"Summarizing the directory: {directory_path}...", 'cyan')
    
    if directory_path in summary_cache:
        return summary_cache[directory_path], previous_interactions, 0
    
    try:
        directories = [content.path for content in contents if content.type == "dir"]
        files = [content.path for content in contents if content.type == "file"]
        
        structure_summary = f"Directories: {directories}\nFiles: {files}\n"
    except Exception as e:
        structure_summary = f"Error fetching directory structure: {e}"
        traceback.print_exc()
    
    user_prompt = f"""
    You are analyzing a GitHub repository directory. The current directory is '{directory_path}'.
    The directory contains the following structure:
    {structure_summary}
    
    Please provide a one-paragraph summary of the important aspects of this directory and the files within it.
    Ignore any licensing information or comments and focus on the code and its functionalities.
    """

    try:
        summary, _, tokens_used = generate_ai_response(SYSTEM_PROMPT, user_prompt, previous_interactions)
        summary_cache[directory_path] = summary  # Cache the summary
        return summary, previous_interactions, tokens_used
    except Exception as e:
        cprint(f"Error in summarize_directory: {e}", 'red')
        traceback.print_exc()
        return f"Error during GPT-4 API call.", previous_interactions, 0

def summarize_file(repo, file_path, file_content, previous_interactions, summary_cache):
    cprint(f"Summarizing the file: {file_path}...", 'cyan')
    
    if file_path in summary_cache:
        return summary_cache[file_path], previous_interactions, 0
    
    prompt = f"""
    You are analyzing a GitHub repository file. The current file is '{file_path}'.
    The file contains the following contents:
    {file_content[:1000]}  # Limiting to the first 1000 characters to fit within token limits
    
    Please provide a one-paragraph summary of the important aspects of this file, its functionalities, and any notable code structures.
    Ignore any licensing information or comments and focus on the code and its functionalities.
    """
    
    try:
        summary, _, tokens_used = generate_ai_response(SYSTEM_PROMPT, prompt, previous_interactions)
        summary_cache[file_path] = summary  # Cache the summary
        return summary, previous_interactions, tokens_used
    except Exception as e:
        cprint(f"Error in summarize_file: {e}", 'red')
        traceback.print_exc()
        return f"Error during GPT-4 API call.", previous_interactions, 0
