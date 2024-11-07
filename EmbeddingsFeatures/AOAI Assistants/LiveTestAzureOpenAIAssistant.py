from AzureOpenAIAssistant import AzureOpenAIAssistant

def main():
    # Initialize the assistant
    assistant_name = "MyAssistant"
    instructions = "You are a helpful assistant."
    model = "gpt-4o"

    assistant = AzureOpenAIAssistant(assistant_name, instructions, model)

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