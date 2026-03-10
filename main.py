import sys
from classifier import classify_intent
from router import route_and_respond

def main():
    print("Welcome to the AI Prompt Router!")
    print("---------------------------------")
    print("This system routes your request to specialized AI experts based on your intent.")
    print("Categories: Code, Data, Writing, Career Advice.")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        try:
            user_input = input("User > ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ("exit", "quit", "q"):
                print("Goodbye!")
                break

            print("\n[Thinking...] Classifying intent...")
            intent_data = classify_intent(user_input)
            
            intent = intent_data.get("intent", "unclear")
            confidence = intent_data.get("confidence", 0.0)
            
            print(f"[Decision] Intent: {intent} (Confidence: {confidence:.2f})")
            print("[Routing] Getting response from expert...\n")
            
            response = route_and_respond(user_input, intent_data)
            
            print("Expert Response:")
            print("----------------")
            print(response)
            print("----------------\n")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            print("Please try again.\n")

if __name__ == "__main__":
    main()
