import os
import base64
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Retrieve API key
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    print("ERROR: GROQ_API_KEY is missing. Please check your .env file.")
    exit(1)
else:
    print("GROQ API Key successfully loaded.")

def encode_image(image_path):
    """
    Encodes an image file into a base64 string.

    Parameters:
        image_path (str): Path to the image file.

    Returns:
        str: Base64 encoded string of the image.
    """
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"ERROR: Image file '{image_path}' not found.")
        exit(1)

def analyze_image_with_groq(image_path, query, model_name):
    """
    Analyzes an image using the Groq API.

    Parameters:
        image_path (str): Path to the image file.
        query (str): Text query to send along with the image.
        model_name (str): Name of the model to use for analysis.
    """
    print(f"Encoding image: {image_path}")
    encoded_image = encode_image(image_path)

    print("Connecting to Groq API...")
    try:
        client = Groq(api_key=GROQ_API_KEY)

        # Send the request to the Groq API
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": query},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}},
                    ],
                }
            ],
        )

        print("Response received:\n")
        print(response.choices[0].message.content)

    except Exception as e:
        print(f"API Error: {e}")

if __name__ == "__main__":
    query = "Is there something wrong with my face?"
    model = "llama-3.2-90b-vision-preview"  

    image_path = "acne.jpg"

    analyze_image_with_groq(image_path, query, model)
