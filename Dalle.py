import openai
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Ensure you set your OpenAI API key in the environment variables
client = OpenAI()

messages = [{"role": "system", "content": "You are an intelligent assistant."}]

while True:
    message = input("User: ")
    if message:
        messages.append({"role": "user", "content": message})
        
        # Call the ChatCompletion API with streaming enabled
        response = client.images.generate(
            model="dall-e-3",
            prompt=message,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        
        print("Dall-E: ", end="", flush=True)
        
        # Stream and print the response as it's generated
        image_url = response.data[0].url
        print(image_url)
        
        print()  # Print a newline after the response is complete
        
        # Append the assistant's reply to the messages list