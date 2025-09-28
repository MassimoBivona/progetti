import os
from .fooocus_interface import FooocusInterface
from .framepack_manager import FramePackManager

class VideoGenerator:
    """
    Orchestrates the video generation pipeline using Fooocus and FramePack.
    """
    def __init__(self, config, project_path, project_data):
        """
        Initializes the video generator.
        """
        self.config = config
        self.project_path = project_path
        self.project_data = project_data

        try:
            self.fooocus = FooocusInterface(self.config['fooocus']['executable_path'])
            self.framepack = FramePackManager(self.config['framepack']['executable_path'])
        except FileNotFoundError as e:
            print(f"ERROR: Could not initialize video modules. {e}")
            raise  # Stop execution if paths are incorrect

    def _get_scene_description(self):
        """
        Generates a textual description for a scene to be visualized.
        In a real implementation, this would use the LLM to parse the script.
        For now, it returns a hardcoded value based on available assets.
        """
        if self.project_data['assets'].get('script_scene_1'):
            return "A cinematic shot of the main hero entering a dark, mysterious cave, as described in the script. Epic fantasy style."
        return "A beautiful fantasy landscape, digital art."

    def run(self, step_config):
        """
        The main execution method called by the agent orchestrator.
        """
        step_name = step_config['name']

        if step_name == "Video Clip Production":
            print("--- Starting Video Clip Production ---")

            # 1. Define the output directory for this video
            video_output_dir = os.path.join(self.project_path, "videos")
            os.makedirs(video_output_dir, exist_ok=True)

            # 2. Get a description for the scene to generate
            image_prompt = self._get_scene_description()

            # 3. Generate the initial frame with Fooocus
            initial_frame_path = self.fooocus.generate_initial_frame(
                prompt=image_prompt,
                output_path=os.path.join(video_output_dir, "initial_frames")
            )

            if not initial_frame_path:
                print("ERROR: Failed to generate initial frame with Fooocus. Aborting video generation.")
                return "failure"

            # 4. Define motion and generate the video with FramePack
            motion_prompt = "slow camera zoom in, subtle wind effect"
            video_clip_path = self.framepack.generate_video_clip(
                initial_frame_path=initial_frame_path,
                motion_prompt=motion_prompt,
                output_path=os.path.join(video_output_dir, "clips")
            )

            if not video_clip_path:
                print("ERROR: Failed to generate video clip with FramePack.")
                return "failure"

            # 5. Record the asset path in the project data
            asset_name = f"video_clip_{os.path.basename(video_clip_path)}"
            self.project_data['assets'][asset_name] = video_clip_path
            print(f"--- Video Clip Production Finished ---")

        else:
            print(f"Warning: Video generation step '{step_name}' is not recognized.")

        return "success"


def execute_step(agent_config, step_config, project_path, project_data):
    """
    Entry point function for the agent to call.
    """
    try:
        video_generator = VideoGenerator(agent_config['models']['video'], project_path, project_data)
        return video_generator.run(step_config)
    except FileNotFoundError:
        print("Skipping video generation due to incorrect configuration.")
        return "skipped" # Return 'skipped' if tools aren't configured
    except Exception as e:
        print(f"A critical error occurred in the video module: {e}")
        return "failure"