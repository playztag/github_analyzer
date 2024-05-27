import os
import traceback

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
        "from project_utils.menu": "from utils.menu"
    },
    "utils/cache_utils.py": {
        "from project_utils.constants": "from utils.constants",
        "from project_utils.cache_utils": "from utils.cache_utils"
    },
    "utils/menu.py": {
        "from project_utils.navigation_utils": "from utils.navigation_utils",
        "from project_utils.cache_utils": "from utils.cache_utils",
        "from project_utils.directory_utils": "from utils.directory_utils",
        "from project_utils.interaction_utils": "from utils.interaction_utils",
        "from project_utils.file_utils": "from utils.file_utils",
        "from project_utils.utils": "from utils.utils"
    }
}

# List of remaining files to update
remaining_files = ["main.py", "utils/cache_utils.py", "utils/menu.py"]

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
