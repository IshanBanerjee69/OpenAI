# importing openai and dotenv modules
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Create an instance of the OpenAI client
client = OpenAI()

# Initialize the conversation with a system message that sets the role and behavior of the assistant
messages = [{"role": "system", "content": "You are an intelligent assistant."}]

# Enter an infinite loop to continually prompt the user for input
while True:
    # Prompt the user for input
    message = input("User: ")
    
    # Check if the user provided a message
    if message:
        # Append the user's message to the messages list with the role 'user'
        messages.append({"role": "user", "content": message})
        
        # Create a chat completion request to the OpenAI API
        chat = client.chat.completions.create(
            model="gpt-4o",  # Specify the model to use
            messages=messages,  # Pass the conversation history
            stream=True  # Enable streaming of the response
        )
        
        # Start streaming the response
        print("ChatGPT: ", end="", flush=True)
        collected_messages = ""
        
        # Stream and print the response as it's generated
        for chunk in chat:
            # Check if the current chunk has content prints it, and appends it to the response
            if hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content is not None:
                chunk_message = str(chunk.choices[0].delta.content)
                print(chunk_message, end="", flush=True)
                collected_messages += chunk_message
        
        # Print a newline after the response is complete
        print()
        
        # Append the assistant's reply to the messages list with the role 'assistant'
        messages.append({"role": "assistant", "content": collected_messages})
