import os
from github import Github
from dotenv import load_dotenv
from termcolor import cprint
from core.summarize import summarize_directory
from utils.log_utils import log_conversation
from utils.menu import navigation_menu
import openai
import traceback

# Load environment variables from .env file
load_dotenv()

# Set up your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Set up GitHub access token
github_token = os.getenv('GITHUB_TOKEN')
g = Github(github_token)

def get_default_branch(repo):
    return repo.default_branch

def main():
    repo_url = "https://github.com/betaflight/betaflight"
    conversation_log = "conversation_log.txt"
    
    try:
        # Parse repository name from URL
        repo_name = "betaflight/betaflight"
        
        # Get repository object
        repo = g.get_repo(repo_name)
        
        # Fetch branches
        branches = [branch.name for branch in repo.get_branches()]
        
        # Fetch and cache the root directory contents
        root_contents = repo.get_contents("", ref=repo.default_branch)
        
        # Summarize initial directory (root)
        summary_cache = {}
        summary, _, tokens_used = summarize_directory(repo, "", root_contents, [], summary_cache)
        cprint("Repository Purpose Summary:\n", 'yellow')
        cprint(summary, 'yellow')
        
        # Log conversation
        log_conversation("Initial repository analysis", summary, conversation_log)
        
        # Start interactive navigation menu
        navigation_menu(repo, conversation_log, root_contents)
    
    except Exception as e:
        cprint(f"Error in main: {e}", 'red')
        traceback.print_exc()

if __name__ == "__main__":
    main()
