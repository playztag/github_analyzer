from termcolor import cprint
from utils.navigation_utils import display_navigation_menu, switch_branch, navigate_up
from utils.cache_utils import check_cache, response_cache
from utils.directory_utils import analyze_directory_choice
from utils.interaction_utils import process_user_prompt
from utils.file_utils import analyze_file_choice
from utils.utils import handle_directory_choice, capture_selected_directories
from core.github_utils import estimate_code_size
import traceback

def execute_choice(choice, repo, branch_name, directory_path, selected_directories, conversation_log, previous_interactions):
    """Execute user choice from the navigation menu."""
    try:
        if choice.isdigit():
            dir_choice = int(choice) - 1
            contents = repo.get_contents(directory_path, ref=branch_name)
            return handle_directory_choice(contents, dir_choice, previous_interactions, conversation_log, response_cache, repo, branch_name)
        elif choice.lower() == 'a':
            selected_directories.append(directory_path)
            cprint(f"Marked '{directory_path}' for capture.", 'yellow')
        elif choice.lower() == 'b':
            capture_selected_directories(selected_directories)
            return None, previous_interactions
        elif choice.lower() == 'c':
            return None, previous_interactions
        elif choice.lower() == 'd':
            return directory_path, process_user_prompt(previous_interactions, conversation_log)
        elif choice.lower() == 'e':
            return analyze_directory_choice(repo, branch_name, directory_path, previous_interactions, conversation_log, response_cache)
        elif choice.lower() == 'f':
            new_branch = switch_branch(repo)
            return new_branch if new_branch else branch_name, previous_interactions
        elif choice.lower() == 'u':
            return navigate_up(directory_path), previous_interactions
        else:
            cprint("Invalid choice. Please enter a valid input.", 'red')
    except Exception as e:
        cprint(f"Error in execute_choice: {e}", 'red')
        traceback.print_exc()
    return directory_path, previous_interactions

def navigation_menu(repo, conversation_log):
    """Main function to navigate the GitHub repository."""
    branch_name = repo.default_branch
    directory_path = ""
    selected_directories = []
    previous_interactions = []

    check_cache()

    while True:
        try:
            contents = repo.get_contents(directory_path, ref=branch_name)
            cprint(f"\nCurrent Branch: {branch_name}", 'yellow')
            cprint(f"Current Directory: {directory_path}\n", 'yellow')
            cprint("Marked Folders for Analysis:", 'yellow')
            for folder in selected_directories:
                cprint(f"- {folder}", 'yellow')
            print()
            
            for i, content in enumerate(contents):
                if content.type == "dir":
                    cprint(f"{i + 1}. Directory: {content.path}", 'yellow')
                elif content.type == "file":
                    lines_of_code = estimate_code_size(repo, content.path, branch_name)
                    cprint(f"{i + 1}. File: {content.path} - Lines of Code: {lines_of_code}", 'yellow')

            display_navigation_menu()
            choice = input("Enter your choice (number to navigate, letter for menu): ")
            
            if choice.lower() == 'c':
                break
            if choice.lower() == 'f':
                branch_name, previous_interactions = execute_choice(choice, repo, branch_name, directory_path, selected_directories, conversation_log, previous_interactions)
                directory_path = ""
            else:
                directory_path, previous_interactions = execute_choice(choice, repo, branch_name, directory_path, selected_directories, conversation_log, previous_interactions)
            
        except Exception as e:
            cprint(f"Error in navigation_menu: {e}", 'red')
            traceback.print_exc()
