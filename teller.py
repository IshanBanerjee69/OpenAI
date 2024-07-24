from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
from playsound import playsound

# Load environment variables from the .env file
load_dotenv()

# Initialize the OpenAI client
client = OpenAI()

# Initialize the conversation with a system message that sets the role and behavior of the assistant
messages = [{"role": "system", "content": "You are an intelligent assistant."}]

# Define the path to save the speech file
speech_file_path = Path(__file__).parent / "speech.mp3"

# Start an infinite loop to repeatedly ask for user input
while True:
    # Get user input
    user_input = input("User: ")
    
    # Check if the user wants to exit
    if user_input.lower() == 'exit':
        print("Exiting the program.")
        break

    # Append the user's message to the messages list with the role 'user'
    messages.append({"role": "user", "content": user_input})
    
    # Create a chat completion request to the OpenAI API
    chat = client.chat.completions.create(
        model="gpt-4o",  # Specify the model to use
        messages=messages,  # Pass the conversation history
        stream=True  # Enable streaming of the response
    )
    
    # Print the assistant's response as it's generated
    print("ChatGPT: ", end="", flush=True)
    collected_messages = ""
    
    # Stream and print the response as it's generated
    for chunk in chat:
        # Check if the current chunk has content and append it to the response
        if hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content is not None:
            chunk_message = str(chunk.choices[0].delta.content)
            print(chunk_message, end="", flush=True)
            collected_messages += chunk_message
    
    # Print a newline after the response is complete
    print()
    
    # Append the assistant's reply to the messages list with the role 'assistant'
    messages.append({"role": "assistant", "content": collected_messages})

    try:
        # Create the speech response using the OpenAI client
        response = client.audio.speech.create(
            model="tts-1",
            voice="nova",  # Ensure the correct case for the voice option
            input=collected_messages
        )

        # Check if the response object is valid
        if response is None:
            print("No response received from the API.")
        else:
            print("Response received. Attempting to stream content to file.")

        # Stream the response content to a file
        with open(speech_file_path, "wb") as f:
            for chunk in response.iter_bytes():
                if not chunk:
                    print("Empty chunk received.")
                    continue
                f.write(chunk)
                print(f"Written chunk of size {len(chunk)}")

        # Verify file size
        file_size = speech_file_path.stat().st_size
        print(f"File saved successfully. Size: {file_size} bytes")

        # Play the MP3 file
        playsound(speech_file_path)

    except Exception as e:
        # Print any errors that occur during the process
        print(f"An error occurred: {e}")
