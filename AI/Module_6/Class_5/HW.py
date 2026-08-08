import speech_recognition as sr
import pyttsx3
import json
import os
from openai import OpenAI

# 1. Importing GROQ_API_KEY from config.py
from config import GROQ_API_KEY

# 2. Groq Client setup — uses the OpenAI library, just with a different base_url
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# 3. File where conversation history will be stored persistently
# Using the script's own folder (not the current working directory) so the
# file always ends up next to HW.py, no matter where you run the command from
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORY_FILE = os.path.join(SCRIPT_DIR, "chat_history.json")

# 4. System prompt that defines the assistant's behavior (always sent first)
SYSTEM_PROMPT = {
    "role": "system",
    "content": "You are a helpful voice assistant. Answer in 1-2 short sentences."
}


def load_history():
    """Load chat history from the JSON file. If it doesn't exist, start fresh."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            # If the file is empty/corrupted, start with a fresh history
            return [SYSTEM_PROMPT]
    return [SYSTEM_PROMPT]


def save_history(history):
    """Save the current chat history to the JSON file."""
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


# 5. chat_history list is created ONCE, outside the main loop, and loaded from disk
chat_history = load_history()


def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Speak now...")
        audio = r.listen(source)
        try:
            command = r.recognize_google(audio)
            print(f"✅ You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("❌ Could not understand.")
        except sr.RequestError as e:
            print(f"❌ API Error: {e}")
    return ""


def ask_llm(command):
    global chat_history

    if "exit" in command or "stop" in command:
        speak("Goodbye!")
        return False

    try:
        # 6. Append the new user message to the running history
        chat_history.append({"role": "user", "content": command})

        # 7. Send the ENTIRE history (not just the current command) so the
        #    model has full context of the conversation so far
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=chat_history
        )

        reply = response.choices[0].message.content
        print(f"🤖 AI Response: {reply}")
        speak(reply)

        # 8. Append the assistant's reply to history too, then persist to disk
        chat_history.append({"role": "assistant", "content": reply})
        save_history(chat_history)

    except Exception as e:
        print(f"Error calling LLM API: {e}")
        speak("Sorry, I am having trouble connecting right now.")
        # Remove the last user message since it never got a successful reply
        if chat_history and chat_history[-1]["role"] == "user":
            chat_history.pop()

    return True


def main():
    speak("Voice assistant activated with AI. Ask me anything!")
    while True:
        command = get_audio()
        if command:
            should_continue = ask_llm(command)
            if not should_continue:
                break

if __name__ == "__main__":
    main()