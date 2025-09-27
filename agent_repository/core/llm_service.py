import os
import json
from agent_repository.core.download_manager import download_file

# This is the "Keystone" logic: we try to import the brain, but if it fails,
# the rest of the application can still run in a high-fidelity simulation mode.
try:
    from llama_cpp import Llama
    LLAMA_CPP_AVAILABLE = True
except ImportError:
    LLAMA_CPP_AVAILABLE = False
    print("[LLM Service WARNING] `llama-cpp-python` is not installed. The LLM brain will be simulated.")
    print("                       To enable the real brain, please install it with GPU support using the command in the README.")


class LLMService:
    """
    A dedicated service to manage and interact with the local LLM.
    It handles model downloading and gracefully falls back to a simulation
    if the required `llama-cpp-python` library is not installed.
    """
    def __init__(self, model_filename="nous-hermes-2-mixtral-8x7b-dpo.Q5_K_M.gguf"):
        self.model_url = f"https://huggingface.co/TheBloke/Nous-Hermes-2-Mixtral-8x7B-DPO-GGUF/resolve/main/{model_filename}"
        self.model_path = os.path.abspath(f"agent_repository/models/checkpoints/{model_filename}")
        self.llm = None

        print("[LLM Service] Initializing...")
        self._ensure_model_is_downloaded()

        if LLAMA_CPP_AVAILABLE:
            self._load_model()
        else:
            # The warning is printed at import time.
            pass

    def _ensure_model_is_downloaded(self):
        """Checks if the model exists and downloads it if necessary."""
        download_file(self.model_url, self.model_path, "Nous-Hermes-2-Mixtral-8x7B GGUF")

    def _load_model(self):
        """Loads the GGUF model into memory with GPU offloading."""
        if self.llm is None:
            print("[LLM Service] Loading Mixtral model into VRAM... This may take a moment.")
            try:
                self.llm = Llama(
                    model_path=self.model_path,
                    n_ctx=32768,
                    n_gpu_layers=-1, # Offload all layers to GPU
                    n_batch=512,
                    verbose=True,
                )
                print("[LLM Service] Mixtral model loaded successfully.")
            except Exception as e:
                print(f"[LLM Service] CRITICAL ERROR: Failed to load LLM. Is CUDA set up correctly? Error: {e}")
                self.llm = None

    def generate_plan(self, idea: str) -> str:
        """
        Generates a structured business plan JSON. Uses the real LLM if available,
        otherwise returns a high-quality simulated plan.
        """
        if self.llm:
            # --- REAL LLM INFERENCE ---
            prompt_template = """<|im_start|>user
You are a world-class AI CEO. Your task is to take a high-level idea and formulate a complete, structured production plan as a single, valid JSON object. Do not add any text before or after the JSON object.

The plan must have a single key "production_plan" which is a list of steps. Each step is a dictionary with "tool", "args", and "output_key".

Example for a video:
{
  "production_plan": [
    { "tool": "concept_artist", "args": { "prompt": "a detailed prompt" }, "output_key": "image_path" },
    { "tool": "film_director", "args": { "image_path": "<image_path>" }, "output_key": "video_path" }
  ]
}

Here is the idea: "{idea}"<|im_end|>
<|im_start|>assistant
"""
            prompt = prompt_template.format(idea=idea)
            print(f"[LLM Service] Prompting Mixtral to generate a business plan for: '{idea}'")
            try:
                response = self.llm(prompt, max_tokens=2048, stop=["<|im_end|>"], echo=False, temperature=0.7)
                return response['choices'][0]['text']
            except Exception as e:
                print(f"[LLM Service] ERROR: Failed to get response from LLM. Error: {e}")
                return '{"error": "Failed to generate a plan from the LLM."}'
        else:
            # --- SIMULATED LLM OUTPUT (FALLBACK) ---
            print(f"[LLM Service] Generating SIMULATED plan for: '{idea}'")
            simulated_plan = {
                "production_plan": [
                    {"tool": "concept_artist", "args": {"prompt": f"A cinematic, high-detail promotional image for a story about '{idea}'"}, "output_key": "image_path"},
                    {"tool": "film_director", "args": {"image_path": "<image_path>", "prompts": ["a slow zoom in, dramatic lighting"]}, "output_key": "video_path"}
                ]
            }
            return json.dumps(simulated_plan, indent=2)