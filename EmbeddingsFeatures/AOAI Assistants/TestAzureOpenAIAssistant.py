import unittest
from unittest.mock import patch, MagicMock
from openai import AzureOpenAI
from AzureOpenAIAssistant import AzureOpenAIAssistant
#import AzureOpenAIAssistant

class TestAzureOpenAIAssistant(unittest.TestCase):

    @patch('AzureOpenAIAssistant.AzureOpenAI')  # Mock AzureOpenAI
    @patch('AzureOpenAIAssistant.get_bearer_token_provider')  # Mock get_bearer_token_provider
    @patch('AzureOpenAIAssistant.ManagedIdentityCredential')  # Mock ManagedIdentityCredential
    def setUp(self, MockManagedIdentityCredential, MockGetBearerTokenProvider, MockAzureOpenAI):
        # Mock the token provider and client
        self.mock_token_provider = MockGetBearerTokenProvider
        self.mock_client = MockAzureOpenAI.return_value
        self.mock_credential = MockManagedIdentityCredential
        self.assistant = AzureOpenAIAssistant(name="TestAssistant", instructions="Test Instructions", model="TestModel")

    def test_create_client(self): 
        self.mock_credential.assert_called_once()
        self.mock_token_provider.assert_called_once_with(self.mock_credential.return_value, "https://cognitiveservices.azure.com/.default")
        self.assertIsNotNone(self.assistant.client)

    def test_create_assistant(self):
        self.mock_client.beta.assistants.create.return_value = MagicMock()
        self.assertIsNotNone(self.assistant.assistant)

    def test_create_thread(self):
        self.mock_client.beta.threads.create.return_value = MagicMock()
        self.assertIsNotNone(self.assistant.thread)

    def test_create_run(self):
        self.mock_client.beta.threads.runs.create.return_value = MagicMock()
        run = self.assistant.create_run()
        self.assertIsNotNone(run)

    def test_get_run_status(self):
        self.mock_client.beta.threads.runs.retrieve.return_value.status = "completed"
        run = self.assistant.get_run_status("test-run-id")
        self.assertEqual(run.status, "completed")

    def test_print_thread_messages(self):
        self.mock_client.beta.threads.messages.list.return_value.model_dump_json.return_value = '{"messages": []}'
        messages = self.assistant.print_thread_messages()
        self.assertEqual(messages, '{"messages": []}')

    def test_print_assistant(self):
        self.assistant.assistant.model_dump_json.return_value = '{"assistant": {}}'
        assistant_info = self.assistant.print_assistant()
        self.assertEqual(assistant_info, '{"assistant": {}}')

    @patch('time.sleep', return_value=None)
    @patch.object(AzureOpenAIAssistant, 'get_run_status', side_effect=[MagicMock(status="running"), MagicMock(status="completed")])
    def test_wait_run_completion(self, mock_get_run_status, _):
        run = self.assistant.wait_run_completion("test-run-id")
        self.assertEqual(run.status, "completed")

    def test_add_message_to_thread(self):
        self.mock_client.beta.threads.messages.create.return_value = MagicMock()
        message = self.assistant.add_message_to_thread("Test message")
        self.assertIsNotNone(message)

    def test_get_latest_response(self):
        self.mock_client.beta.threads.messages.list.return_value.model_dump_json.return_value = '{"data": [{"content": [{"text": {"value": "Test response"}}]}]}'
        response = self.assistant.get_latest_response()
        self.assertEqual(response, "Test response")

    @patch('AzureOpenAIAssistant.AzureOpenAIAssistant.create_run')
    @patch('AzureOpenAIAssistant.AzureOpenAIAssistant.wait_run_completion')
    @patch('AzureOpenAIAssistant.AzureOpenAIAssistant.get_latest_response')
    def test_message_and_receive_response(self, mock_get_latest_response, mock_wait_run_completion, mock_create_run):
        mock_create_run.return_value.id = "test-run-id"
        mock_wait_run_completion.return_value = "completed"
        mock_get_latest_response.return_value = "Test response"
        response = self.assistant.message_and_receive_response("Test message")
        self.assertEqual(response, "Test response")

if __name__ == '__main__':
    unittest.main()