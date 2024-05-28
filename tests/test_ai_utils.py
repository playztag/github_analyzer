# test_ai_utils.py
import unittest
from unittest.mock import patch, MagicMock
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

    @patch('core.ai_utils.protected_openai_chat_completion')
    def test_generate_ai_response_error(self, mock_protected_openai_chat_completion):
        mock_protected_openai_chat_completion.side_effect = Exception("API error")
        system_prompt = "You are a helpful assistant."
        user_prompt = "Tell me a joke."
        response, messages, tokens = generate_ai_response(system_prompt, user_prompt)
        self.assertIn("Error in generate_ai_response", response)
        self.assertIsInstance(messages, list)
        self.assertGreater(tokens, 0)

if __name__ == "__main__":
    unittest.main()
