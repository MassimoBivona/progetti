import subprocess
import os
import sys

class MusicGenerator:
    """
    A wrapper to run MusicGen via a command-line script to generate music tracks.
    """
    def __init__(self, config, project_path):
        """
        Initializes the MusicGenerator.

        Args:
            config (dict): The musicgen configuration section.
            project_path (str): The path to the current project's output directory.
        """
        self.wrapper_script = config.get('wrapper_script')
        if not self.wrapper_script or not os.path.exists(self.wrapper_script):
            raise FileNotFoundError(f"MusicGen wrapper script not found at: {self.wrapper_script}")
        self.project_path = project_path
        self.script_dir = os.path.dirname(self.wrapper_script)

    def generate_music(self, prompt, duration_seconds=30):
        """
        Generates a music track based on a text prompt.

        Args:
            prompt (str): A description of the music to generate.
            duration_seconds (int): The desired duration of the music track.

        Returns:
            str: The path to the generated audio file, or None on failure.
        """
        print(f"Generating music for prompt: '{prompt}'")

        output_dir = os.path.join(self.project_path, "audio", "music")
        os.makedirs(output_dir, exist_ok=True)

        output_filename = f"music_{prompt.replace(' ', '_')[:20]}.wav"
        output_filepath = os.path.join(output_dir, output_filename)

        command = [
            sys.executable,
            self.wrapper_script,
            "--prompt", prompt,
            "--duration", str(duration_seconds),
            "--output_path", output_filepath
        ]

        print(f"Executing MusicGen command: {' '.join(command)}")

        try:
            # This is the actual command execution.
            process = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
                cwd=self.script_dir,
                timeout=300 # 5-minute timeout for music generation
            )
            print("MusicGen process completed.")
            print(f"MusicGen STDOUT: {process.stdout}")

            if os.path.exists(output_filepath):
                print(f"Successfully generated music track: {output_filepath}")
                return output_filepath
            else:
                print("ERROR: MusicGen script ran, but the output file was not created.")
                return None

        except FileNotFoundError:
            print(f"ERROR: The python executable or the MusicGen wrapper script was not found.")
            raise
        except subprocess.CalledProcessError as e:
            print(f"ERROR: MusicGen execution failed with return code {e.returncode}.")
            print(f"Stderr: {e.stderr}")
            print(f"Stdout: {e.stdout}")
            return None
        except subprocess.TimeoutExpired:
            print("ERROR: MusicGen execution timed out.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred while running MusicGen: {e}")
            return None