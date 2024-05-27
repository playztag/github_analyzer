# test_menu.py
import unittest
from unittest.mock import patch, MagicMock
from utils.menu import execute_choice

class TestMenuModule(unittest.TestCase):

    @patch('utils.menu.summarize_directory')
    @patch('utils.menu.summarize_file')
    @patch('utils.menu.switch_branch')
    @patch('utils.menu.navigate_up')
    def test_execute_choice(self, mock_navigate_up, mock_switch_branch, mock_summarize_file, mock_summarize_directory):
        mock_repo = MagicMock()
        mock_dir_contents = [MagicMock(type="file", path="README.md"), MagicMock(type="dir", path="src")]
        mock_file_contents = MagicMock(decoded_content=b"print('Hello, World!')")

        def mock_get_contents(path, ref):
            if path == "":
                return mock_dir_contents
            elif path == "README.md":
                return mock_file_contents
            elif path == "src":
                return []
            return []

        mock_repo.get_contents.side_effect = mock_get_contents
        mock_summarize_directory.return_value = ("Summary", [], 100)
        mock_summarize_file.return_value = ("File Summary", [], 50)

        conversation_log = "conversation_log.txt"
        previous_interactions = []
        cached_contents = {"": mock_dir_contents}
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

    @patch('utils.menu.summarize_directory')
    @patch('utils.menu.summarize_file')
    @patch('utils.menu.switch_branch')
    @patch('utils.menu.navigate_up')
    def test_execute_choice_errors(self, mock_navigate_up, mock_switch_branch, mock_summarize_file, mock_summarize_directory):
        mock_repo = MagicMock()
        mock_repo.get_contents.side_effect = Exception("API error")

        conversation_log = "conversation_log.txt"
        previous_interactions = []
        cached_contents = {}
        summary_cache = {}

        directory_path, interactions, valid_navigation = execute_choice(
            "1", mock_repo, "main", "", [], conversation_log, previous_interactions, cached_contents, summary_cache
        )
        self.assertFalse(valid_navigation)
        self.assertEqual(directory_path, "")

    @patch('utils.menu.summarize_directory')
    @patch('utils.menu.summarize_file')
    @patch('utils.menu.switch_branch')
    @patch('utils.menu.navigate_up')
    def test_execute_choice_invalid_choice(self, mock_navigate_up, mock_switch_branch, mock_summarize_file, mock_summarize_directory):
        mock_repo = MagicMock()
        mock_dir_contents = [MagicMock(type="file", path="README.md"), MagicMock(type="dir", path="src")]

        def mock_get_contents(path, ref):
            if path == "":
                return mock_dir_contents
            return []

        mock_repo.get_contents.side_effect = mock_get_contents
        mock_summarize_directory.return_value = ("Summary", [], 100)
        mock_summarize_file.return_value = ("File Summary", [], 50)

        conversation_log = "conversation_log.txt"
        previous_interactions = []
        cached_contents = {"": mock_dir_contents}
        summary_cache = {}

        # Test invalid numeric choice
        directory_path, interactions, valid_navigation = execute_choice(
            "10", mock_repo, "main", "", [], conversation_log, previous_interactions, cached_contents, summary_cache
        )
        self.assertFalse(valid_navigation)
        self.assertEqual(directory_path, "")

        # Test invalid letter choice
        directory_path, interactions, valid_navigation = execute_choice(
            "z", mock_repo, "main", "", [], conversation_log, previous_interactions, cached_contents, summary_cache
        )
        self.assertFalse(valid_navigation)
        self.assertEqual(directory_path, "")

if __name__ == "__main__":
    unittest.main()
