from FunctionAzureOpenAIAssistant import FunctionAzureOpenAIAssistant

def main():

    #salientexamples
    # hnproxy
    # Initialize the assistant
    assistant_name = "MyAssistant"
    instructions = "You are a helpful assistant."
    model = "gpt-4o"
    mi_client_id = "1820118a-ccca-4e98-ae0a-6dcb9c01eadf"
    api_endpoint = "https://perftest2.azurewebsites.net/api"
    app_client_id = "6cdf5319-fd7d-4ca7-9499-66cfe19fa436"
    function_spec = [{
        "type": "function",
        "function": {
            "name": "salientexamples",
            "description": "Extract salient examples based on human text requirements",
            "parameters": {
                "type": "object",
                "properties": {
                "name": {"type": "string", "description": "name of Cosmic container"}
                # "location": {"type": "string", "description": "Location for the query"}
                },
                "required": ["name"]
            }
        }
    }]

    assistant = FunctionAzureOpenAIAssistant(assistant_name, instructions, model, function_spec, mi_client_id, api_endpoint, app_client_id)

    print("Assistant initialized. You can start chatting now.")
    print("Type 'exit' to end the chat.")

    while True:
        user_message = input("You: ")
        if user_message.lower() == 'exit':
            print("Ending chat. Goodbye!")
            break

        response = assistant.message_and_receive_response(user_message)
        print(f"Assistant: {response}")

if __name__ == "__main__":
    main()