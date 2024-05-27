from termcolor import cprint
from core.github_utils import estimate_code_size
from utils.cache_utils import check_cache, response_cache
from utils.constants import CACHE_FILE
import traceback

def display_navigation_menu():
    """Display navigation menu options."""
    cprint("\nNavigation Menu:", 'cyan')
    cprint("a. Mark current directory for capture", 'cyan')
    cprint("b. Capture all selected directories", 'cyan')
    cprint("c. Exit", 'cyan')
    cprint("d. Enter a prompt for AI assistance", 'cyan')
    cprint("e. Analyze current directory with AI", 'cyan')
    cprint("f. Change branch", 'cyan')
    cprint("u. Navigate up to previous directory", 'cyan')

def switch_branch(repo):
    """Switch to a different branch."""
    cprint("Available branches:", 'cyan')
    branches = repo.get_branches()
    branch_list = [branch.name for branch in branches]
    for i, branch in enumerate(branch_list):
        cprint(f"{i + 1}. {branch}", 'yellow')
    branch_choice = int(input("Enter the number of the branch to switch to: ")) - 1
    if branch_choice < len(branch_list):
        return branch_list[branch_choice]
    else:
        cprint("Invalid choice. Please select a valid branch number.", 'red')
    return None

def navigate_up(directory_path):
    """Navigate up to the previous directory."""
    if '/' in directory_path:
        parent_directory = '/'.join(directory_path.split('/')[:-1])
        return parent_directory
    else:
        return ""
