import speech_recognition as sr
from googletrans import Translator
import pyttsx3
import keyboard
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
import json
from datetime import datetime
import os
conversation_log = [] 


def speak(text, language="en"):
    if not text:
        print("❌ No text available to speak.")
        return

    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # Always use English voice

    engine.say(text)
    engine.runAndWait()
    engine.stop()

def log_conversation(speaker, original_text, original_lang, translated_text, translated_lang):
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "speaker": speaker,
        "original_text": original_text,
        "original_language": original_lang,
        "translated_text": translated_text,
        "translated_language": translated_lang
    }
    conversation_log.append(entry)
    print(f"📝 Logged: {speaker} said '{original_text}' -> '{translated_text}'")
    

import os

def save_conversation_log(filename="conversation_log.json"):
    if not conversation_log:
        print("❌ No conversation to save.")
        return

    #  script will be saved in the section where it is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_dir, filename)

    try:
        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(conversation_log, f, ensure_ascii=False, indent=4)
        print(f"✅ Conversation log saved to: {full_path}")
    except Exception as e:
        print(f"❌ Failed to save log: {e}")
        
        
        
        
        

# Push-to-Talk enabled Speech-to-Text
def speech_to_text(recognition_language="en-US", prompt="Hold SPACE to speak..."):
    recognizer = sr.Recognizer()

    print(f"🎙️ {prompt}")
    print("👉 Press and hold SPACE to talk, release to stop.")

    # Wait until user presses and holds the hotkey
    keyboard.wait("space")  # Blocks here until SPACE is pressed

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.3)
        print("🔴 Recording... (release SPACE to stop)")

        audio_data = []

        # Keep listening only while SPACE is held down
        with sr.Microphone() as source:
            while keyboard.is_pressed("space"):
                try:
                    # Listen in small chunks while key is held
                    audio_chunk = recognizer.listen(source, phrase_time_limit=1, timeout=1)
                    audio_data.append(audio_chunk)
                except sr.WaitTimeoutError:
                    continue

        print("⏹️ Recording stopped.")

    if not audio_data:
        print("❌ No audio captured.")
        return ""

    # Combine all chunks into one AudioData object
    combined_frame_data = b"".join(chunk.get_raw_data() for chunk in audio_data)
    sample_rate = audio_data[0].sample_rate
    sample_width = audio_data[0].sample_width
    full_audio = sr.AudioData(combined_frame_data, sample_rate, sample_width)

    try:
        print("🔍 Recognizing speech...")
        text = recognizer.recognize_google(full_audio, language=recognition_language)
        print(f"✅ You said: {text}")
        return text
    except sr.UnknownValueError:
        print("❌ Could not understand the audio.")
    except sr.RequestError as e:
        print(f"❌ API Error: {e}")
    return ""


def translate_text(text, source_language="en", target_language="hi"):
    translator = Translator()
    translation = translator.translate(text, src=source_language, dest=target_language)
    print(f"🌐 Translated ({source_language} → {target_language}): {translation.text}")
    return translation.text


SCRIPT_MAP = {
    "hi": sanscript.DEVANAGARI,
    "mr": sanscript.DEVANAGARI,
    "bn": sanscript.BENGALI,
    "ta": sanscript.TAMIL,
    "te": sanscript.TELUGU,
    "gu": sanscript.GUJARATI,
    "ml": sanscript.MALAYALAM,
    "pa": sanscript.GURMUKHI,
}

RECOGNITION_LOCALE = {
    "hi": "hi-IN",
    "ta": "ta-IN",
    "te": "te-IN",
    "bn": "bn-IN",
    "mr": "mr-IN",
    "gu": "gu-IN",
    "ml": "ml-IN",
    "pa": "pa-IN",
}


def transliterate_to_roman(text, target_language):
    script = SCRIPT_MAP.get(target_language)
    if not script:
        return text
    roman_text = transliterate(text, script, sanscript.ITRANS)
    print(f"🔤 Roman script: {roman_text}")
    return roman_text


def display_language_options():
    print("🌍 Available translation languages: ")
    print("1. Hindi (hi)")
    print("2. Tamil (ta)")
    print("3. Telugu (te)")
    print("4. Bengali (bn)")
    print("5. Marathi (mr)")
    print("6. Gujarati (gu)")
    print("7. Malayalam (ml)")
    print("8. Punjabi (pa)")

    choice = input("Please select the target language number (1-8): ")
    language_dict = {
        "1": "hi", "2": "ta", "3": "te", "4": "bn",
        "5": "mr", "6": "gu", "7": "ml", "8": "pa"
    }
    return language_dict.get(choice, "hi")


def conversation_loop(target_language):
    recognition_locale = RECOGNITION_LOCALE.get(target_language, "hi-IN")

    print("\n🔄 Bi-directional conversation started.")
    print("Press and hold SPACE to talk, release to stop.")
    print("Say 'exit' or 'quit' to end.\n")

    turn = "english_speaker"

    while True:
        if turn == "english_speaker":
            print("---- 🧑 English Speaker's turn ----")
            original_text = speech_to_text(
                recognition_language="en-US",
                prompt="Hold SPACE and speak in English..."
            )
            if original_text.lower() in ["exit", "quit", "stop"]:
                print("👋 Conversation ended.")
                save_conversation_log()
                break
            if original_text:
                translated = translate_text(original_text, source_language="en", target_language=target_language)
                log_conversation("English Speaker", original_text, "en", translated, target_language)
                roman = transliterate_to_roman(translated, target_language)
                speak(roman, language="en")
            turn = "target_speaker"

        else:
            print("---- 🧑 Target Language Speaker's turn ----")
            original_text = speech_to_text(
                recognition_language=recognition_locale,
                prompt="Hold SPACE and speak in your language..."
            )
            if original_text.lower() in ["exit", "quit", "stop"]:
                print("👋 Conversation ended.")
                save_conversation_log()
                break
            if original_text:
                translated_back = translate_text(original_text, source_language=target_language, target_language="en")
                log_conversation("Target Language Speaker", original_text, target_language, translated_back, "en")
                speak(translated_back, language="en")
            turn = "english_speaker"


def main():
    target_language = display_language_options()
    conversation_loop(target_language)


if __name__ == "__main__":
    main()