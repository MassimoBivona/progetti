import subprocess
import os
import sys
import base64

class FooocusInterface:
    """
    A wrapper to run Fooocus via the command line to generate a single image.
    This is intended to create the initial frame for a video sequence.
    """
    def __init__(self, executable_path):
        """
        Initializes the Fooocus interface.

        Args:
            executable_path (str): The full path to the Fooocus launch script (e.g., 'C:/Fooocus/launch.py').
        """
        if not os.path.exists(executable_path):
            raise FileNotFoundError(f"Fooocus executable not found at: {executable_path}")
        self.executable_path = executable_path
        self.fooocus_dir = os.path.dirname(self.executable_path)

    def generate_initial_frame(self, prompt, output_path):
        """
        Generates a single image using Fooocus.

        Args:
            prompt (str): The text prompt for image generation.
            output_path (str): The directory where the image should be saved.

        Returns:
            str: The path to the generated image, or None if generation failed.
        """
        print(f"Starting Fooocus to generate initial frame for prompt: '{prompt[:80]}...'")

        # The command-line arguments for Fooocus can be complex and may require a specific
        # fork or a wrapper script to handle them robustly. This is a plausible implementation.
        # It assumes Fooocus is configured to exit after generating one image when a prompt is passed.

        # Define the default Fooocus output directory to find the generated file.
        default_output_dir = os.path.join(self.fooocus_dir, "outputs")
        os.makedirs(default_output_dir, exist_ok=True)

        command = [
            sys.executable,  # The python interpreter
            self.executable_path,
            "--prompt", prompt,
            "--output-path", default_output_dir,
            "--headless" # Assumed headless/exit-after-done flag
        ]

        print(f"Executing Fooocus command: {' '.join(command)}")

        try:
            # This is the actual command execution. It will only work in an environment
            # where Fooocus is installed and correctly configured at the specified path.
            process = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
                cwd=self.fooocus_dir,
                timeout=300 # 5-minute timeout for image generation
            )
            print("Fooocus process completed.")
            print(f"Fooocus STDOUT: {process.stdout}")

            # After execution, find the newest file in the Fooocus output directory
            files = [os.path.join(default_output_dir, f) for f in os.listdir(default_output_dir) if f.endswith('.png')]
            if not files:
                print("ERROR: Fooocus ran, but no output PNG file was found in its directory.")
                return None

            latest_file = max(files, key=os.path.getctime)

            # Move the generated file to the desired project output path
            os.makedirs(output_path, exist_ok=True)
            final_path = os.path.join(output_path, os.path.basename(latest_file))
            os.rename(latest_file, final_path)

            print(f"Successfully generated and moved initial frame to: {final_path}")
            return final_path

        except FileNotFoundError:
            print(f"ERROR: The python executable or the Fooocus script was not found.")
            raise
        except subprocess.CalledProcessError as e:
            print(f"ERROR: Fooocus execution failed with return code {e.returncode}.")
            print(f"Stderr: {e.stderr}")
            print(f"Stdout: {e.stdout}")
            return None
        except subprocess.TimeoutExpired:
            print("ERROR: Fooocus execution timed out.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred while running Fooocus: {e}")
            return None