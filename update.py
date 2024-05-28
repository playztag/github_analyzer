import os
import shutil

# Directories and files to create
new_directories = [
    'config', 'core', 'utils'
]

new_files_content = {
    'context_manager.py': """class ContextManager:
    def __init__(self):
        self.global_context = {
            "summaries": {},
            "previous_prompts": [],
            "analyzed_files": [],
            "analyzed_directories": []
        }

    def add_analyzed_directory(self, directory_path):
        self.global_context["analyzed_directories"].append(directory_path)

    def add_analyzed_file(self, file_path):
        self.global_context["analyzed_files"].append(file_path)

    def add_summary(self, key, summary):
        self.global_context["summaries"][key] = summary

    def add_previous_prompt(self, prompt):
        self.global_context["previous_prompts"].append(prompt)

    def summarize_previous_interactions(self):
        summary = "Summary of previous interactions:\\n"
        for item in self.global_context["summaries"].values():
            summary += f"{item}\\n"
        return summary

    def get_context(self):
        return self.global_context

context_manager = ContextManager()
""",
    'ai_interaction.py': """from core.ai_utils import generate_ai_response
from context_manager import context_manager
from logger import log_conversation
from termcolor import cprint
import traceback

def generate_full_prompt(context, user_prompt):
    system_prompt = "You are a helpful assistant with expertise in software engineering and GitHub repository analysis."
    previous_summary = context_manager.summarize_previous_interactions()
    return f"{context}\\n\\n{previous_summary}\\n\\nUser Prompt: {user_prompt}"

def process_user_prompt(previous_interactions, conversation_log, context):
    try:
        user_prompt = input("Enter your prompt: ")
        full_prompt = generate_full_prompt(context, user_prompt)
        ai_response, previous_interactions, tokens_used = generate_ai_response(system_prompt, full_prompt, previous_interactions)
        cprint(ai_response, 'yellow')
        log_conversation(user_prompt, ai_response, conversation_log)
        return previous_interactions
    except Exception as e:
        cprint(f"Error in process_user_prompt: {e}", 'red')
        traceback.print_exc()
        return previous_interactions
""",
    'logger.py': """import traceback

def log_conversation(user_prompt, ai_response, conversation_log):
    try:
        with open(conversation_log, 'a') as log_file:
            log_file.write(f"User: {user_prompt}\\n")
            log_file.write(f"AI: {ai_response}\\n\\n")
    except Exception as e:
        print(f"Error in log_conversation: {e}")
        traceback.print_exc()
"""
}

# Create new directories if they don't exist
for directory in new_directories:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Create new files with content
for file, content in new_files_content.items():
    with open(file, 'w') as f:
        f.write(content)

# Function to update import statements
def update_imports(file_path, import_map):
    try:
        with open(file_path, 'r') as file:
            content = file.readlines()

        new_content = []
        for line in content:
            for old_import, new_import in import_map.items():
                if old_import in line:
                    line = line.replace(old_import, new_import)
            new_content.append(line)

        with open(file_path, 'w') as file:
            file.writelines(new_content)
        print(f"Updated imports in {file_path}")
    except Exception as e:
        print(f"Error updating imports in {file_path}: {e}")
        traceback.print_exc()

# Define import mappings for the remaining files
import_mappings_remaining = {
    "main.py": {
        "from utils.menu": "from utils.menu",
        "from core.summarize": "from core.summarize",
        "from utils.log_utils": "from logger"
    },
    "utils/menu.py": {
        "from utils.menu": "from utils.menu",
        "from core.github_utils": "from core.github_utils",
        "from core.summarize": "from core.summarize",
        "from utils.log_utils": "from logger",
        "from utils.interaction_utils": "from ai_interaction"
    },
}

# List of remaining files to update
remaining_files = ["main.py", "utils/menu.py"]

# Update imports in each remaining file
print("Updating import statements for remaining files...")
for file in remaining_files:
    if os.path.exists(file) and file in import_mappings_remaining:
        update_imports(file, import_mappings_remaining[file])
    elif not os.path.exists(file):
        print(f"File {file} not found, skipping...")
    else:
        print(f"No import mappings for {file}, skipping...")

print("Import statements update for remaining files completed successfully.")