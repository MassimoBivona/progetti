import os
import sys
import json
import traceback

# This allows the core to import its tools from other packages
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent_repository.reasoning.wrapper import ReasoningEngine
from agent_repository.image_gen.wrapper import ImageGenerator

class AutonomousCore:
    """
    The orchestrator for Project Phoenix. It gets a plan from the real LLM
    and executes the core pipeline of generating a real image.
    """
    def __init__(self):
        print("[Phoenix Core] Initializing...")
        # For this minimal pipeline, we only need these two real tools.
        self.planner = ReasoningEngine()
        self.artist = ImageGenerator()
        print("[Phoenix Core] Brain and Artist are ready.")

    def _resolve_arg(self, arg_placeholder: str, context: dict):
        """A simple resolver for placeholders like '<prompt>'."""
        key = arg_placeholder.strip('<>')
        return context.get(key, None)

    def execute_idea(self, idea: str):
        """
        Main generator for the idea-to-real-image pipeline.
        """
        log_history = "[Phoenix] Venture Started.\n"
        execution_context = {}
        yield {"log": log_history, "status": "running"}

        # --- Step 1: Get Strategic Plan from the LLM ---
        log_history += "Consulting the creative brain (Mixtral) for a prompt...\n"
        yield {"log": log_history, "status": "running"}

        # The ReasoningEngine now returns a dictionary with a simple plan
        plan_dict = self.planner.execute(idea=idea)
        if "error" in plan_dict:
            log_history += f"CRITICAL FAILURE: The LLM failed to generate a valid plan. Reason: {plan_dict['error']}\n"
            yield {"log": log_history, "status": "failed"}
            return

        # In this minimal version, the plan is just the prompt
        execution_context['prompt'] = plan_dict.get('prompt', 'A default prompt if LLM fails')
        log_history += f"Brain has generated the creative prompt: '{execution_context['prompt']}'\n"
        yield {"log": log_history, "status": "running", "prompt": execution_context['prompt']}

        # --- Step 2: Execute Image Generation ---
        log_history += "Engaging the Concept Artist (JuggernautXL)...\n"
        yield {"log": log_history, "status": "running", "prompt": execution_context['prompt']}

        try:
            image_path = self.artist.execute(prompt=execution_context['prompt'])
            execution_context['image_path'] = image_path
            log_history += "Artist has completed the work.\n"
            yield {"log": log_history, "status": "complete", "image_path": image_path, "prompt": execution_context['prompt']}
        except Exception:
            error_details = traceback.format_exc()
            log_history += f"CRITICAL FAILURE during image generation: {error_details}\n"
            yield {"log": log_history, "status": "failed"}
            return

        print("[Phoenix Core] Pipeline complete.")