import argparse
import torch
from TTS.api import TTS
import os

def generate_voice(text, output_path, speaker_wav=None):
    """
    Generates speech from text using a pre-trained TTS model.
    If a speaker_wav is provided, it will attempt to clone the voice.
    """
    print("Initializing Coqui-TTS model...")
    # Check for GPU availability
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    try:
        # Using a multi-speaker, multi-lingual model that's good for general use.
        # On first run, this will download the necessary model files.
        model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
        tts = TTS(model_name, progress_bar=True).to(device)
    except Exception as e:
        print(f"ERROR: Failed to load TTS model. Please check your internet connection.")
        print(f"Details: {e}")
        return

    print("TTS model loaded. Generating voiceover...")

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        # Use the provided speaker WAV for voice cloning if available, otherwise use a default voice.
        if speaker_wav and os.path.exists(speaker_wav):
            print(f"Attempting voice cloning from: {speaker_wav}")
            tts.tts_to_file(
                text=text,
                file_path=output_path,
                speaker_wav=speaker_wav,
                language="en" # Specify language for better results
            )
        else:
            if speaker_wav:
                print(f"Warning: Speaker WAV file not found at '{speaker_wav}'. Using default voice.")
            else:
                print("No speaker WAV provided. Using default voice.")
            # This model doesn't have default speakers, it requires a speaker_wav.
            # We must provide a fallback or raise an error.
            # For this agent, we will require a speaker_wav for this model.
            print("ERROR: This TTS model requires a speaker WAV file for voice cloning.")
            print("Please provide a path to a clean audio sample of the desired voice via --speaker_wav.")
            return

        print(f"Successfully saved voiceover to: {output_path}")

    except Exception as e:
        print(f"An unexpected error occurred during TTS synthesis: {e}")
        if "out of memory" in str(e).lower():
            print("\nCUDA out of memory. The input text might be too long.")
        else:
            print(f"\nAn unhandled error occurred: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate voiceovers using Coqui-TTS.")
    parser.add_argument("--text", type=str, required=True, help="The text to synthesize.")
    parser.add_argument("--output_path", type=str, required=True, help="The path to save the output .wav file.")
    parser.add_argument("--speaker_wav", type=str, default=None, help="Path to a .wav file of the target voice for cloning. Required for this model.")

    args = parser.parse_args()

    if not args.speaker_wav:
        print("Error: The --speaker_wav argument is required for the selected TTS model.")
        print("Please provide a path to a clean audio sample (e.g., 10 seconds) of the desired voice.")
    else:
        generate_voice(args.text, args.output_path, args.speaker_wav)