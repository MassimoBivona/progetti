import os
from PIL import Image
import sys

# Ensure the root directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.tool_interface import ToolInterface

class ImageGenerator(ToolInterface):
    """
    A tool for generating an image from a text prompt using Fooocus.
    """
    def __init__(self):
        """Initializes the ImageGenerator."""
        # In a real implementation, this would load the Fooocus models.
        pass

    @property
    def name(self) -> str:
        return "image_generator"

    @property
    def description(self) -> str:
        return "Generates a single, high-quality image from a descriptive text prompt."

    def execute(self, prompt: str, **kwargs) -> str:
        """
        Generates an image based on a text prompt.

        Args:
            prompt (str): The text prompt to generate the image from.
            **kwargs: Can include `output_dir` for custom output locations.

        Returns:
            str: The file path of the generated image.
        """
        output_dir = kwargs.get("output_dir", "image_gen/output")
        print(f"[{self.name}] Generating an image for the prompt: '{prompt}'")

        # --- Simulation of the Fooocus image generation process ---
        os.makedirs(output_dir, exist_ok=True)

        safe_filename = "".join(c for c in prompt if c.isalnum() or c in (' ', '_')).rstrip()
        image_filename = f"{safe_filename.replace(' ', '_')[:30]}.png"
        final_path = os.path.join(output_dir, image_filename)

        # Create a dummy image to represent the output
        placeholder_image = Image.new('RGB', (1024, 1024), color='darkgreen')
        placeholder_image.save(final_path)
        # --- End of simulation ---

        print(f"[{self.name}] Image generation complete. Output saved to: {final_path}")
        return final_path