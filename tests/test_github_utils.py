# test_github_utils.py
import unittest
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

    @patch('core.github_utils.generate_ai_response')
    @patch('core.github_utils.estimate_code_size')
    def test_analyze_empty_directory(self, mock_estimate_code_size, mock_generate_ai_response):
        mock_repo = MagicMock()
        mock_estimate_code_size.return_value = 0
        mock_generate_ai_response.return_value = ("Empty directory analysis", [], 50)

        previous_interactions = []
        analysis, interactions, tokens = analyze_directory(mock_repo, "main", "empty_dir", previous_interactions)
        self.assertEqual(analysis, "Empty directory analysis")
        self.assertEqual(interactions, previous_interactions)
        self.assertEqual(tokens, 50)

    @patch('core.github_utils.generate_ai_response')
    def test_analyze_non_utf8_file(self, mock_generate_ai_response):
        mock_repo = MagicMock()
        mock_file_content = "print('Hello, World!')".encode('latin-1')
        mock_repo.get_contents.return_value = MagicMock(decoded_content=mock_file_content)
        mock_generate_ai_response.return_value = ("Non-UTF-8 file analysis", [], 150)

        previous_interactions = []
        analysis, interactions, tokens = analyze_file(mock_repo, "main", "non_utf8.py", previous_interactions)
        self.assertEqual(analysis, "Non-UTF-8 file analysis")
        self.assertEqual(interactions, previous_interactions)
        self.assertEqual(tokens, 150)

if __name__ == "__main__":
    unittest.main()
