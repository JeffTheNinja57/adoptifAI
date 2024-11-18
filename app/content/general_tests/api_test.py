import google.generativeai as genai
import os

try:
    GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
except KeyError:
    with open(os.path.abspath("/gemini_key.txt"), "r") as file:
        GEMINI_API_KEY = file.read().strip()

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(
    "Tell me a story about a magic backpack.",
    generation_config=genai.types.GenerationConfig(
        # Only one candidate for now.
        candidate_count=1,
        stop_sequences=["x"],
        max_output_tokens=20,
        temperature=1.0,
    ),
)
print(response.text)