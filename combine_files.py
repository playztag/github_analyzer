import os

# Define the output file
output_file = 'combined_source_code.txt'

# Define file extensions to include
include_extensions = {'.py', '.md'}

# Function to check if a file should be included based on its extension
def should_include_file(file_name):
    _, ext = os.path.splitext(file_name)
    return ext in include_extensions

# Function to gather ignore patterns from .gitignore
def get_gitignore_patterns(base_path):
    gitignore_path = os.path.join(base_path, '.gitignore')
    if not os.path.exists(gitignore_path):
        return []

    with open(gitignore_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    patterns = [line.strip() for line in lines if line.strip() and not line.startswith('#')]
    return patterns

# Function to check if a path should be excluded based on .gitignore patterns
def should_exclude_path(path, patterns):
    for pattern in patterns:
        if pattern.endswith('/'):
            if os.path.isdir(path) and path.endswith(pattern.rstrip('/')):
                return True
        elif os.path.isfile(path) and path.endswith(pattern):
            return True
    return False

# Function to check if a path is hidden
def is_hidden(path):
    return any(part.startswith('.') for part in path.split(os.sep))

# Function to gather the directory and file tree
def get_directory_tree(base_path, patterns):
    tree = []
    for root, dirs, files in os.walk(base_path):
        if should_exclude_path(root, patterns) or is_hidden(root):
            continue
        level = root.replace(base_path, '').count(os.sep)
        indent = ' ' * 4 * level
        tree.append(f"{indent}{os.path.basename(root)}/")
        sub_indent = ' ' * 4 * (level + 1)
        dirs[:] = [d for d in dirs if not should_exclude_path(os.path.join(root, d), patterns) and not is_hidden(d)]
        for file in files:
            if should_include_file(file) and not should_exclude_path(os.path.join(root, file), patterns) and not is_hidden(file):
                tree.append(f"{sub_indent}{file}")
    return tree

# Function to walk through the directory and gather file contents
def gather_files_content(base_path, patterns):
    contents = []
    total_lines = 0
    for root, dirs, files in os.walk(base_path):
        if should_exclude_path(root, patterns) or is_hidden(root):
            continue
        dirs[:] = [d for d in dirs if not should_exclude_path(os.path.join(root, d), patterns) and not is_hidden(d)]
        for file in files:
            if should_include_file(file) and not should_exclude_path(os.path.join(root, file), patterns) and not is_hidden(file):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, base_path)
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                contents.append(f"### {rel_path} ###\n{file_content}\n")
                total_lines += file_content.count('\n') + 1
    return contents, total_lines

def main():
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    # Get .gitignore patterns
    patterns = get_gitignore_patterns(base_path)
    
    # Get the directory tree
    directory_tree = get_directory_tree(base_path, patterns)
    
    # Gather file contents
    contents, total_lines = gather_files_content(base_path, patterns)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("Project Directory Tree:\n")
        f.write('\n'.join(directory_tree))
        f.write('\n\nTotal Lines: {}\n\n'.format(total_lines))
        f.write('='*80 + '\n')
        
        for content in contents:
            f.write(content)
            f.write('\n' + '='*80 + '\n')  # Delimiter between files

    print(f"Combined source code written to {output_file}")

if __name__ == "__main__":
    main()
