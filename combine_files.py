import os

# Define the output file
output_file = 'combined_source_code.txt'

# Define file extensions to include
include_extensions = {'.py', '.md'}

# Define directories to exclude
exclude_dirs = {'__pycache__', 'env', 'venv', 'node_modules'}

# Function to check if a file should be included based on its extension
def should_include_file(file_name):
    _, ext = os.path.splitext(file_name)
    return ext in include_extensions

# Function to check if a directory should be excluded
def should_exclude_dir(dir_name):
    return dir_name in exclude_dirs

# Function to walk through the directory and gather file contents
def gather_files_content(base_path):
    contents = []
    for root, dirs, files in os.walk(base_path):
        # Exclude specific directories
        dirs[:] = [d for d in dirs if not should_exclude_dir(d)]
        for file in files:
            if file == 'combine_files.py':
                continue
            if should_include_file(file):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, base_path)
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                contents.append(f"### {rel_path} ###\n{file_content}\n")
    return contents

def main():
    base_path = os.path.dirname(os.path.abspath(__file__))
    contents = gather_files_content(base_path)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for content in contents:
            f.write(content)
            f.write('\n' + '='*80 + '\n')  # Delimiter between files

    print(f"Combined source code written to {output_file}")

if __name__ == "__main__":
    main()
