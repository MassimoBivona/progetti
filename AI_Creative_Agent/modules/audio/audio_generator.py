import os
from .music_generator import MusicGenerator
from .voice_generator import VoiceGenerator

class AudioOrchestrator:
    """
    Orchestrates the audio production step by calling the specific
    music and voice generation modules.
    """
    def __init__(self, config, project_path, project_data):
        self.config = config
        self.project_path = project_path
        self.project_data = project_data
        self.music_generator = None
        self.voice_generator = None

        # Safely initialize sub-modules
        try:
            if 'musicgen' in self.config:
                self.music_generator = MusicGenerator(self.config['musicgen'], self.project_path)
        except FileNotFoundError as e:
            print(f"WARNING: Could not initialize MusicGenerator: {e}. Music generation will be skipped.")

        try:
            if 'voice' in self.config:
                self.voice_generator = VoiceGenerator(self.config['voice'], self.project_path)
        except FileNotFoundError as e:
            print(f"WARNING: Could not initialize VoiceGenerator: {e}. Voice generation will be skipped.")

    def run(self, step_config):
        step_name = step_config['name']

        if step_name == "Audio Production":
            print("--- Starting Audio Production ---")

            # 1. Generate background music
            if self.music_generator:
                music_prompt = "Epic and adventurous fantasy score for a movie scene."
                music_path = self.music_generator.generate_music(music_prompt)
                if music_path:
                    self.project_data['assets']['background_music'] = music_path

            # 2. Generate voiceover for a script line
            if self.voice_generator and self.project_data['assets'].get('script_scene_1'):
                # This is a simplified example. A real implementation would parse the script.
                first_line = "The hero entered the dark cave, a flickering torch in hand."
                voice_path = self.voice_generator.generate_voiceover(first_line, "narrator", "scene_1_line_1")
                if voice_path:
                    self.project_data['assets']['voiceover_scene_1_line_1'] = voice_path

            print("--- Audio Production Finished ---")

        return "success"


def execute_step(agent_config, step_config, project_path, project_data):
    """
    Entry point function for the agent to call.
    """
    try:
        # The 'audio' model config is passed down
        orchestrator = AudioOrchestrator(agent_config['models']['audio'], project_path, project_data)
        return orchestrator.run(step_config)
    except Exception as e:
        print(f"A critical error occurred in the audio orchestrator module: {e}")
        return "failure"