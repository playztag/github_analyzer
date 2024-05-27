# test_summarize.py
import unittest
from unittest.mock import patch, MagicMock
from core.summarize import summarize_directory, summarize_file

class TestSummarizeModule(unittest.TestCase):

    @patch('core.summarize.generate_ai_response')
    def test_summarize_python_file(self, mock_generate_ai_response):
        mock_repo = MagicMock()
        mock_file_content = "def hello_world():\n    print('Hello, World!')"
        mock_generate_ai_response.return_value = ("Summary of Python file", [], 50)

        summary_cache = {}
        summary, _, _ = summarize_file(mock_repo, "hello.py", mock_file_content, [], summary_cache)
        self.assertEqual(summary, "Summary of Python file")
        self.assertIn("hello.py", summary_cache)

    @patch('core.summarize.generate_ai_response')
    def test_summarize_markdown_file(self, mock_generate_ai_response):
        mock_repo = MagicMock()
        mock_file_content = "# Title\nThis is a markdown file."
        mock_generate_ai_response.return_value = ("Summary of Markdown file", [], 50)

        summary_cache = {}
        summary, _, _ = summarize_file(mock_repo, "README.md", mock_file_content, [], summary_cache)
        self.assertEqual(summary, "Summary of Markdown file")
        self.assertIn("README.md", summary_cache)

    @patch('core.summarize.generate_ai_response')
    def test_summarize_javascript_file(self, mock_generate_ai_response):
        mock_repo = MagicMock()
        mock_file_content = "function helloWorld() {\n    console.log('Hello, World!');\n}"
        mock_generate_ai_response.return_value = ("Summary of JavaScript file", [], 50)

        summary_cache = {}
        summary, _, _ = summarize_file(mock_repo, "hello.js", mock_file_content, [], summary_cache)
        self.assertEqual(summary, "Summary of JavaScript file")
        self.assertIn("hello.js", summary_cache)

if __name__ == "__main__":
    unittest.main()
