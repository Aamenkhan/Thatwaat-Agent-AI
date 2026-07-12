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

while True:
    user = input("\nYou: ")

    if user.lower() == "exit":
        break

    if user.lower() == "time":
        print("AI:", datetime.datetime.now().strftime("%I:%M %p"))
        continue

    if user.lower() == "date":
        print("AI:", datetime.date.today())
        continue

    messages.append({"role": "user", "content": user})

    response = ollama.chat(
        model="qwen2.5-coder:3b",
        messages=messages,
    )

    answer = response["message"]["content"]
    print("\nAI:", answer)

    messages.append({"role": "assistant", "content": answer})