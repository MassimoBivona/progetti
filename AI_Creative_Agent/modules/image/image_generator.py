import requests
import os
import base64
import json
from io.file_manager import FileManager

class ImageGenerator:
    """
    Handles all image generation tasks by interfacing with a local
    Stable Diffusion API (e.g., Automatic1111).
    """
    def __init__(self, config, project_path, project_data):
        """
        Initializes the image generator.
        """
        self.config = config
        self.project_data = project_data
        self.file_manager = FileManager(project_path)
        self.api_url = self.config['endpoint']
        self.headers = {"Content-Type": "application/json"}

    def _generate(self, prompt, filename):
        """
        Sends a prompt to the Stable Diffusion API and saves the resulting image.
        """
        print(f"Generating image for prompt: '{prompt[:80]}...'")

        # Ensure filename has a .png extension
        if not filename.lower().endswith('.png'):
            filename += '.png'

        payload = {
            "prompt": prompt,
            "negative_prompt": self.config.get('negative_prompt', ''),
            "steps": 25,
            "cfg_scale": 7,
            "width": 1024,
            "height": 1024,
            "sampler_name": "DPM++ 2M Karras",
        }

        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload, timeout=180)
            response.raise_for_status()

            r = response.json()
            if 'images' in r and r['images']:
                image_data = base64.b64decode(r['images'][0])
                filepath = self.file_manager.save_binary(filename, image_data, asset_type="images")
                print(f"Image generated and saved to {filepath}")
                return filepath
            else:
                print("ERROR: Image generation API did not return an image.")
                print("Response:", r)
                return None

        except requests.exceptions.RequestException as e:
            print(f"ERROR: Could not connect to the Image Generation API at {self.api_url}.")
            print(f"Details: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred during image generation: {e}")
            return None

    def run(self, step_config):
        """
        The main execution method called by the agent orchestrator.
        """
        step_name = step_config['name']

        # A helper to create a detailed prompt from the project data
        def create_base_prompt(description):
            base = self.project_data.get('refined_concept', '')
            # A simple summary of the concept
            base_summary = " ".join(base.split()[:100])
            return f"epic fantasy art, cinematic lighting, detailed, high quality. Concept: {base_summary}. Description: {description}"

        if step_name == "Visual Development":
            print("Starting Visual Development...")
            # Generate image for the main character
            character_prompt = "Portrait of the main character, based on character profiles."
            if self.project_data['assets'].get('character_profiles'):
                 # In a real scenario, you'd parse the text to get specific descriptions
                 character_prompt = "Portrait of the main protagonist as described in the project's character profiles. Fantasy setting."

            self._generate(create_base_prompt(character_prompt), "01_main_character_concept.png")

            # Generate image for a key location
            location_prompt = "A key location from the lore, an ancient forest."
            self._generate(create_base_prompt(location_prompt), "02_environment_concept.png")

        elif step_name == "Scene Illustration":
            print("Starting Scene Illustration...")
            if not self.project_data['assets'].get('script_scene_1'):
                print("WARNING: Cannot illustrate a scene without a script. Skipping.")
                return "success" # Not a failure, just can't run

            # This would be more sophisticated, parsing the script for a description.
            scene_prompt = "Illustration of the first scene from the script: a hero entering a dark, mysterious cave."
            self._generate(create_base_prompt(scene_prompt), "03_scene_1_illustration.png")

        elif step_name == "Promotional Material":
            print("Generating promotional material...")
            promo_prompt = "A promotional poster for a new epic fantasy story. Should feature the main character and a dramatic background."
            self._generate(create_base_prompt(promo_prompt), "promo_poster_01.png")

        else:
            print(f"Warning: Image generation step '{step_name}' is not recognized by the image module.")

        return "success"


def execute_step(agent_config, step_config, project_path, project_data):
    """
    Entry point function for the agent to call.
    """
    image_generator = ImageGenerator(agent_config['models']['image'], project_path, project_data)
    return image_generator.run(step_config)