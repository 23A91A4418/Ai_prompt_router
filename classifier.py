import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from prompts import CLASSIFIER_PROMPT

# Load environment variables
load_dotenv()

# Configure Google Generative AI
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    print("Warning: GOOGLE_API_KEY not found in environment variables.")

def classify_intent(message: str) -> dict:
    """
    Classifies the user's intent using an LLM.
    Returns a dictionary with 'intent' and 'confidence'.
    """
    try:
        model = genai.GenerativeModel("gemini-flash-latest")
        prompt = CLASSIFIER_PROMPT.format(message=message)
        
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Strip potential markdown formatting (e.g., ```json ... ```)
        if response_text.startswith("```json"):
            response_text = response_text[7:-3].strip()
        elif response_text.startswith("```"):
            response_text = response_text[3:-3].strip()

        intent_data = json.loads(response_text)
        
        # Validate keys
        if "intent" not in intent_data or "confidence" not in intent_data:
            raise ValueError("Missing required keys in LLM response")
            
        return intent_data

    except (json.JSONDecodeError, ValueError, Exception) as e:
        print(f"Error parsing classifier response: {e}")
        # Default to unclear if parsing fails
        return {"intent": "unclear", "confidence": 0.0}

if __name__ == "__main__":
    # Test cases
    test_message = "how do i sort a list in python?"
    print(f"Message: {test_message}")
    print(f"Classification: {classify_intent(test_message)}")
