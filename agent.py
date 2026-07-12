import ollama
import datetime
import os

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
    if user.lower() == "time":
        yield datetime.datetime.now().strftime("%I:%M %p")
        return
    if user.lower() == "date":
        yield str(datetime.date.today())
        return

    messages.append({"role": "user", "content": user})

    try:
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
    except Exception as e:
        yield f"\n\n[Error: {str(e)}]"

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