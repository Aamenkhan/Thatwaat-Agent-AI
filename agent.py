import ollama
import datetime
import os
import logging

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename='logs/chat.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Agent CLI prints moved to run_cli
messages = [
    {
        "role": "system",
        "content": (
            "You are Thatwaat Agent AI, a helpful AI assistant. "
            "Answer clearly and help with coding, files, and learning."
        ),
    }
]
from config import OLLAMA_MODEL

def get_agent_response_stream(user):
    logging.info(f"User Prompt: {user}")
    if user.lower() == "time":
        ans = datetime.datetime.now().strftime("%I:%M %p")
        logging.info(f"AI Response: {ans}")
        yield ans
        return
    if user.lower() == "date":
        ans = str(datetime.date.today())
        logging.info(f"AI Response: {ans}")
        yield ans
        return

    messages.append({"role": "user", "content": user})

    try:
        logging.info(f"Sending request to Ollama ({OLLAMA_MODEL})")
        stream = ollama.chat(
            model=OLLAMA_MODEL,
            messages=messages,
            stream=True
        )

        full_answer = ""
        for chunk in stream:
            token = chunk["message"]["content"]
            full_answer += token
            yield token

        messages.append({"role": "assistant", "content": full_answer})
        logging.info(f"AI Response: {full_answer}")
    except Exception as e:
        error_msg = f"[Error: {str(e)}]"
        logging.error(error_msg)
        yield f"\n\n{error_msg}"

def run_cli():
    print("=" * 50)
    print("🤖 Thatwaat Agent AI")
    print("Type 'exit' to quit")
    print("=" * 50)
    
    while True:
        user = input("\nYou: ")

        if user.lower() == "exit":
            break
        
        print("\nAI: ", end="", flush=True)
        for token in get_agent_response_stream(user):
            print(token, end="", flush=True)
        print()

if __name__ == "__main__":
    run_cli()