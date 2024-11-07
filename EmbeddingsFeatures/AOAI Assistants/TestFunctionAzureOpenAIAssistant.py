import unittest
from azure.identity import ManagedIdentityCredential
from AzureOpenAIAssistant import AzureOpenAIAssistant
from FunctionAzureOpenAIAssistant import FunctionAzureOpenAIAssistant
from unittest.mock import patch, MagicMock, PropertyMock

class TestFunctionAzureOpenAIAssistant(unittest.TestCase):

    @patch('AzureOpenAIAssistant.AzureOpenAI')  # Mock AzureOpenAI
    @patch('AzureOpenAIAssistant.get_bearer_token_provider')  # Mock get_bearer_token_provider
    @patch('AzureOpenAIAssistant.ManagedIdentityCredential')  # Mock ManagedIdentityCredential
    @patch('FunctionAzureOpenAIAssistant.ManagedIdentityCredential')  # Mock ManagedIdentityCredential
    def setUp(self, MockFunctionManagedIdentityCredential, MockManagedIdentityCredential, MockGetBearerTokenProvider, MockAzureOpenAI):
        # Mock the get_token method of the ManagedIdentityCredential's return value
        mock_credential_instance = MockFunctionManagedIdentityCredential.return_value
        mock_credential_instance.get_token.return_value.token = "fake_token"
        self.mock_token_provider = MockGetBearerTokenProvider
        self.mock_client = MockAzureOpenAI.return_value
        self.mock_credential = MockManagedIdentityCredential
        self.assistant = FunctionAzureOpenAIAssistant(
            name="test",
            instructions="test instructions",
            model="test_model",
            function_spec="test_spec",
            mi_client_id="test_client_id",
            api_endpoint="https://fake.endpoint",
            app_client_id="test_app_client_id"
        )

    @patch('azure.identity.ManagedIdentityCredential')
    @patch('requests.post')
    def test_call_azure_function(self, mock_post, mock_credential):
        # Setup
        mock_token = MagicMock()
        mock_token.token = "fake_token"
        mock_credential.return_value.get_token.return_value = mock_token
        mock_post.return_value._content = b'{"result": "success"}'
        
        # Execute
        result = self.assistant.call_azure_function("test_function", {"arg1": "value1"})
        
        # Assert
        self.assertEqual(result, '{"result": "success"}')
        mock_post.assert_called_once_with(
            "https://fake.endpoint/test_function",
            headers={
                "Authorization": "Bearer fake_token",
                "Content-Type": "application/json"
            },
            data='{"arg1": "value1"}'
        )

    @patch('time.sleep', return_value=None)
    @patch.object(AzureOpenAIAssistant, 'get_run_status', side_effect=[MagicMock(status="running"), MagicMock(status="requires_action")])
    def test_wait_run_completion_or_action(self, mock_get_run_status, mock_sleep):
        # Setup
        #mock_get_run_status.return_value = MagicMock()
        #type(mock_get_run_status.return_value).status = PropertyMock(side_effect=["running", "requires_action"])
        #mock_get_run_status.return_value.status.side_effect = ["running", "requires_action"]
        # Execute
        result = self.assistant.wait_run_completion_or_action("test_run_id")
        
        # Assertcd code
        self.assertEqual(result.status, "requires_action")
        mock_get_run_status.assert_called()

    @patch.object(AzureOpenAIAssistant, 'wait_run_completion')
    @patch.object(FunctionAzureOpenAIAssistant, 'wait_run_completion_or_action')
    @patch.object(FunctionAzureOpenAIAssistant, 'call_azure_function', return_value='{"output": "result"}')
    @patch.object(FunctionAzureOpenAIAssistant, 'submit_tool_outputs_and_poll')
    @patch.object(FunctionAzureOpenAIAssistant, 'create_run')
    @patch.object(FunctionAzureOpenAIAssistant, 'add_message_to_thread')
    @patch.object(FunctionAzureOpenAIAssistant, 'get_latest_response', return_value="final_response")
    def test_message_and_receive_response(self, mock_get_latest_response, mock_add_message_to_thread, mock_create_run, mock_submit_tool_outputs_and_poll, mock_call_azure_function,
            mock_wait_run_completion_or_action, mock_wait_run_completion):
        # Setup
        mock_wait_run_completion_or_action.return_value = MagicMock(status="requires_action")
        mock_wait_run_completion.return_value = MagicMock(status="completed")
        mock_run = MagicMock()
        #mock_run.id = "test_run_id"
        #mock_run.status = "requires_action"
        mock_wait_run_completion_or_action.return_value.required_action.submit_tool_outputs.tool_calls = [
            MagicMock(function=MagicMock(arguments='{"arg1": "value1"}'), id="tool_call_id")
        ]
        mock_wait_run_completion_or_action.return_value.required_action.submit_tool_outputs.tool_calls[0].function.name = "test_function"
        mock_create_run.return_value = mock_run
        mock_submit_tool_outputs_and_poll.return_value = mock_run
        
        # Execute
        result = self.assistant.message_and_receive_response("test_message")
        
        # Assert
        self.assertEqual(result, "final_response")
        mock_add_message_to_thread.assert_called_once_with("test_message")
        mock_create_run.assert_called_once()
        mock_call_azure_function.assert_called_once_with("test_function", {"arg1": "value1"})
        mock_submit_tool_outputs_and_poll.assert_called_once()

if __name__ == '__main__':
    unittest.main()