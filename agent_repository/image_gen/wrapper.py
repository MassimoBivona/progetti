import os
import sys
import torch
from diffusers import StableDiffusionXLPipeline

# Ensure the root directory is in the Python path for package imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent_repository.core.tool_interface import ToolInterface
from agent_repository.core.download_manager import download_file

class ImageGenerator(ToolInterface):
    """
    A tool for generating a high-quality image using a real Stable Diffusion XL model.
    It automatically downloads the required model if it's not present.
    """
    def __init__(self):
        self.model_url = "https://huggingface.co/RunDiffusion/Juggernaut-XL-v8/resolve/main/juggernautXL_v8Rundiffusion.safetensors"
        self.model_path = os.path.abspath("agent_repository/models/checkpoints/juggernautXL_v8Rundiffusion.safetensors")
        self.pipe = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        print(f"[{self.name}] Initializing... Ensuring model exists.")
        download_file(self.model_url, self.model_path, "JuggernautXL v8 Checkpoint")

    @property
    def name(self) -> str:
        return "concept_artist"

    @property
    def description(self) -> str:
        return "Generates a single, high-quality image from a descriptive text prompt using the JuggernautXL model."

    def _load_pipeline(self):
        """Loads the SDXL pipeline into memory if not already loaded."""
        if self.pipe is None:
            print(f"[{self.name}] Loading JuggernautXL pipeline into VRAM... This may take a moment.")
            try:
                self.pipe = StableDiffusionXLPipeline.from_single_file(
                    self.model_path,
                    torch_dtype=torch.float16,
                    use_safetensors=True,
                    variant="fp16"
                ).to(self.device)
                print(f"[{self.name}] Pipeline loaded successfully on {self.device}.")
            except Exception as e:
                print(f"[{self.name}] ERROR: Failed to load SDXL pipeline. Is `diffusers` installed correctly? Error: {e}")
                self.pipe = None # Ensure it remains None on failure

    def execute(self, **kwargs) -> str:
        """
        Generates a real image using the JuggernautXL model.

        Args:
            prompt (str): The text prompt for the image.
            output_dir (str, optional): Directory to save the output.
        """
        prompt = kwargs.get("prompt", "a beautiful fantasy landscape, cinematic lighting, 8k")
        output_dir = kwargs.get("output_dir", "image_gen/output")

        print(f"[{self.name}] Generating image for prompt: '{prompt}'")
        os.makedirs(output_dir, exist_ok=True)

        self._load_pipeline()

        if self.pipe is None:
            return "ERROR: Image generation pipeline could not be loaded."

        # Generate the image
        try:
            with torch.no_grad():
                image = self.pipe(prompt=prompt, num_inference_steps=25).images[0]
        except Exception as e:
            return f"ERROR: Image generation failed during inference. Error: {e}"

        # Save the image
        safe_prompt = "".join(c for c in prompt if c.isalnum() or c in (' ', '_')).rstrip()[:50]
        image_filename = f"{safe_prompt.replace(' ', '_')}.png"
        image_path = os.path.join(output_dir, image_filename)
        image.save(image_path)

        print(f"[{self.name}] Image generation complete. Output saved to: {image_path}")
        return image_path