from termcolor import cprint
from core.github_utils import estimate_code_size
from utils.file_utils import analyze_file_choice
from utils.directory_utils import analyze_directory_choice
from utils.interaction_utils import process_user_prompt
import traceback

marked_items = {}

def mark_item(path):
    if path in marked_items:
        marked_items[path] = not marked_items[path]
    else:
        marked_items[path] = True

def display_marked_items():
    for path, marked in marked_items.items():
        mark = '✔' if marked else '☐'
        cprint(f"{mark} {path}", 'yellow')

def handle_directory_choice(contents, dir_choice, previous_interactions, conversation_log, response_cache, repo, branch_name):
    """Handle user's choice to navigate into a directory or analyze a file."""
    try:
        if dir_choice < len(contents):
            if contents[dir_choice].type == "dir":
                return contents[dir_choice].path, previous_interactions
            elif contents[dir_choice].type == "file":
                return analyze_file_choice(contents[dir_choice], previous_interactions, conversation_log, response_cache, repo, branch_name)
        else:
            cprint("Invalid choice. Please select a valid item.", 'red')
        return None, previous_interactions
    except Exception as e:
        cprint(f"Error in handle_directory_choice: {e}", 'red')
        traceback.print_exc()
        return None, previous_interactions

def capture_selected_directories(selected_directories):
    """Capture selected directories for analysis."""
    cprint("Capturing selected directories:", 'cyan')
    for dir in selected_directories:
        cprint(f"- {dir}", 'cyan')

def display_contents(contents):
    directories = [content for content in contents if content.type == "dir"]
    files = [content for content in contents if content.type == "file"]
    
    cprint("Directories:", 'blue')
    for i, content in enumerate(directories):
        cprint(f"{i + 1}. {content.path}", 'blue')
    
    cprint("Files:", 'green')
    for i, content in enumerate(files):
        lines_of_code = estimate_code_size(repo, content.path, branch_name)
        cprint(f"{i + 1 + len(directories)}. {content.path} - Lines of Code: {lines_of_code}", 'green')
