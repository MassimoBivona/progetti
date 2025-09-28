import argparse
import torch
from scipy.io.wavfile import write as write_wav
from transformers import AutoProcessor, MusicgenForConditionalGeneration
import os

def generate_music(prompt, duration_seconds, output_path):
    """
    Generates music using the MusicGen model and saves it to a file.
    """
    print("Initializing MusicGen model...")
    print("This may take a while on the first run as the model needs to be downloaded.")

    # Check for GPU availability
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    try:
        processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
        model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small").to(device)
    except Exception as e:
        print(f"ERROR: Failed to load MusicGen model from Hugging Face. Please check your internet connection.")
        print(f"Details: {e}")
        return

    print("Model loaded. Generating music...")

    inputs = processor(
        text=[prompt],
        padding=True,
        return_tensors="pt",
    ).to(device)

    # Calculate max new tokens based on duration. The model generates at a certain rate.
    # The default model's sampling rate is 32000, and it generates tokens that correspond to that.
    # A common heuristic is ~50 tokens per second of audio.
    max_new_tokens = int(duration_seconds * 50)

    audio_values = model.generate(**inputs, do_sample=True, guidance_scale=3, max_new_tokens=max_new_tokens)

    print("Music generated. Saving to file...")

    # Get the sampling rate from the model's config
    sampling_rate = model.config.audio_encoder.sampling_rate

    # The output is a batch, so we take the first item
    audio_data = audio_values[0, 0].cpu().numpy()

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Write the WAV file
    write_wav(output_path, rate=sampling_rate, data=audio_data)
    print(f"Successfully saved music to: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate music using Meta's MusicGen model.")
    parser.add_argument("--prompt", type=str, required=True, help="A description of the music to generate.")
    parser.add_argument("--duration", type=int, default=30, help="The desired duration of the music in seconds.")
    parser.add_argument("--output_path", type=str, required=True, help="The path to save the output .wav file.")

    args = parser.parse_args()

    try:
        generate_music(args.prompt, args.duration, args.output_path)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        # Provide a more helpful message for common issues
        if "out of memory" in str(e).lower():
            print("\nCUDA out of memory. Please try a smaller duration or a smaller model version if available.")
        elif "offline" in str(e).lower():
            print("\nCould not connect to Hugging Face. Please ensure you have an active internet connection for the first run.")
        else:
            print(f"\nAn unhandled error occurred: {e}")