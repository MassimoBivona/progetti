import requests
import os
import json
from io.file_manager import FileManager

class TextGenerator:
    """
    Handles all text generation tasks by interfacing with a local LLM
    via an OpenAI-compatible API endpoint.
    """
    def __init__(self, config, project_path, project_data):
        """
        Initializes the text generator.

        Args:
            config (dict): The model configuration section from the main config.
            project_path (str): The path to the current project's output directory.
            project_data (dict): The shared state/data of the project.
        """
        self.config = config
        self.project_data = project_data
        self.file_manager = FileManager(project_path)
        self.api_url = f"{self.config['endpoint']}/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.get('api_key', 'no-key')}"
        }

    def _generate(self, prompt, model_override=None):
        """
        Sends a prompt to the local LLM and returns the response.
        """
        model_to_use = model_override if model_override else self.config['generation_model']
        print(f"Sending prompt to LLM (model: {model_to_use})...")

        payload = {
            "model": model_to_use,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 2048
        }

        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload, timeout=120)
            response.raise_for_status()  # Raise an exception for bad status codes

            completion = response.json()
            generated_text = completion['choices'][0]['message']['content']

            print("LLM response received successfully.")
            return generated_text.strip()

        except requests.exceptions.RequestException as e:
            print(f"ERROR: Could not connect to the LLM API at {self.api_url}. Please ensure the local server is running.")
            print(f"Details: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred during text generation: {e}")
            return None

    def run(self, step_config):
        """
        The main execution method called by the agent orchestrator.
        It drives the text generation based on the current workflow step.
        """
        step_name = step_config['name']

        if step_name == "Concept Refinement":
            prompt = f"""
            Initial Idea: "{self.project_data['initial_prompt']}"

            Analyze this idea using AZR (Analyze, Synthesize, Refine) and DeepConf (Deep Confidence) reasoning.
            Expand it into a more robust and compelling concept. Flesh out the core themes, potential plot arcs, and unique selling points.
            The output should be a detailed, structured concept document.
            """
            refined_concept = self._generate(prompt, model_override=self.config['reasoning_model'])
            if refined_concept:
                self.project_data['refined_concept'] = refined_concept
                self.file_manager.save_text("01_refined_concept.txt", refined_concept, asset_type="text")
            else:
                return "failure" # Propagate failure

        elif step_name == "Core Content Generation":
            if not self.project_data.get('refined_concept'):
                print("ERROR: Cannot generate core content without a refined concept.")
                return "failure"

            for sub_step in step_config.get('sub-steps', []):
                if sub_step == "Generate Plot":
                    prompt = f"Based on the following concept, generate a detailed plot outline with three acts.\n\nConcept:\n{self.project_data['refined_concept']}"
                    plot = self._generate(prompt)
                    if plot:
                        self.project_data['assets']['plot'] = self.file_manager.save_text("02_plot.txt", plot, asset_type="text")

                elif sub_step == "Generate Character Profiles":
                    prompt = f"Based on the following concept, create detailed character profiles for the main protagonist, antagonist, and two supporting characters.\n\nConcept:\n{self.project_data['refined_concept']}"
                    profiles = self._generate(prompt)
                    if profiles:
                        self.project_data['assets']['character_profiles'] = self.file_manager.save_text("03_character_profiles.txt", profiles, asset_type="text")

                elif sub_step == "Generate Lore":
                    prompt = f"Based on the following concept, create a lore document for the world, including key locations, history, and magical systems.\n\nConcept:\n{self.project_data['refined_concept']}"
                    lore = self._generate(prompt)
                    if lore:
                        self.project_data['assets']['lore'] = self.file_manager.save_text("04_lore.txt", lore, asset_type="text")

        elif step_name == "Scriptwriting":
            plot_path = self.project_data['assets'].get('plot')
            if not plot_path:
                print("ERROR: Cannot write script without a plot. Please ensure the plot has been generated.")
                return "failure"

            plot_content = self.file_manager.read_text(plot_path)
            if not plot_content:
                print(f"ERROR: Could not read plot content from {plot_path}")
                return "failure"

            prompt = f"Based on the provided plot, write a script for the first major scene.\n\nPlot:\n{plot_content}"
            script = self._generate(prompt)
            if script:
                self.project_data['assets']['script_scene_1'] = self.file_manager.save_text("05_script_scene_1.txt", script, asset_type="text")

        else:
            print(f"Warning: Text generation step '{step_name}' is not recognized by the text module.")

        return "success"


def execute_step(agent_config, step_config, project_path, project_data):
    """
    Entry point function for the agent to call.
    """
    text_generator = TextGenerator(agent_config['models']['text'], project_path, project_data)
    return text_generator.run(step_config)