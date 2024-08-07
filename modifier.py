import streamlit as st
import openai
from dotenv import load_dotenv
import base64

load_dotenv()
openai.api_key = "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"  # Ensure your API key is set here or via .env file

def dalle_completions(prompt, image_data):
    try:
        # Simplified API call for debug purposes
        response = openai.images.generate(
            prompt=prompt,
            model= "dall-e-2",
            n=1,
            size="1024x1024"
        )
        print("API response:", response)
        image_url = response.data[0].url
        return image_url
    except Exception as e:
        print("Error generating image:", e)
        return None

st.title("DALL-E Image Modifier")

# Upload an image
image_file = st.file_uploader(
    "Upload an image with company names or logos...",
    type=["jpg", "jpeg", "png", "webp"],
)

image_data = None
if image_file:
    st.image(image_file, caption="Uploaded Image")
    image_bytes = image_file.getvalue()
    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    image_data = f"data:image/jpeg;base64,{base64_image}"

# Get the user's description
message = st.text_area("Enter a description of how you want to modify the image...")
gen_button = st.button("Generate Modified Image")

if gen_button and image_file and message:
    response_url = dalle_completions(message, image_data)
    if response_url:
        st.image(response_url, caption="Dalle Modified Image", use_column_width=True)
    else:
        st.write("Failed to generate image. Check logs for details.")
