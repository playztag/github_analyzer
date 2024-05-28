from core.ai_utils import generate_ai_response
import traceback

def estimate_code_size(repo, path, ref):
    try:
        file_contents = repo.get_contents(path, ref=ref).decoded_content.decode('utf-8')
        lines_of_code = file_contents.count('\n') + 1
        return lines_of_code
    except Exception as e:
        print(f"Error in estimate_code_size: {e}")
        traceback.print_exc()
        return 0

def analyze_directory(repo, branch_name, directory_path, previous_interactions):
    try:
        contents = repo.get_contents(directory_path, ref=branch_name)
        
        directory_structure = ""
        for content in contents:
            if content.type == "dir":
                directory_structure += f"Directory: {content.path}\n"
            elif content.type == "file":
                lines_of_code = estimate_code_size(repo, content.path, branch_name)
                directory_structure += f"File: {content.path} - Lines of Code: {lines_of_code}\n"
        
        prompt = f"""
        You are analyzing a GitHub repository directory. The current directory is '{directory_path}' on branch '{branch_name}'.
        The directory contains the following structure:
        {directory_structure}
        
        Please provide a one-paragraph summary of the important aspects of this directory and the files within it.
        """
        
        system_prompt = "You are a helpful assistant with expertise in software engineering and GitHub repository analysis."
        return generate_ai_response(system_prompt, prompt, previous_interactions)
    except Exception as e:
        print(f"Error in analyze_directory: {e}")
        traceback.print_exc()
        return f"Error in analyze_directory: {e}", previous_interactions

def analyze_file(repo, branch_name, file_path, previous_interactions):
    try:
        file_contents = repo.get_contents(file_path, ref=branch_name).decoded_content.decode('utf-8')
        lines_of_code = file_contents.count('\n') + 1
        
        # Add file content to context manager
        context_manager.add_file_content(file_path, file_contents)
        context_manager.add_interaction(f"Analyzed File: {file_path}\nContent: {file_contents[:1000]}")
        
        # Ensure the file content is fully included in the prompt
        prompt = f"""
        You are analyzing a GitHub repository file. The current file is '{file_path}' on branch '{branch_name}'.
        The file contains the following contents:
        {file_contents}
        
        Please provide a one-paragraph summary of the important aspects of this file, its functionalities, and any notable code structures. 
        """
        
        system_prompt = "You are a helpful assistant with expertise in software engineering and GitHub repository analysis."
        return generate_ai_response(system_prompt, prompt, previous_interactions)
    except Exception as e:
        print(f"Error in analyze_file: {e}")
        traceback.print_exc()
        return f"Error in analyze_file: {e}", previous_interactions
