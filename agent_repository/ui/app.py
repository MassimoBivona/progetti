import gradio as gr
import os
import sys

# This allows the app to import from the project's packages
# Run this app from the root directory: `python -m agent_repository.ui.app`
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent_repository.core.reasoner import AutonomousCore

def create_phoenix_ui():
    """Defines the Gradio UI for the Project Phoenix MVP."""

    with gr.Blocks(theme=gr.themes.Soft(), title="Project Phoenix Agent") as demo:
        gr.Markdown("# 🔥 Project Phoenix: Idea-to-Image")
        gr.Markdown("A real, working prototype. Provide an idea, and the agent will use a real LLM to generate a prompt, then use a real image model to create the art.")

        with gr.Row():
            idea_input = gr.Textbox(label="Your Creative Idea", scale=4, placeholder="e.g., A wise old dragon guarding a celestial library")
            start_button = gr.Button("🔥 Generate", variant="primary", scale=1)

        gr.Markdown("## Production Log & Final Artwork")

        progress_bar = gr.Progress(track_tqdm=True)

        with gr.Row():
            with gr.Column(scale=1):
                log_output = gr.Textbox(label="Live Log", lines=15, interactive=False)
                prompt_output = gr.Textbox(label="LLM-Generated Prompt", lines=5, interactive=False)
            with gr.Column(scale=2):
                image_output = gr.Image(label="Final Artwork", interactive=False, height=512)

        # --- Backend Logic Connection ---
        def run_phoenix_pipeline(idea, progress=gr.Progress(track_tqdm=True)):
            """Calls the AutonomousCore and streams the results to the UI."""
            core = AutonomousCore()

            asset_context = {}
            # This loop will stream updates from the core
            for i, state in enumerate(core.execute_idea(idea)):
                asset_context.update(state)

                log = asset_context.get("log", "")
                prompt = asset_context.get("prompt")
                img_path = asset_context.get("image_path")

                # A simple way to track progress without a defined number of steps
                progress(i / 10, desc=log.strip().split('\n')[-1])

                yield log, prompt, img_path

            # Final update
            progress(1, desc="Complete!")
            yield asset_context.get("log"), asset_context.get("prompt"), asset_context.get("image_path")


        start_button.click(
            fn=run_phoenix_pipeline,
            inputs=[idea_input],
            outputs=[log_output, prompt_output, image_output]
        )

    return demo

if __name__ == "__main__":
    # To run this app correctly, navigate to the project root
    # and run: `python -m agent_repository.ui.app`
    ui = create_phoenix_ui()
    ui.launch()