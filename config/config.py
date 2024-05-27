import os
from github import Github
import openai
from dotenv import load_dotenv
import traceback

# Load environment variables from .env file
load_dotenv()

# Set up your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Set up GitHub access token
github_token = os.getenv('GITHUB_TOKEN')
if not github_token:
    raise EnvironmentError("GitHub token not found. Please set GITHUB_TOKEN in the environment variables.")
g = Github(github_token)
