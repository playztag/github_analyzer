from termcolor import cprint
from utils.navigation_utils import display_navigation_menu, switch_branch, navigate_up
from utils.cache_utils import check_cache, response_cache
from utils.directory_utils import analyze_directory_choice
from utils.interaction_utils import process_user_prompt
from utils.file_utils import analyze_file_choice
from utils.utils import handle_directory_choice, capture_selected_directories, display_contents, mark_item, display_marked_items, bookmark_item, display_bookmarked_items
from core.github_utils import estimate_code_size
from core.summarize import summarize_directory, summarize_file
from utils.log_utils import log_conversation
import traceback

def execute_choice(choice, repo, branch_name, directory_path, selected_directories, conversation_log, previous_interactions, cached_contents, summary_cache):
    print(f"DEBUG: execute_choice called with choice: {choice}")
    try:
        if directory_path in cached_contents:
            contents = cached_contents[directory_path]
        else:
            contents = repo.get_contents(directory_path, ref=branch_name)
            cached_contents[directory_path] = contents

        directories = [content for content in contents if content.type == "dir"]
        files = [content for content in contents if content.type == "file"]

        if choice.isdigit():
            print(f"DEBUG: Handling numeric choice: {choice}")
            dir_choice = int(choice) - 1
            if dir_choice < len(directories):
                new_path = directories[dir_choice].path
                new_contents = repo.get_contents(new_path, ref=branch_name)
                cached_contents[new_path] = new_contents
                summary, previous_interactions, tokens_used = summarize_directory(repo, new_path, new_contents, previous_interactions, summary_cache)
                cprint(summary, 'yellow')
                log_conversation(f"Directory: {new_path}", summary, conversation_log)
                return new_path, previous_interactions, True
            elif dir_choice < len(directories) + len(files):
                file_choice = dir_choice - len(directories)
                file_path = files[file_choice].path
                file_content = repo.get_contents(file_path, ref=branch_name).decoded_content.decode('utf-8')
                summary, previous_interactions, tokens_used = summarize_file(repo, file_path, file_content, previous_interactions, summary_cache)
                cprint(summary, 'yellow')
                log_conversation(f"File: {file_path}", summary, conversation_log)
                return file_path, previous_interactions, True
            else:
                cprint("Invalid choice. Please select a valid item.", 'red')
                return directory_path, previous_interactions, False
        elif choice.lower() == 'a':
            print(f"DEBUG: Handling choice 'a'")
            mark_item(directory_path)
            cprint(f"Marked '{directory_path}' for capture.", 'yellow')
            return directory_path, previous_interactions, False
        elif choice.lower() == 'b':
            print(f"DEBUG: Handling choice 'b'")
            capture_selected_directories(selected_directories)
            return directory_path, previous_interactions, False
        elif choice.lower() == 'c':
            print(f"DEBUG: Handling choice 'c'")
            return None, previous_interactions, False
        elif choice.lower() == 'd':
            print(f"DEBUG: Handling choice 'd'")
            return directory_path, process_user_prompt(previous_interactions, conversation_log), False
        elif choice.lower() == 'e':
            print(f"DEBUG: Handling choice 'e'")
            summary, previous_interactions, tokens_used = summarize_directory(repo, directory_path, contents, previous_interactions, summary_cache)
            cprint(summary, 'yellow')
            log_conversation(f"Directory: {directory_path}", summary, conversation_log)
            return directory_path, previous_interactions, False
        elif choice.lower() == 'f':
            print(f"DEBUG: Handling choice 'f'")
            new_branch = switch_branch(repo)
            return new_branch if new_branch else branch_name, previous_interactions, False
        elif choice.lower() == 'g':
            print(f"DEBUG: Handling choice 'g'")
            # Return to last AI-analyzed directory/file
            # TODO: Implement this functionality
            cprint("Feature not implemented yet.", 'red')
            return directory_path, previous_interactions, False
        elif choice.lower() == 'h':
            print(f"DEBUG: Handling choice 'h'")
            # List current directory contents without AI summary
            display_contents(contents, repo, branch_name)
            return directory_path, previous_interactions, False
        elif choice.lower() == 'i':
            print(f"DEBUG: Handling choice 'i'")
            bookmark_item(directory_path)
            return directory_path, previous_interactions, False
        elif choice.lower() == 'u':
            print(f"DEBUG: Handling choice 'u'")
            new_path = navigate_up(directory_path)
            if new_path in cached_contents:
                contents = cached_contents[new_path]
            else:
                contents = repo.get_contents(new_path, ref=branch_name)
                cached_contents[new_path] = contents
            cprint(f"Navigated up to {new_path}", 'yellow')
            return new_path, previous_interactions, True
        else:
            cprint("Invalid choice. Please enter a valid input.", 'red')
            return directory_path, previous_interactions, False
    except Exception as e:
        cprint(f"Error in execute_choice: {e}", 'red')
        traceback.print_exc()
        return directory_path, previous_interactions, False

def navigation_menu(repo, conversation_log, root_contents):
    """Main function to navigate the GitHub repository."""
    branch_name = repo.default_branch
    directory_path = ""
    selected_directories = []
    previous_interactions = []

    check_cache()

    # Cache for storing directory contents and summaries
    cached_contents = {"": root_contents}
    summary_cache = {}

    while True:
        try:
            if directory_path in cached_contents:
                contents = cached_contents[directory_path]
            else:
                contents = repo.get_contents(directory_path, ref=branch_name)
                cached_contents[directory_path] = contents

            if contents:
                cprint(f"\nCurrent Branch: {branch_name}", 'yellow')
                cprint(f"Current Directory: {directory_path or 'default'}\n", 'yellow')
                display_marked_items()
                display_bookmarked_items()
                directories, files = display_contents(contents, repo, branch_name)

            display_navigation_menu()
            choice = input("Enter your choice (number to navigate, letter for menu): ")

            if choice.lower() == 'c':
                cprint("Exiting...", 'cyan')
                break
            
            print(f"DEBUG: Before execute_choice, directory_path: {directory_path}")
            directory_path, previous_interactions, valid_navigation = execute_choice(
                choice, repo, branch_name, directory_path, selected_directories, conversation_log, previous_interactions, cached_contents, summary_cache
            )
            print(f"DEBUG: After execute_choice, directory_path: {directory_path}")
            
            if not valid_navigation:
                continue
            
        except Exception as e:
            cprint(f"Error in navigation_menu: {e}", 'red')
            traceback.print_exc()
            break

def display_navigation_menu():
    """Display navigation menu options."""
    cprint("\nNavigation Menu:", 'cyan', attrs=['bold'])
    cprint("a. Mark current directory for capture", 'cyan')
    cprint("b. Capture all selected directories", 'cyan')
    cprint("c. Exit", 'cyan')
    cprint("d. Enter a prompt for AI assistance", 'cyan')
    cprint("e. Analyze current directory with AI", 'cyan')
    cprint("f. Change branch", 'cyan')
    cprint("g. Return to last AI-analyzed directory/file", 'cyan')
    cprint("h. List current directory contents", 'cyan')
    cprint("i. Bookmark current directory/file", 'cyan')
    cprint("u. Navigate up to previous directory", 'cyan')
    print()
