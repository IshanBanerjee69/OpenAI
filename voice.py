from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
from playsound import playsound

# Load environment variables from the .env file
load_dotenv()

# Initialize the OpenAI client
client = OpenAI()

# Define the path to save the speech file
speech_file_path = Path(__file__).parent / "speech.mp3"

# Start an infinite loop to repeatedly ask for user input
while True:
    # Get user input for the text to be converted to speech
    user_input = input("Enter the text to convert to speech (or 'exit' to quit): ")
    
    # Check if the user wants to exit
    if user_input.lower() == 'exit':
        print("Exiting the program.")
        break

    try:
        # Create the speech response using the OpenAI client
        response = client.audio.speech.create(
            model="tts-1",
            voice="nova",  # Ensure the correct case for the voice option
            input=user_input
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
