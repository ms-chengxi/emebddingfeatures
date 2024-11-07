from azure.identity import ManagedIdentityCredential, get_bearer_token_provider
from AzureOpenAIAssistant import AzureOpenAIAssistant
import time
import json
import requests


class FunctionAzureOpenAIAssistant(AzureOpenAIAssistant):



    def __init__(self, name, instructions, model, function_spec, mi_client_id=None, api_endpoint=None, app_client_id=None):
        super().__init__(name, instructions, model, function_spec)
        self.function_spec = function_spec
        self.mi_client_id = mi_client_id
        self.api_endpoint = api_endpoint
        if self.mi_client_id or self.api_endpoint:
            credential = ManagedIdentityCredential(client_id=self.mi_client_id)
            token = credential.get_token(f"{app_client_id}/.default")
            #token = credential.get_token("d07a4aa0-7148-4e4a-9060-36a8fbec0888/.default")
            self.headers = {
                "Authorization": f"Bearer {token.token}",
                "Content-Type": "application/json"
            }


    def call_azure_function(self, function_name, arguments):
        if not self.mi_client_id or not self.api_endpoint:
            return "todo: return the call locally"    
        URI = f"{self.api_endpoint}/{function_name}"
        #URI = "https://logicappembeddingfunction.azurewebsites.net/api/embeddingfunction?Service=WaAppAgent"
        #URI = "https://logicappembeddingfunction.azurewebsites.net/api/embeddingfunction"
        body = json.dumps(arguments)
        response = requests.post(URI, headers=self.headers, data=body)
        return response._content.decode("utf-8")

    def wait_run_completion_or_action(self, run_id):
        run = self.get_run_status(run_id)
        while run.status != "completed" and run.status != "requires_action" and run.status != "failed":
            time.sleep(.2)
            run = self.get_run_status(run_id)
        return run

    def message_and_receive_response(self, message):
        self.add_message_to_thread(message)
        run = self.create_run()
        run = self.wait_run_completion_or_action(run.id)
        if run.status == "requires_action":
            # Define the list to store tool outputs
            tool_outputs = []
            
            # Loop through each tool in the required action section
            for tool in run.required_action.submit_tool_outputs.tool_calls:
                function_name = tool.function.name
                arguments = json.loads(tool.function.arguments)
                result = self.call_azure_function(function_name, arguments)
                tool_outputs.append({
                "tool_call_id": tool.id,
                "output": result
                })
            run = self.submit_tool_outputs_and_poll(run.thread_id, run.id, tool_outputs)
            self.wait_run_completion(run.id)
        response = self.get_latest_response()
        #response = self.get_run_status(run.id)#run.model_dump_json(indent=2)
        #messages = self.client.beta.threads.messages.list(self.thread.id)
        #print(messages.model_dump_json(indent=2))
        return response

    def submit_tool_outputs_and_poll(self, thread_id, run_id, tool_outputs):      
        run = self.client.beta.threads.runs.submit_tool_outputs_and_poll(
            thread_id=thread_id,
            run_id=run_id,
            tool_outputs=tool_outputs
        )
        return run