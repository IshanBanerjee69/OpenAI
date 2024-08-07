
import base64
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

image_file = st.file_uploader(
    "Upload an image with company names or logos...",
    type=["jpg", "jpeg", "png", "webp"],
)

if image_file:
    st.image(image_file, caption="Uploaded Image")

    image_bytes = image_file.getvalue()
    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    image_url = f"data:image/jpeg;base64,{base64_image}"

message = st.text_area("Ask anything about the image..")
messages = [{"type": "text", "text": message}]

send = st.button("Send")

if image_file and send:
    messages.append({
        "type": "image_url",
        "image_url": {"url": image_url}
    })

    # Make the API call to OpenAI
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": messages,
            }
        ],
        max_tokens=300,
    )

    st.markdown("##### ChatGPT:")
    st.write(response.choices[0].message.content)


    
