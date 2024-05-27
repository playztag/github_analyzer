# GitHub Repository Analysis Tool

This tool is designed to provide a detailed analysis of any GitHub repository. It utilizes OpenAI's GPT-4 and the GitHub API to summarize README files, analyze repository structures, and offer interactive navigation through the repository contents.

## Features

- **Summarize README and Repository Structure:** Automatically generate concise summaries of README files and repository structures.
- **Interactive Navigation:** Navigate through the repository's directories and files interactively.
- **AI-Powered Insights:** Utilize OpenAI's GPT-4 to gain insights into code functionalities and structures.
- **Conversation Logging:** Log interactions and conversations for future reference.
- **Import Statements Update:** Automatically update import statements in the project's files based on predefined mappings.

## Installation

### Prerequisites

- Python 3.8+
- Git
- [GitHub Personal Access Token](https://github.com/settings/tokens)
- [OpenAI API Key](https://beta.openai.com/signup/)
- [pip](https://pip.pypa.io/en/stable/installation/)

### Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/yourrepository.git
    cd yourrepository
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up your environment variables by creating a `.env` file in the project root directory with the following contents:
    ```
    OPENAI_API_KEY=your_openai_api_key
    GITHUB_TOKEN=your_github_access_token
    ```

## Usage

1. **Run the main script:**
    ```sh
    python main.py
    ```

    This will start the repository analysis, summarizing the README and repository structure, and providing an interactive navigation menu.

### Command Line Options

- **Analyze specific repository:**
    Edit the `repo_url` variable in `main.py` to point to the desired GitHub repository.

- **Conversation Log:**
    The conversations and interactions are logged in `conversation_log.txt`.

## Project Structure

```
.
├── main.py                    # Main script to start the repository analysis
├── prompts.py                 # Prompts used for AI interactions
├── update.py                  # Script to update import statements
├── config/
│   └── config.py              # Configuration and environment setup
├── core/
│   ├── ai_utils.py            # Utility functions for AI interactions
│   ├── github_utils.py        # GitHub utility functions
│   ├── protected_openai_call.py # Functions to handle protected OpenAI API calls
│   └── summarize.py           # Functions to summarize README and repository structure
├── utils/
│   ├── cache_utils.py         # Cache management utilities
│   ├── constants.py           # Constant values used in the project
│   ├── directory_utils.py     # Functions to analyze directories
│   ├── file_utils.py          # Functions to analyze files
│   ├── interaction_utils.py   # Functions to process user interactions
│   ├── log_utils.py           # Logging utilities
│   ├── menu.py                # Interactive navigation menu
│   └── utils.py               # General utility functions
└── requirements.txt           # Required packages
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.