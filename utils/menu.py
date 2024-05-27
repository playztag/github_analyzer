from termcolor import cprint
from utils.navigation_utils import display_navigation_menu, switch_branch, navigate_up
from utils.cache_utils import check_cache, response_cache
from utils.directory_utils import analyze_directory_choice
from utils.interaction_utils import process_user_prompt
from utils.file_utils import analyze_file_choice
from utils.utils import handle_directory_choice, capture_selected_directories, display_contents, mark_item, display_marked_items
from core.github_utils import estimate_code_size
from core.summarize import summarize_directory, summarize_file
from utils.log_utils import log_conversation
import traceback

def execute_choice(choice, repo, branch_name, directory_path, selected_directories, conversation_log, previous_interactions, cached_contents, summary_cache):
    """Execute user choice from the navigation menu."""
    try:
        if directory_path in cached_contents:
            contents = cached_contents[directory_path]
        else:
            contents = repo.get_contents(directory_path, ref=branch_name)
            cached_contents[directory_path] = contents

        directories, files = display_contents(contents, repo, branch_name)

        if choice.isdigit():
            dir_choice = int(choice) - 1
            if dir_choice < len(directories):
                new_path = directories[dir_choice].path
                new_contents = repo.get_contents(new_path, ref=branch_name)
                cached_contents[new_path] = new_contents
                summary, previous_interactions, tokens_used = summarize_directory(repo, new_path, new_contents, previous_interactions, summary_cache)
                cprint(summary, 'yellow')
                log_conversation(f"Directory: {new_path}", summary, conversation_log)
                return new_path, previous_interactions
            elif dir_choice < len(directories) + len(files):
                file_choice = dir_choice - len(directories)
                file_path = files[file_choice].path
                file_content = repo.get_contents(file_path, ref=branch_name).decoded_content.decode('utf-8')
                summary, previous_interactions, tokens_used = summarize_file(repo, file_path, file_content, previous_interactions, summary_cache)
                cprint(summary, 'yellow')
                log_conversation(f"File: {file_path}", summary, conversation_log)
                return file_path, previous_interactions
            else:
                cprint("Invalid choice. Please select a valid item.", 'red')
                return directory_path, previous_interactions
        elif choice.lower() == 'a':
            mark_item(directory_path)
            cprint(f"Marked '{directory_path}' for capture.", 'yellow')
        elif choice.lower() == 'b':
            capture_selected_directories(selected_directories)
            return directory_path, previous_interactions
        elif choice.lower() == 'c':
            return None, previous_interactions
        elif choice.lower() == 'd':
            return directory_path, process_user_prompt(previous_interactions, conversation_log)
        elif choice.lower() == 'e':
            summary, previous_interactions, tokens_used = summarize_directory(repo, directory_path, contents, previous_interactions, summary_cache)
            cprint(summary, 'yellow')
            log_conversation(f"Directory: {directory_path}", summary, conversation_log)
            return directory_path, previous_interactions
        elif choice.lower() == 'f':
            new_branch = switch_branch(repo)
            return new_branch if new_branch else branch_name, previous_interactions
        elif choice.lower() == 'u':
            new_path = navigate_up(directory_path)
            if new_path in cached_contents:
                contents = cached_contents[new_path]
            else:
                contents = repo.get_contents(new_path, ref=branch_name)
                cached_contents[new_path] = contents
            cprint(f"Navigated up to {new_path}", 'yellow')
            return new_path, previous_interactions
        else:
            cprint("Invalid choice. Please enter a valid input.", 'red')
    except Exception as e:
        cprint(f"Error in execute_choice: {e}", 'red')
        traceback.print_exc()
    return directory_path, previous_interactions

def navigation_menu(repo, conversation_log, root_contents):
    """Main function to navigate the GitHub repository."""
    branch_name = repo.default_branch  # Use repo.default_branch directly
    directory_path = ""
    selected_directories = []
    previous_interactions = []

    check_cache()

    # Cache for storing directory contents and summaries
    cached_contents = {"": root_contents}
    summary_cache = {}

    while True:
        try:
            contents = cached_contents.get(directory_path, [])
            cprint(f"\nCurrent Branch: {branch_name}", 'yellow')
            cprint(f"Current Directory: {directory_path or 'default'}\n", 'yellow')
            
            display_marked_items()
            directories, files = display_contents(contents, repo, branch_name)
            display_navigation_menu()
            choice = input("Enter your choice (number to navigate, letter for menu): ")
            
            directory_path, previous_interactions = execute_choice(choice, repo, branch_name, directory_path, selected_directories, conversation_log, previous_interactions, cached_contents, summary_cache)
            
        except Exception as e:
            cprint(f"Error in navigation_menu: {e}", 'red')
            traceback.print_exc()
            break  # Exit the loop on error
