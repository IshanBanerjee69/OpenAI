# Import the OpenAI library to interact with the OpenAI API
import openai

# Import the os library to interact with the operating system
import os

# Import the load_dotenv function from the dotenv library to load environment variables from a .env file
from dotenv import load_dotenv

# Import the OpenAI class from the openai library
from openai import OpenAI

# Load environment variables from a .env file
load_dotenv()

client = OpenAI()  # Initialize the OpenAI client

# Initialize the conversation with a system message
messages = [{"role": "system", "content": "You are an intelligent assistant."}]

# Start an infinite loop to keep the conversation going
while True:
    # Prompt the user for input
    message = input("User: ")
    
    if message:  # Check if the user provided a message
        # Add the user's message to the messages list
        messages.append({"role": "user", "content": message})
        
        # Call the DALL-E API to generate an image based on the user's message
        response = client.images.generate(
            model="dall-e-3",       # Specify the model to use (DALL-E 3)
            prompt=message,         # Provide the user's message as the prompt
            size="1024x1024",       # Specify the size of the generated image
            quality="standard",     # Specify the quality of the generated image
            n=1,                    # Generate one image
        )
        
        # Print the prefix for the assistant's response
        print("DALL-E: ", end="", flush=True)
        
        # Retrieve and print the URL of the generated image
        image_url = response.data[0].url
        print(image_url)
        
        # Print a newline after the response is complete
        print()  
        
        # Append the assistant's reply to the messages list
        messages.append({"role": "assistant", "content": image_url})
