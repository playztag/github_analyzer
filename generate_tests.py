import os

# Define the test cases
test_cases = {
    "test_summarize.py": """import unittest
from unittest.mock import patch, MagicMock
from core.summarize import summarize_directory, summarize_file

class TestSummarizeModule(unittest.TestCase):

    @patch('core.summarize.generate_ai_response')
    def test_summarize_directory(self, mock_generate_ai_response):
        mock_repo = MagicMock()
        mock_contents = [MagicMock(type="file", path="README.md"), MagicMock(type="dir", path="src")]
        mock_generate_ai_response.return_value = ("Summary of directory", [], 100)

        summary_cache = {}
        summary, _, _ = summarize_directory(mock_repo, "", mock_contents, [], summary_cache)
        self.assertEqual(summary, "Summary of directory")
        self.assertIn("", summary_cache)

    @patch('core.summarize.generate_ai_response')
    def test_summarize_file(self, mock_generate_ai_response):
        mock_repo = MagicMock()
        mock_file_content = "print('Hello, World!')"
        mock_generate_ai_response.return_value = ("Summary of file", [], 50)

        summary_cache = {}
        summary, _, _ = summarize_file(mock_repo, "main.py", mock_file_content, [], summary_cache)
        self.assertEqual(summary, "Summary of file")
        self.assertIn("main.py", summary_cache)

if __name__ == "__main__":
    unittest.main()
""",
    "test_github_utils.py": """import unittest
from unittest.mock import patch, MagicMock
from core.github_utils import analyze_directory, analyze_file

class TestGithubUtilsModule(unittest.TestCase):

    @patch('core.github_utils.generate_ai_response')
    @patch('core.github_utils.estimate_code_size')
    def test_analyze_directory(self, mock_estimate_code_size, mock_generate_ai_response):
        mock_repo = MagicMock()
        mock_estimate_code_size.return_value = 100
        mock_generate_ai_response.return_value = ("Directory analysis", [], 200)

        previous_interactions = []
        analysis, interactions, tokens = analyze_directory(mock_repo, "main", "src", previous_interactions)
        self.assertEqual(analysis, "Directory analysis")
        self.assertEqual(interactions, previous_interactions)
        self.assertEqual(tokens, 200)

    @patch('core.github_utils.generate_ai_response')
    def test_analyze_file(self, mock_generate_ai_response):
        mock_repo = MagicMock()
        mock_file_content = "print('Hello, World!')"
        mock_repo.get_contents.return_value = MagicMock(decoded_content=mock_file_content.encode('utf-8'))
        mock_generate_ai_response.return_value = ("File analysis", [], 150)

        previous_interactions = []
        analysis, interactions, tokens = analyze_file(mock_repo, "main", "README.md", previous_interactions)
        self.assertEqual(analysis, "File analysis")
        self.assertEqual(interactions, previous_interactions)
        self.assertEqual(tokens, 150)

if __name__ == "__main__":
    unittest.main()
""",
    "test_ai_utils.py": """import unittest
from unittest.mock import patch
from core.ai_utils import generate_ai_response, count_tokens

class TestAIUtilsModule(unittest.TestCase):

    def test_count_tokens(self):
        text = "Hello, World!"
        tokens = count_tokens(text)
        self.assertIsInstance(tokens, int)
        self.assertGreater(tokens, 0)

    @patch('core.ai_utils.protected_openai_chat_completion')
    def test_generate_ai_response(self, mock_protected_openai_chat_completion):
        mock_protected_openai_chat_completion.return_value = MagicMock(choices=[MagicMock(message=MagicMock(content="AI response"))])
        system_prompt = "You are a helpful assistant."
        user_prompt = "Tell me a joke."
        response, messages, tokens = generate_ai_response(system_prompt, user_prompt)
        self.assertEqual(response, "AI response")
        self.assertIsInstance(messages, list)
        self.assertGreater(tokens, 0)

if __name__ == "__main__":
    unittest.main()
""",
    "test_menu.py": """import unittest
from unittest.mock import patch, MagicMock
from utils.menu import execute_choice

class TestMenuModule(unittest.TestCase):

    @patch('utils.menu.summarize_directory')
    @patch('utils.menu.summarize_file')
    @patch('utils.menu.switch_branch')
    @patch('utils.menu.navigate_up')
    def test_execute_choice(self, mock_navigate_up, mock_switch_branch, mock_summarize_file, mock_summarize_directory):
        mock_repo = MagicMock()
        mock_contents = [MagicMock(type="file", path="README.md"), MagicMock(type="dir", path="src")]
        mock_repo.get_contents.return_value = mock_contents
        mock_summarize_directory.return_value = ("Summary", [], 100)
        mock_summarize_file.return_value = ("File Summary", [], 50)

        conversation_log = "conversation_log.txt"
        previous_interactions = []
        cached_contents = {"": mock_contents}
        summary_cache = {}

        # Test directory choice
        directory_path, interactions, valid_navigation = execute_choice(
            "1", mock_repo, "main", "", [], conversation_log, previous_interactions, cached_contents, summary_cache
        )
        self.assertTrue(valid_navigation)
        self.assertEqual(directory_path, "src")

        # Test file choice
        directory_path, interactions, valid_navigation = execute_choice(
            "2", mock_repo, "main", "", [], conversation_log, previous_interactions, cached_contents, summary_cache
        )
        self.assertTrue(valid_navigation)
        self.assertEqual(directory_path, "README.md")

if __name__ == "__main__":
    unittest.main()
""",
    "test_utils.py": """import unittest
from unittest.mock import MagicMock
from utils.utils import mark_item, display_marked_items, bookmark_item, display_bookmarked_items

class TestUtilsModule(unittest.TestCase):

    def test_mark_item(self):
        path = "src"
        mark_item(path)
        self.assertTrue(marked_items[path])
        mark_item(path)
        self.assertFalse(marked_items[path])

    def test_bookmark_item(self):
        path = "src"
        bookmark_item(path)
        self.assertIn(path, bookmarked_items)
        bookmark_item(path)
        self.assertEqual(bookmarked_items.count(path), 1)

if __name__ == "__main__":
    unittest.main()
"""
}

# Create the tests directory if it doesn't exist
if not os.path.exists("tests"):
    os.makedirs("tests")

# Create each test file in the tests directory
for filename, content in test_cases.items():
    with open(os.path.join("tests", filename), "w") as f:
        f.write(content)

print("Test files created successfully.")
