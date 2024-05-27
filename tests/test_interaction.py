from unittest.mock import patch, MagicMock
import unittest

# Correct import path based on actual structure
from utils.menu import execute_choice

class TestNavigationMenuIntegration(unittest.TestCase):
    @patch('utils.menu.repo.get_contents', new_callable=MagicMock)
    @patch('utils.menu.summarize_directory')
    def test_analyze_current_directory_with_ai(self, mock_summarize_directory, mock_get_contents):
        mock_get_contents.return_value = [MagicMock(type="dir", path="src"), MagicMock(type="file", path="README.md")]
        mock_summarize_directory.return_value = ("summary", [], 0)

        print("DEBUG: Running test_analyze_current_directory_with_ai")
        directory_path, previous_interactions, valid_navigation = execute_choice("e", MagicMock(), "master", "", [], [], {}, {})
        print(f"DEBUG: After execute_choice - directory_path: {directory_path}, valid_navigation: {valid_navigation}")
        mock_summarize_directory.assert_called_once()
        self.assertTrue(valid_navigation)

    @patch('utils.menu.repo.get_contents', new_callable=MagicMock)
    @patch('utils.menu.switch_branch')
    def test_change_branch(self, mock_switch_branch, mock_get_contents):
        mock_get_contents.return_value = [MagicMock(type="dir", path="src"), MagicMock(type="file", path="README.md")]
        mock_switch_branch.return_value = "new_branch"

        print("DEBUG: Running test_change_branch")
        directory_path, previous_interactions, valid_navigation = execute_choice("f", MagicMock(), "master", "", [], [], {}, {})
        print(f"DEBUG: After execute_choice - directory_path: {directory_path}, valid_navigation: {valid_navigation}")
        self.assertEqual(directory_path, "new_branch")
        self.assertTrue(valid_navigation)

    @patch('utils.menu.repo.get_contents', new_callable=MagicMock)
    @patch('utils.menu.generate_ai_response')
    def test_enter_prompt_for_ai_assistance(self, mock_generate_ai_response, mock_get_contents):
        mock_get_contents.return_value = [MagicMock(type="dir", path="src"), MagicMock(type="file", path="README.md")]
        mock_generate_ai_response.return_value = "AI response"

        print("DEBUG: Running test_enter_prompt_for_ai_assistance")
        directory_path, previous_interactions, valid_navigation = execute_choice("d", MagicMock(), "master", "", [], [], {}, {})
        print(f"DEBUG: After execute_choice - directory_path: {directory_path}, valid_navigation: {valid_navigation}")
        mock_generate_ai_response.assert_called_once()
        self.assertTrue(valid_navigation)

    @patch('utils.menu.repo.get_contents', new_callable=MagicMock)
    def test_return_to_last_ai_analyzed_directory_file(self, mock_get_contents):
        mock_get_contents.return_value = [MagicMock(type="dir", path="src"), MagicMock(type="file", path="README.md")]

        print("DEBUG: Running test_return_to_last_ai_analyzed_directory_file")
        directory_path, previous_interactions, valid_navigation = execute_choice("g", MagicMock(), "master", "", [], [], {}, {})
        print(f"DEBUG: After execute_choice - directory_path: {directory_path}, valid_navigation: {valid_navigation}")
        self.assertTrue(valid_navigation)

    @patch('utils.menu.repo.get_contents', new_callable=MagicMock)
    def test_bookmark_current_directory_file(self, mock_get_contents):
        mock_get_contents.return_value = [MagicMock(type="dir", path="src"), MagicMock(type="file", path="README.md")]

        print("DEBUG: Running test_bookmark_current_directory_file")
        directory_path, previous_interactions, valid_navigation = execute_choice("i", MagicMock(), "master", "", [], [], {}, {})
        print(f"DEBUG: After execute_choice - directory_path: {directory_path}, valid_navigation: {valid_navigation}")
        self.assertTrue(valid_navigation)

    @patch('utils.menu.repo.get_contents', new_callable=MagicMock)
    def test_mark_current_directory_for_capture(self, mock_get_contents):
        mock_get_contents.return_value = [MagicMock(type="dir", path="src"), MagicMock(type="file", path="README.md")]

        print("DEBUG: Running test_mark_current_directory_for_capture")
        directory_path, previous_interactions, valid_navigation = execute_choice("a", MagicMock(), "master", "", [], [], {}, {})
        print(f"DEBUG: After execute_choice - directory_path: {directory_path}, valid_navigation: {valid_navigation}")
        self.assertTrue(valid_navigation)

    @patch('utils.menu.repo.get_contents', new_callable=MagicMock)
    def test_capture_all_selected_directories(self, mock_get_contents):
        mock_get_contents.return_value = [MagicMock(type="dir", path="src"), MagicMock(type="file", path="README.md")]

        print("DEBUG: Running test_capture_all_selected_directories")
        directory_path, previous_interactions, valid_navigation = execute_choice("b", MagicMock(), "master", "", [], [], {}, {})
        print(f"DEBUG: After execute_choice - directory_path: {directory_path}, valid_navigation: {valid_navigation}")
        self.assertTrue(valid_navigation)

    @patch('utils.menu.repo.get_contents', new_callable=MagicMock)
    def test_list_current_directory_contents(self, mock_get_contents):
        mock_get_contents.return_value = [MagicMock(type="dir", path="src"), MagicMock(type="file", path="README.md")]

        print("DEBUG: Running test_list_current_directory_contents")
        directory_path, previous_interactions, valid_navigation = execute_choice("h", MagicMock(), "master", "", [], [], {}, {})
        print(f"DEBUG: After execute_choice - directory_path: {directory_path}, valid_navigation: {valid_navigation}")
        self.assertTrue(valid_navigation)

    @patch('utils.menu.repo.get_contents', new_callable=MagicMock)
    def test_navigate_up_to_previous_directory(self, mock_get_contents):
        mock_get_contents.return_value = [MagicMock(type="dir", path="src"), MagicMock(type="file", path="README.md")]

        print("DEBUG: Running test_navigate_up_to_previous_directory")
        directory_path, previous_interactions, valid_navigation = execute_choice("u", MagicMock(), "master", "src", [], [], {}, {})
        print(f"DEBUG: After execute_choice - directory_path: {directory_path}, valid_navigation: {valid_navigation}")
        self.assertTrue(valid_navigation)

    @patch('utils.menu.repo.get_contents', new_callable=MagicMock)
    def test_exit(self, mock_get_contents):
        mock_get_contents.return_value = [MagicMock(type="dir", path="src"), MagicMock(type="file", path="README.md")]

        print("DEBUG: Running test_exit")
        directory_path, previous_interactions, valid_navigation = execute_choice("c", MagicMock(), "master", "", [], [], {}, {})
        print(f"DEBUG: After execute_choice - directory_path: {directory_path}, valid_navigation: {valid_navigation}")
        self.assertTrue(valid_navigation)

if __name__ == "__main__":
    unittest.main()

