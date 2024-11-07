from openai import AzureOpenAI
from azure.identity import ManagedIdentityCredential, get_bearer_token_provider
import time
import json

class AzureOpenAIAssistant:

    

    def __init__(self, name, instructions, model, tools = None):
        self.name = name
        self.instructions = instructions
        self.model = model
        self.tools = tools
        self.client = self.__create_client()
        self.assistant = self.__create_assistant()
        self.thread = self.__create_thread()


    def __create_client(self):
            token_provider = get_bearer_token_provider(
                    ManagedIdentityCredential(client_id= "92056c31-71e6-4ff3-a938-371fb93b3d0e"), "https://cognitiveservices.azure.com/.default"
                    )
            client = AzureOpenAI(
                    azure_ad_token_provider=token_provider,
                    api_version = "2024-02-15-preview",
                    azure_endpoint = "https://capsenseadsoai.openai.azure.com/"
                    )
            return client


    def __create_assistant(self):
        assistant = self.client.beta.assistants.create(
                name= self.name,
                instructions=self.instructions,
                model= self.model,
                tools=self.tools
                )
        return assistant


    def __create_thread(self):
        thread = self.client.beta.threads.create()
        return thread
    

    def create_run(self):
        run = self.client.beta.threads.runs.create(
                thread_id=self.thread.id,
                assistant_id=self.assistant.id,
                )
        return run
    

    def get_run_status(self, run_id):
        run = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread.id,
                run_id=run_id
                )
        return run


    def print_thread_messages(self):
        thread_messages = self.client.beta.threads.messages.list(self.thread.id)
        return thread_messages.model_dump_json(indent=2)
    

    def print_assistant(self):
        return self.assistant.model_dump_json(indent=2)
    

    def wait_run_completion(self, run_id):
        run = self.get_run_status(run_id)
        while run.status != "completed" and run.status != "failed":
            time.sleep(.2)
            run = self.get_run_status(run_id)
        return run
    

    def add_message_to_thread(self, message):
        message = self.client.beta.threads.messages.create(
                thread_id=self.thread.id,
                role="user",
                content=message
                )
        return message


    def get_latest_response(self):
        thread_messages = self.client.beta.threads.messages.list(self.thread.id)
        data = json.loads(thread_messages.model_dump_json(indent=2))
        latest_response = data['data'][0]['content'][0]['text']['value']#data['messages'][-1]['content']
        return latest_response


    def message_and_receive_response(self, message):
        self.add_message_to_thread(message)
        run = self.create_run()
        self.wait_run_completion(run.id)
        response = self.get_latest_response()
        return response

        