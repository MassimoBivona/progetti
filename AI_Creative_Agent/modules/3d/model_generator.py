import subprocess
import os
import sys

class ModelGenerator:
    """
    A wrapper to run a 2D-to-3D model generator like Instant3D
    via a command-line script.
    """
    def __init__(self, config, project_path, project_data):
        """
        Initializes the ModelGenerator.

        Args:
            config (dict): The 3d model configuration section.
            project_path (str): The path to the current project's output directory.
            project_data (dict): The shared project data.
        """
        self.wrapper_script = config.get('wrapper_script')
        if not self.wrapper_script or not os.path.exists(self.wrapper_script):
            raise FileNotFoundError(f"3D model generator wrapper script not found at: {self.wrapper_script}")
        self.project_path = project_path
        self.project_data = project_data
        self.script_dir = os.path.dirname(self.wrapper_script)

    def generate_3d_model(self, input_image_path, output_filename):
        """
        Generates a 3D model from a single input image.

        Args:
            input_image_path (str): The path to the source 2D image.
            output_filename (str): The desired output filename (e.g., 'character.stl').

        Returns:
            str: The path to the generated 3D model file, or None on failure.
        """
        print(f"Generating 3D model from image: {os.path.basename(input_image_path)}")

        output_dir = os.path.join(self.project_path, "3d_models")
        os.makedirs(output_dir, exist_ok=True)

        output_filepath = os.path.join(output_dir, output_filename)

        command = [
            sys.executable,
            self.wrapper_script,
            "--input_image", input_image_path,
            "--output_path", output_filepath
        ]

        print(f"Executing 3D generator command: {' '.join(command)}")

        try:
            # This is the actual command execution.
            process = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
                cwd=self.script_dir,
                timeout=600 # 10-minute timeout for 3D model generation
            )
            print("3D generator process completed.")
            print(f"3D generator STDOUT: {process.stdout}")

            if os.path.exists(output_filepath):
                print(f"Successfully generated 3D model: {output_filepath}")
                return output_filepath
            else:
                print("ERROR: 3D generator script ran, but the output file was not created.")
                return None

        except FileNotFoundError:
            print(f"ERROR: The python executable or the 3D generator wrapper script was not found.")
            raise
        except subprocess.CalledProcessError as e:
            print(f"ERROR: 3D model generation failed with return code {e.returncode}.")
            print(f"Stderr: {e.stderr}")
            print(f"Stdout: {e.stdout}")
            return None
        except subprocess.TimeoutExpired:
            print("ERROR: 3D model generation timed out.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred while running 3D model generation: {e}")
            return None

    def run(self, step_config):
        """
        The main execution method called by the agent orchestrator.
        """
        step_name = step_config['name']
        if step_name == "3D Model Creation":
            print("--- Starting 3D Model Creation ---")

            # Find a suitable source image (e.g., the main character concept)
            source_image_path = None
            # A more robust check for a generated character concept art
            for asset_key, asset_path in self.project_data['assets'].items():
                if isinstance(asset_path, str) and 'character_concept' in asset_path:
                    source_image_path = asset_path
                    break

            if not source_image_path or not os.path.exists(source_image_path):
                 print("WARNING: Could not find a suitable source image for 3D model generation. Skipping.")
                 # Trying to find any other image as a fallback
                 for asset_key, asset_path in self.project_data['assets'].items():
                    if isinstance(asset_path, str) and asset_path.endswith('.png'):
                        source_image_path = asset_path
                        print(f"Fallback: Using image {source_image_path}")
                        break

            if not source_image_path:
                print("ERROR: No suitable PNG image found in assets to generate a 3D model from. Skipping step.")
                return "skipped"

            model_path = self.generate_3d_model(source_image_path, "main_character_model.stl")
            if model_path:
                self.project_data['assets']['3d_model_character'] = model_path
            else:
                return "failure"

        else:
            print(f"Warning: 3D generation step '{step_name}' is not recognized.")

        return "success"

def execute_step(agent_config, step_config, project_path, project_data):
    """
    Entry point function for the agent to call.
    """
    try:
        model_generator = ModelGenerator(agent_config['models']['3d'], project_path, project_data)
        return model_generator.run(step_config)
    except FileNotFoundError as e:
        print(f"Skipping 3D model generation due to incorrect configuration: {e}")
        return "skipped"
    except Exception as e:
        print(f"A critical error occurred in the 3D module: {e}")
        return "failure"