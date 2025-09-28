import subprocess
import os
import sys

class FramePackManager:
    """
    A wrapper to run FramePack via the command line to generate a video clip
    from an initial frame.
    """
    def __init__(self, executable_path):
        """
        Initializes the FramePack manager.

        Args:
            executable_path (str): The full path to the FramePack main script (e.g., 'C:/FramePack/main.py').
        """
        if not os.path.exists(executable_path):
            raise FileNotFoundError(f"FramePack executable not found at: {executable_path}")
        self.executable_path = executable_path
        self.framepack_dir = os.path.dirname(self.executable_path)

    def generate_video_clip(self, initial_frame_path, motion_prompt, output_path):
        """
        Generates a video clip from a starting image.

        Args:
            initial_frame_path (str): The path to the starting image.
            motion_prompt (str): A text prompt describing the desired motion.
            output_path (str): The directory where the final video should be saved.

        Returns:
            str: The path to the generated video, or None if generation failed.
        """
        print(f"Starting FramePack to generate video from: {os.path.basename(initial_frame_path)}")
        print(f"Motion prompt: '{motion_prompt}'")

        os.makedirs(output_path, exist_ok=True)
        # Define a predictable output filename
        output_filename = f"clip_{os.path.splitext(os.path.basename(initial_frame_path))[0]}.mp4"
        final_video_path = os.path.join(output_path, output_filename)

        command = [
            sys.executable,
            self.executable_path,
            "--input_image", initial_frame_path,
            "--motion_prompt", motion_prompt,
            "--output_path", final_video_path, # Pass the full file path
            "--num_frames", "24"
        ]

        print(f"Executing FramePack command: {' '.join(command)}")

        try:
            # This is the actual command execution.
            process = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
                cwd=self.framepack_dir,
                timeout=600 # 10-minute timeout for video generation
            )
            print("FramePack process completed.")
            print(f"FramePack STDOUT: {process.stdout}")

            if os.path.exists(final_video_path):
                print(f"Successfully generated video clip: {final_video_path}")
                return final_video_path
            else:
                print("ERROR: FramePack ran, but the output video file was not created at the expected path.")
                return None

        except FileNotFoundError:
            print(f"ERROR: The python executable or the FramePack script was not found.")
            raise
        except subprocess.CalledProcessError as e:
            print(f"ERROR: FramePack execution failed with return code {e.returncode}.")
            print(f"Stderr: {e.stderr}")
            print(f"Stdout: {e.stdout}")
            return None
        except subprocess.TimeoutExpired:
            print("ERROR: FramePack execution timed out.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred while running FramePack: {e}")
            return None