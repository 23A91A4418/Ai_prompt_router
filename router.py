import os
import json
import google.generativeai as genai
from datetime import datetime
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPTS

# Load environment variables
load_dotenv()

# Configure Google Generative AI
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    print("Warning: GOOGLE_API_KEY not found in environment variables.")

LOG_FILE = "route_log.jsonl"

def log_request(intent: str, confidence: float, user_message: str, final_response: str):
    """
    Logs the routing decision and final response to a JSON Lines file.
    """
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "intent": intent,
        "confidence": confidence,
        "user_message": user_message,
        "final_response": final_response
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

def route_and_respond(message: str, intent_data: dict) -> str:
    """
    Routes the message to the appropriate expert or asks for clarification.
    """
    intent = intent_data.get("intent", "unclear")
    confidence = intent_data.get("confidence", 0.0)
    
    # Confidence threshold: if low, treat as unclear
    if confidence < 0.7:
        intent = "unclear"

    if intent == "unclear" or intent not in SYSTEM_PROMPTS:
        final_response = "I'm not quite sure what you're asking for. Could you please clarify if you're looking for help with coding, data analysis, writing coaching, or career advice?"
    else:
        system_prompt = SYSTEM_PROMPTS[intent]
        try:
            model = genai.GenerativeModel("gemini-flash-latest", system_instruction=system_prompt)
            response = model.generate_content(message)
            final_response = response.text.strip()
        except Exception as e:
            final_response = f"An error occurred while generating the response: {e}"

    # Log the request
    log_request(intent, confidence, message, final_response)
    
    return final_response

if __name__ == "__main__":
    # Small test
    test_intent = {"intent": "code", "confidence": 0.95}
    test_msg = "how do i sort a list in python?"
    print(f"Routing message: {test_msg}")
    print(f"Response: {route_and_respond(test_msg, test_intent)}")
