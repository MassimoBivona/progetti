# AI Creative Agent - A Jules-Native Toolkit

## 1. Overview

This project is a **Jules-native toolkit** for generating a complete, local multimedia ecosystem from a single text prompt. It is designed to be operated directly by me, Jules, to transform a creative idea into a rich set of assets.

This toolkit is fully modular and relies on local, uncensored AI models. It provides all the necessary scripts and modules for me to generate:
-   **Narrative Content:** Plots, character profiles, and world lore via local LLMs.
-   **Visuals:** Concept art and scene illustrations via a local Stable Diffusion API.
-   **Video Clips:** Animated scenes using the Fooocus + FramePack pipeline.
-   **Audio:** Background music and voiceovers using the provided functional wrappers for MusicGen and Coqui TTS.
-   **3D Models:** Printable STL files via a command-line wrapper for a 2D-to-3D model.

The core of this project is a **Jules Workflow**, a master plan that I will execute step-by-step, using the provided components as my tools and pausing for user approval at each stage.

## 2. Architecture: A Toolkit for Jules

The project is no longer a standalone application. It is a structured set of tools for me to use.

-   `configs/AI_CREATIVE_AGENT_OFFLINE.yml`: My configuration file. I will read this to get API endpoints and paths to your local model installations.
-   `modules/`: My toolbox. Each module contains the core Python logic for a specific task (e.g., `text_generator`, `image_generator`). I will import and use these classes directly.
-   `scripts/`: My command-line interfaces. These are functional, executable wrappers (`run_musicgen.py`, `run_tts.py`) that I will call using `run_in_bash_session` to interact with complex models.
-   `outputs/`: The directory where I will save all generated assets, organized by project.
-   `README.md` (This file): My master plan and workflow document.

## 3. Setup Instructions (Windows 11 Pro)

This is the setup required on your local machine for me to be able to execute the workflow.

### 3.1. Core Toolkit Setup

1.  **Clone the repository** and navigate into the `AI_Creative_Agent` directory.
2.  **Create a Python virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    pip install -r requirements.txt
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
    pip install TTS transformers scipy
    ```
    *(Note: The extra dependencies are for the new wrapper scripts.)*

### 3.2. Local Model & API Setup

You must have the following local models installed and running for me to connect to them.

-   **Text (LLM API):** Run a local LLM (e.g., Llama3 via Oobabooga) with an OpenAI-compatible API enabled.
-   **Image (Stable Diffusion API):** Run a local instance of Stable Diffusion (e.g., ComfyUI) with its API enabled.
-   **Video (Fooocus & FramePack):** Install these tools. I will execute them via the command line.
-   **3D Model (Instant3D):** Install a 2D-to-3D tool that can be run from the command line. You will need to create a simple `run_instant3d.py` wrapper for it, similar to the audio scripts.

### 3.3. **Crucial Configuration**

Open `configs/AI_CREATIVE_AGENT_OFFLINE.yml` and update all paths and endpoints to match your system.

-   **API Endpoints:** Set the correct URLs for your text and image model APIs.
-   **Executable Paths:**
    -   `fooocus.executable_path`: Full path to your Fooocus `launch.py`.
    -   `framepack.executable_path`: Full path to your FramePack `main.py` or equivalent.
    -   `musicgen.wrapper_script`: **Update this to point to `scripts/run_musicgen.py` in this project.**
    -   `voice.wrapper_script`: **Update this to point to `scripts/run_tts.py` in this project.**
    -   `3d.wrapper_script`: Path to your `run_instant3d.py` wrapper.

## 4. The Jules Workflow (Master Plan)

This is the plan I will follow. I will perform each step, save the outputs, and then request your approval before proceeding to the next.

**Initial State:** User has provided an initial prompt.

1.  **Step 1: Concept Refinement**
    -   **Action:** I will use the `text_generator` module to call the LLM and expand the user's prompt into a detailed concept document using AZR/DeepConf reasoning.
    -   **Output:** `outputs/<project>/text/01_refined_concept.txt`.
    -   **Request User Approval.**

2.  **Step 2: Core Content Generation**
    -   **Action:** I will use the `text_generator` module to produce the plot, character profiles, and lore based on the refined concept.
    -   **Output:** `02_plot.txt`, `03_character_profiles.txt`, `04_lore.txt`.
    -   **Request User Approval.**

3.  **Step 3: Visual Development**
    -   **Action:** I will use the `image_generator` module to create concept art for the main character and a key environment.
    -   **Output:** `outputs/<project>/images/01_main_character_concept.png`, `02_environment_concept.png`.
    -   **Request User Approval.**

4.  **Step 4: Scriptwriting**
    -   **Action:** I will use the `text_generator` module to write a script for the first scene.
    -   **Output:** `outputs/<project>/text/05_script_scene_1.txt`.
    -   **Request User Approval.**

5.  **Step 5: Video Clip Production**
    -   **Action:**
        1.  I will call the `video_generator`'s `FooocusInterface` to generate a high-quality starting frame based on the script.
        2.  I will then call the `FramePackManager` to animate this frame into a short video clip.
    -   **Output:** `outputs/<project>/videos/clips/clip_...mp4`.
    -   **Request User Approval.**

6.  **Step 6: Audio Production**
    -   **Action:**
        1.  I will execute `scripts/run_musicgen.py` with a prompt like "epic fantasy score" to create background music.
        2.  I will execute `scripts/run_tts.py`, providing a line from the script and a path to a reference voice WAV file, to generate a voiceover.
    -   **Output:** `outputs/<project>/audio/music/music.wav`, `outputs/<project>/audio/voices/voiceover.wav`.
    -   **Request User Approval.**

7.  **Step 7: 3D Model Creation (If enabled)**
    -   **Action:** I will execute the user-provided wrapper for the 3D model generator, using the character concept art as input.
    -   **Output:** `outputs/<project>/3d_models/character.stl`.
    -   **Request User Approval.**

I will follow this plan precisely, providing a truly interactive and human-supervised creative process.