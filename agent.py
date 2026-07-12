import ollama
import datetime
import os

print("=" * 50)
print("🤖 Thatwaat Agent AI")
print("Type 'exit' to quit")
print("=" * 50)

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

def get_agent_response(user):
    if user.lower() == "time":
        return datetime.datetime.now().strftime("%I:%M %p")
    if user.lower() == "date":
        return str(datetime.date.today())

    messages.append({"role": "user", "content": user})

    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=messages,
    )

    answer = response["message"]["content"]
    messages.append({"role": "assistant", "content": answer})
    return answer

def run_cli():
    while True:
        user = input("\nYou: ")

        if user.lower() == "exit":
            break
        
        answer = get_agent_response(user)
        print("\nAI:", answer)

if __name__ == "__main__":
    run_cli()