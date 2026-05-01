import json
import re
from ollama import AsyncClient  # Using AsyncClient to prevent server blocking

# Set this to the model you have downloaded (e.g., gemma3:4b)
MODEL_NAME = "gemma3:4b"

async def call_local_llm(prompt: str) -> str:
    """
    Asynchronously sends a prompt to the local Ollama model.
    This prevents the FastAPI event loop from freezing during inference.
    """
    try:
        response = await AsyncClient().chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You are a specialized data extraction engine. Output ONLY raw JSON. No conversational text or markdown backticks."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            # Options to ensure faster and more consistent extraction
            options={
                "temperature": 0,
                "num_ctx": 4096
            }
        )
        return response["message"]["content"]
    except Exception as e:
        print(f" Ollama Connection Error: {e}")
        return "{}"

def extract_json(text: str) -> dict:
    """
    Safely extracts and parses JSON from the LLM output, 
    even if the model includes extra text or markdown backticks.
    """
    if not text:
        return {}
        
    # Regex to find text between the first { and last }
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            print(" Error: LLM returned invalid JSON format.")
            return {}
    return {}
if __name__ == "__main__":
    import asyncio
    async def test():
        print(f" Testing connection to {MODEL_NAME}...")
        try:
            # Simple test prompt
            res = await call_local_llm("Say 'Connected' if you can read this.")
            print(f"Success! Gemma responded: {res}")
        except Exception as e:
            print(f" Connection failed: {e}")

    asyncio.run(test())
