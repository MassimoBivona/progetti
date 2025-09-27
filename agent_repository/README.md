# 🔥 Project Phoenix: The Autonomous Creative Agent (MVP)

Welcome to Project Phoenix. This repository contains a real, working prototype of an autonomous creative agent. It's designed to demonstrate a core, end-to-end pipeline: taking a high-level user idea, using a powerful local LLM to brainstorm a creative prompt, and then using a state-of-the-art image generation model to create a high-quality piece of art.

This project is built on the **"Keystone" architecture**: I, the AI agent, have built the entire engine, and I am now handing you, the user, the final "keystone" to complete it.

---

## How It Works: The Idea-to-Image Pipeline

This Minimum Viable Product (MVP) proves the core concept with a two-step process:

1.  **The Brain (`LLMService`):** When you provide an idea, the agent first consults its "brain"—a powerful, locally-run Large Language Model (`Nous-Hermes-2 Mixtral 8x7B`). This LLM acts as a creative partner, brainstorming and generating a detailed, artistic prompt based on your initial concept.

2.  **The Artist (`ImageGenerator`):** The generated prompt is then passed to the "artist"—a high-performance image generation model (`JuggernautXL v8`). This model interprets the artistic prompt and creates the final, high-resolution image.

Both of these core components are designed to be **auto-provisioning**. The first time you run the application, the agent will automatically download the necessary models (be aware, this is a large download of over 35 GB).

---

## 🔑 The Keystone: Installing the LLM Brain

This project is fully functional *except* for one component that **only you can install** due to system-specific hardware compilation: the LLM engine itself.

I have built everything else. To bring the agent's brain to life, please follow these two steps precisely.

### Step 1: Install Dependencies
First, install all the other required Python libraries using the `requirements.txt` file.
```bash
pip install -r agent_repository/requirements.txt
```

### Step 2: Install the Brain (with GPU Acceleration)
Now, install `llama-cpp-python` with the correct flags for your powerful NVIDIA GPU. This command will compile the library to use your CUDA cores, providing maximum performance. **This is the most important step.**

**Copy and paste this exact command into your terminal:**
```bash
CMAKE_ARGS="-DGGML_CUDA=on" FORCE_CMAKE=1 pip install llama-cpp-python --no-cache-dir
```

---

## Running the Agent

Once the installation is complete, you can run the agent. Because we have built this as a professional Python package, you must run it as a module from the **root directory of the project** (the one containing `setup.py` and `agent_repository`).

**Use this exact command to launch the Gradio UI:**
```bash
python -m agent_repository.ui.app
```

Navigate to the local URL provided in your terminal (e.g., `http://127.0.0.1:7860`).

1.  The first time you run the app, the agent will download the required models. Please be patient, as this can take some time. Monitor the progress in your terminal.
2.  Once loaded, enter your creative idea into the textbox.
3.  Click "Generate".
4.  Watch the live log as the agent first uses the LLM to generate a prompt, and then uses the image model to create your artwork.

---

## Project Structure

-   `setup.py`: Makes this project a professional, installable Python package.
-   `agent_repository/`: The main package containing all the agent's logic.
    -   `core/`: Contains the `LLMService` (the brain) and the `DownloadManager`.
    -   `image_gen/`: Contains the `ImageGenerator` (the artist).
    -   `reasoning/`: The interface to the `LLMService`.
    -   `ui/`: Contains the Gradio web interface.
    -   `models/`: The directory where the downloaded AI models will be stored.