import json
import google.genai as genai

MODEL_NAME = "models/gemini-2.5-flash"


def call_gemini(prompt: str, api_key: str):
    if not api_key:
        raise RuntimeError("Gemini API key is required")

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config={
            "temperature": 0,
            "response_mime_type": "application/json",
        },
    )

    if not response.text:
        raise RuntimeError("Empty response from Gemini")

    return json.loads(response.text)
