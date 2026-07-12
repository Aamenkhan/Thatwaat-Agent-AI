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
        "content": """You are Thatwaat Agent AI.

Rules:
- Default language: Hindi.
- Agar user Hindi me baat kare to hamesha Hindi me jawab do.
- Agar user English me baat kare to English me jawab do.
- Agar user Hinglish me baat kare to Hinglish me jawab do.
- Programming code aur code comments English me rakho.
- Explanations user ki language me do."""
    }
]
from config import OLLAMA_MODEL

def get_agent_response_stream(user, lang="Auto"):
    logging.info(f"User Prompt: {user} (Lang: {lang})")
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

    if lang != "Auto":
        content = f"Reply in {lang}.\n\n{user}"
    else:
        content = user

    messages.append({"role": "user", "content": content})

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