import subprocess
import os
import sys

class VoiceGenerator:
    """
    A wrapper to run a Text-to-Speech (TTS) engine like Coqui TTS or OpenVoice
    via a command-line script.
    """
    def __init__(self, config, project_path):
        """
        Initializes the VoiceGenerator.

        Args:
            config (dict): The voice configuration section.
            project_path (str): The path to the current project's output directory.
        """
        self.wrapper_script = config.get('wrapper_script')
        if not self.wrapper_script or not os.path.exists(self.wrapper_script):
            raise FileNotFoundError(f"TTS wrapper script not found at: {self.wrapper_script}")
        self.project_path = project_path
        self.script_dir = os.path.dirname(self.wrapper_script)

    def generate_voiceover(self, text, speaker, filename):
        """
        Generates a voiceover from a line of text.

        Args:
            text (str): The text to be spoken.
            speaker (str): The identifier for the voice to use (e.g., 'narrator').
            filename (str): The desired output filename (without extension).

        Returns:
            str: The path to the generated audio file, or None on failure.
        """
        print(f"Generating voiceover for speaker '{speaker}': '{text[:60]}...'")

        output_dir = os.path.join(self.project_path, "audio", "voices")
        os.makedirs(output_dir, exist_ok=True)

        output_filepath = os.path.join(output_dir, f"{filename}.wav")

        command = [
            sys.executable,
            self.wrapper_script,
            "--text", text,
            "--speaker", speaker,
            "--output_path", output_filepath
        ]

        print(f"Executing TTS command: {' '.join(command)}")

        try:
            # This is the actual command execution.
            process = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
                cwd=self.script_dir,
                timeout=120 # 2-minute timeout for TTS generation
            )
            print("TTS process completed.")
            print(f"TTS STDOUT: {process.stdout}")

            if os.path.exists(output_filepath):
                print(f"Successfully generated voiceover: {output_filepath}")
                return output_filepath
            else:
                print("ERROR: TTS script ran, but the output file was not created.")
                return None

        except FileNotFoundError:
            print(f"ERROR: The python executable or the TTS wrapper script was not found.")
            raise
        except subprocess.CalledProcessError as e:
            print(f"ERROR: TTS execution failed with return code {e.returncode}.")
            print(f"Stderr: {e.stderr}")
            print(f"Stdout: {e.stdout}")
            return None
        except subprocess.TimeoutExpired:
            print("ERROR: TTS execution timed out.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred while running TTS: {e}")
            return None