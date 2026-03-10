# AI Prompt Router

An intelligent system design pattern for intent-based routing in AI applications. This project demonstrates how to route user requests to specialized "expert" AI personas after an initial classification step.

## Features

- **Intent Classification**: Uses a lightweight LLM call to identify user intent (Code, Data, Writing, Career, or Unclear).
- **Expert Personas**: Dedicated system prompts for different domains ensuring high-quality specialized responses.
- **Decision Logging**: Every classification and routing decision is logged to `route_log.jsonl` for audit and improvement.
- **Robustness**: Handles malformed LLM responses and low-confidence classifications gracefully.

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure Environment**:
    - Copy `.env.example` to `.env`.
    - Add your `GOOGLE_API_KEY` to the `.env` file.

## Usage

Run the unified entry point:

```bash
python main.py
```

### Examples

- **Code**: "How do I reverse a string in Python?"
- **Data**: "What does a high standard deviation tell me about my data?"
- **Writing**: "Can you check if this paragraph is too wordy?"
- **Career**: "What are the most in-demand skills for a Cloud Architect in 2024?"

## Architecture

1.  **`classifier.py`**: The "First Pass" - listens to the user and outputs a JSON intent.
2.  **`prompts.py`**: Storage for all system instructions and classification schemas.
3.  **`router.py`**: The "Traffic Controller" - selects the best expert and logs the outcome.
4.  **`main.py`**: The "Operator" - provides a loop-based interface for the user.