"""
🎙️ Say & See — Your Mini Speech-to-Text Studio
-------------------------------------------------
A self-contained Python tool that:
  1. Captures audio from your microphone (Audio Capture)
  2. Converts the recorded sound into numeric data (Digitization)
  3. Transcribes your speech into text using Google Speech-to-Text
  4. Plots the waveform of your recording

Run this script, speak when prompted, press Enter to stop recording,
and you'll see your transcription + waveform plot.
"""

import sys
import threading

# ------------------------------------------------------------------
# Dependency check — make sure required libraries are installed
# ------------------------------------------------------------------
try:
    import pyaudio
    import numpy as np
    import matplotlib.pyplot as plt
    import speech_recognition as sr
    from speech_recognition import AudioData
except ImportError as e:
    print(f"❌ Missing library: {e.name}")
    print("\nInstall commands:")
    print("   Windows: pip install SpeechRecognition pyaudio numpy matplotlib")
    print("   macOS:   brew install portaudio && pip install SpeechRecognition pyaudio numpy matplotlib")
    sys.exit(1)


# A simple "flag" used to signal between threads when to stop recording
stop_event = threading.Event()


# ------------------------------------------------------------------
# Step 0: Helper — waits in the background for the user to press Enter
# ------------------------------------------------------------------
def wait_for_enter():
    input()                # Blocks here until Enter is pressed
    stop_event.set()       # Signal: "stop recording now"


# ------------------------------------------------------------------
# Step 1: AUDIO CAPTURE — record raw sound from the microphone
# ------------------------------------------------------------------
def record_audio():
    stop_event.clear()  # Reset the stop flag before starting

    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,   # 16-bit audio samples
        channels=1,                # Mono recording
        rate=16000,                 # 16,000 samples per second
        input=True,
        frames_per_buffer=1024
    )

    frames = []
    print("\n🎙️  Speak now!")
    print("   Press Enter to stop recording...")

    # Start a background thread that waits for Enter to be pressed
    threading.Thread(target=wait_for_enter, daemon=True).start()

    print("🔴 Recording", end="", flush=True)
    while not stop_event.is_set():
        # Read a small chunk of audio and store it
        frames.append(stream.read(1024, exception_on_overflow=False))
        print(".", end="", flush=True)
    print(" ✅ Done!")

    stream.stop_stream()
    stream.close()
    sample_width = p.get_sample_size(pyaudio.paInt16)
    p.terminate()

    # Join all the small chunks into one continuous byte string
    audio_data = b"".join(frames)
    return audio_data, 16000, sample_width


# ------------------------------------------------------------------
# Step 2: DIGITIZATION — convert raw bytes into numeric sample values
# ------------------------------------------------------------------
def analyze_audio(data, rate):
    # Turn the raw byte stream into an array of integers (digitized signal)
    samples = np.frombuffer(data, dtype=np.int16)

    return {
        "duration": len(samples) / rate,        # Length of recording in seconds
        "avg_volume": np.mean(np.abs(samples)),  # Average loudness
        "max_volume": np.max(np.abs(samples)),   # Peak loudness
        "samples": samples                        # Full digitized waveform
    }


# ------------------------------------------------------------------
# Step 3: SPEECH RECOGNITION — convert speech audio into text
# ------------------------------------------------------------------
def transcribe(data, rate, width):
    recognizer = sr.Recognizer()
    try:
        audio = AudioData(data, rate, width)
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "[Could not understand audio]"
    except sr.RequestError:
        return "[Speech service unavailable — check your internet connection]"


# ------------------------------------------------------------------
# Step 4: DISPLAY RESULTS — print stats and transcription
# ------------------------------------------------------------------
def display_stats(stats, text):
    print("\n" + "─" * 40)
    print("📊 Recording Results")
    print("─" * 40)
    print(f"⏱️  Duration:       {stats['duration']:.2f} seconds")
    print(f"🔊 Avg Amplitude:  {stats['avg_volume']:.0f}")
    print(f"📈 Max Amplitude:  {stats['max_volume']:.0f}")
    print(f"📝 Transcription:  {text}")


# ------------------------------------------------------------------
# Step 5: VISUALIZATION — plot the waveform of the recording
# ------------------------------------------------------------------
def plot_waveform(stats, rate):
    samples = stats["samples"]
    # Build a time axis from 0 to duration, with one point per sample
    time_axis = np.linspace(0, len(samples) / rate, len(samples))

    plt.figure(figsize=(10, 4))
    plt.plot(time_axis, samples, color="blue", linewidth=0.5)
    plt.title(f"Waveform — Duration: {stats['duration']:.2f}s, Avg Amplitude: {stats['avg_volume']:.0f}")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")
    plt.grid(True, alpha=0.3)
    plt.ylim(-35000, 35000)
    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------------
# MAIN PROGRAM — ties all the steps together
# ------------------------------------------------------------------
def main():
    print("=" * 40)
    print("🎙️  SAY & SEE — Speech-to-Text Studio")
    print("=" * 40)
    print("Record your voice, see it transcribed, and view its waveform!\n")

    input("Press Enter when you're ready to start recording...")

    # 1. Capture audio
    audio_data, rate, width = record_audio()

    # 2. Digitize and analyze
    stats = analyze_audio(audio_data, rate)

    # 3. Transcribe speech to text
    text = transcribe(audio_data, rate, width)

    # 4. Display results
    display_stats(stats, text)

    # 5. Plot waveform
    plot_waveform(stats, rate)


if __name__ == "__main__":
    main()
