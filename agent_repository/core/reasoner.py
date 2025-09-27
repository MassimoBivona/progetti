import sys
import os
import random

# Ensure the root directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import tool wrappers
from knowledge.manager import KnowledgeManager
from reasoning.wrapper import ReasoningEngine
from image_gen.wrapper import ImageGenerator
from video_gen.wrapper import VideoGenerator

class AutonomousCore:
    """
    The central brain of the agent, enhanced with DeepConf principles.
    It generates multiple plans, evaluates its confidence, and executes the best one
    by interacting with its tools through a standardized interface.
    """
    def __init__(self, num_candidate_plans=3, confidence_threshold=0.7):
        print("[CORE] Initializing AutonomousCore with DeepConf...")
        self.num_candidate_plans = num_candidate_plans
        self.confidence_threshold = confidence_threshold
        self._initialize_tools()
        print("[CORE] Toolbox is ready.")

    def _initialize_tools(self):
        """Loads all available tools, referencing them by their standard names."""
        self.tools = {
            "knowledge_retriever_and_builder": KnowledgeManager(),
            "script_synthesizer": ReasoningEngine(),
            "image_generator": ImageGenerator(),
            "video_generator": VideoGenerator(),
        }

    def _generate_candidate_plans(self, idea: str) -> list:
        """Generates multiple candidate plans to achieve the user's idea."""
        print(f"[CORE-PLAN] Generating {self.num_candidate_plans} candidate plans for idea: '{idea}'")

        # Plan 1: Full, standard pipeline
        plan_1 = [
            {"tool": "knowledge_retriever_and_builder", "args": {"action": "chat", "query": idea}, "output_key": "context"},
            {"tool": "script_synthesizer", "args": {"context": "<context>"}, "output_key": "script"},
            {"tool": "image_generator", "args": {"prompt": "<script.scenes[0].prompt>"}, "output_key": "initial_image_path"},
            {"tool": "video_generator", "args": {"image_path": "<initial_image_path>", "prompts": "<script.scenes[1+].prompt>"}, "output_key": "final_video_path"}
        ]
        # Plan 2: Skips knowledge retrieval, synthesizes directly from the idea
        plan_2 = [
            {"tool": "script_synthesizer", "args": {"context": idea}, "output_key": "script"},
            {"tool": "image_generator", "args": {"prompt": "<script.scenes[0].prompt>"}, "output_key": "initial_image_path"},
            {"tool": "video_generator", "args": {"image_path": "<initial_image_path>", "prompts": "<script.scenes[1+].prompt>"}, "output_key": "final_video_path"}
        ]
        # Plan 3: Low-quality plan, only generates an image
        plan_3 = [{"tool": "image_generator", "args": {"prompt": idea}, "output_key": "final_image"}]

        return [plan_1, plan_2, plan_3]

    def _evaluate_confidence(self, plan: list) -> float:
        """Simulates confidence evaluation based on plan structure."""
        score = 0.0
        if len(plan) > 2 and plan[-1]["tool"] == "video_generator":
            score = 0.9 + random.uniform(-0.05, 0.05)
        elif len(plan) > 1:
            score = 0.6 + random.uniform(-0.05, 0.05)
        else:
            score = 0.4 + random.uniform(-0.05, 0.05)
        return score

    def _resolve_args(self, args: dict, context: dict) -> dict:
        """
        Resolves placeholder arguments with values from the execution context.
        NOTE: This is a simplified resolver for the simulation.
        """
        resolved_args = {}
        for key, value in args.items():
            if isinstance(value, str) and value.startswith('<') and value.endswith('>'):
                placeholder = value.strip('<>')
                if placeholder == 'context':
                    resolved_args[key] = context.get('context')
                elif placeholder == 'initial_image_path':
                    resolved_args[key] = context.get('initial_image_path')
                elif placeholder.startswith('script.'):
                    script = context.get('script', {})
                    if 'scenes[0].prompt' in placeholder:
                        resolved_args[key] = script.get('scenes', [{}])[0].get('prompt', '')
                    elif 'scenes[1+].prompt' in placeholder:
                        resolved_args[key] = [s.get('prompt') for s in script.get('scenes', [])[1:]]
            else:
                resolved_args[key] = value
        return resolved_args

    def _execute_plan(self, plan: list) -> dict:
        """Executes the plan using the standardized ToolInterface."""
        print("[CORE-EXEC] Starting execution of the highest-confidence plan...")
        execution_context = {}
        for i, step in enumerate(plan):
            tool_name = step.get("tool")
            tool = self.tools.get(tool_name)
            if not tool:
                print(f"Error: Tool '{tool_name}' not found. Aborting.")
                return {"error": f"Tool '{tool_name}' not found."}

            print(f"\n[CORE-EXEC] Step {i+1}/{len(plan)}: Executing tool '{tool.name}'...")
            args = self._resolve_args(step.get("args", {}), execution_context)

            try:
                result = tool.execute(**args)
                execution_context[step["output_key"]] = result
            except Exception as e:
                return {"error": f"Execution failed at step {i+1} ({tool.name})", "details": str(e)}
        return execution_context

    def execute_idea(self, idea: str):
        """Main entry point for the DeepConf-enhanced autonomous operation."""
        candidate_plans = self._generate_candidate_plans(idea)
        confident_plans = []
        for plan in candidate_plans:
            score = self._evaluate_confidence(plan)
            if score >= self.confidence_threshold:
                confident_plans.append((plan, score))

        if not confident_plans:
            print("[CORE] No plans met the confidence threshold. Aborting.")
            return "Failed to generate a confident plan."

        best_plan, best_score = max(confident_plans, key=lambda x: x[1])
        print(f"[CORE] Selected best plan with confidence {best_score:.2f}.")

        final_context = self._execute_plan(best_plan)

        print("\n--- Autonomous Execution Summary ---")
        for key, value in final_context.items():
            value_repr = str(value)
            if len(value_repr) > 150: value_repr = f"{value_repr[:150]}..."
            print(f"  - {key}: {value_repr}")

        return final_context.get("final_video_path", "Execution finished.")