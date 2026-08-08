import speech_recognition as sr
import pyttsx3
from googletrans import Translator  # Google Translate API
import os

# --- NEW IMPORTS ADDED FOR AUDIO SAVING & WAVEFORM PLOTTING ---
import numpy as np
import matplotlib.pyplot as plt
# -------------------------------------------------------------

# Initialize text-to-speech engine
def speak(text, language="en"):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Speed of speech
    voices = engine.getProperty('voices')
    
    # Set voice for English or other language if supported by pyttsx3
    if language == "en":
        engine.setProperty('voice', voices[0].id)  # Default English voice
    else:
        engine.setProperty('voice', voices[1].id)  # Fallback to another voice if available
    
    engine.say(text)
    engine.runAndWait()

# --- NEW FUNCTION: Save audio data to a .wav file ---
def save_audio_file(audio, filename="recording.wav"):
    # file- exact folder path seeking
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
    filepath = os.path.join(script_dir, filename)
    
    wav_data = audio.get_wav_data()
    with open(filepath, "wb") as f:
        f.write(wav_data)
    print(f"💾 Audio saved as '{filepath}'")

# --- NEW FUNCTION: Visualize and display audio waveform ---
def plot_waveform(audio):
    """
    Converts audio buffer to NumPy array and plots the waveform using matplotlib.
    """
    # Extract raw audio data at 16000 Hz sample rate and 16-bit PCM width
    raw_data = audio.get_raw_data(convert_rate=16000, convert_width=2)
    samples = np.frombuffer(raw_data, dtype=np.int16)
    
    # Calculate time axis in seconds
    duration = len(samples) / 16000
    time_axis = np.linspace(0, duration, len(samples))
    
    # Render waveform graph
    plt.figure(figsize=(10, 4))
    plt.plot(time_axis, samples, color='blue')
    plt.title("Your Voice Waveform")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

# Speech-to-Text: Recognize spoken language (English)
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Please speak now in English...")
        audio = recognizer.listen(source)

    # --- FEATURE ADDED: Save audio & plot waveform immediately after recording ---
    save_audio_file(audio, filename="recording.wav")
    plot_waveform(audio)
    # -------------------------------------------------------------------------

    try:
        print("🔍 Recognizing speech...")
        text = recognizer.recognize_google(audio, language="en-US")  # Use English for speech recognition
        print(f"✅ You said: {text}")
        return text
    except sr.UnknownValueError:
        print("❌ Could not understand the audio.")
    except sr.RequestError as e:
        print(f"❌ API Error: {e}")
    return ""

# Translate text using Google Translate API
def translate_text(text, target_language="es"):  # Default target language is Spanish (es)
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    print(f"🌍 Translated text: {translation.text}")
    return translation.text

# Display language options to the user
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

    # User selects language
    choice = input("Please select the target language number (1-8): ")
    language_dict = {
        "1": "hi",
        "2": "ta",
        "3": "te",
        "4": "bn",
        "5": "mr",
        "6": "gu",
        "7": "ml",
        "8": "pa"
    }
    
    return language_dict.get(choice, "es")  # Default to Spanish if invalid input

# Main function to combine all steps
def main():
    # Step 1: Display language options and get user's choice
    target_language = display_language_options()
    
    # Step 2: Speech-to-Text (recognizing English speech + saving & plotting audio)
    original_text = speech_to_text()
    
    if original_text:
        # Step 3: Translate to selected target language
        translated_text = translate_text(original_text, target_language=target_language)
        
        # Step 4: Text-to-Speech (Translate output and speak it)
        speak(translated_text, language="en")  # Speak the translation in English
        print("✅ Translation spoken out!")

if __name__ == "__main__":
    main()