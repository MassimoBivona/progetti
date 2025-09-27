# The Autonomous Creative Agent

This repository contains the implementation of a sophisticated, autonomous creative agent. It is designed to take a high-level idea from a user (e.g., "create a video about the Roman Empire") and independently reason, plan, and execute a complex workflow to generate a final creative output.

The agent's architecture is built on a "brain" and a "toolbox" principle, combining multiple cutting-edge AI technologies.

---

## Core Philosophy & Technologies

This agent operates on a four-stage creative process, orchestrated by an autonomous core inspired by **Absolute Zero** and **DeepConf** reasoning principles.

1.  **Knowledge Retrieval (`Memvid`):** The agent first consults its knowledge base to gather context and facts about the user's idea. This knowledge is stored in a highly compressed, searchable video format.
2.  **Reasoning & Scripting (`SpikingBrain`):** Using the retrieved context, the agent's reasoning engine synthesizes a structured plan and a creative script, breaking down the story into scenes with descriptive prompts.
3.  **Initial Visualization (`Fooocus`):** The agent generates a high-quality "seed" image for the first scene of the script, setting the visual tone for the entire piece.
4.  **Video Animation (`FramePack`):** Using the seed image and the remaining script prompts, the agent animates the story, generating the final video output.

The agent's "brain" (`core/reasoner.py`) is capable of generating multiple plans, evaluating its confidence in each, and pursuing only the most promising path, ensuring both efficiency and quality.

---

## Project Structure

-   `main.py`: The minimalist entry point. You only need to provide your idea here.
-   `core/`: Contains the agent's "brain" (`reasoner.py`) and the standard `tool_interface.py`.
-   `knowledge/`: The tool for managing the `Memvid` knowledge base.
-   `reasoning/`: The tool wrapper for the `SpikingBrain` scripting model.
-   `image_gen/`: The tool wrapper for the `Fooocus` image generator.
-   `video_gen/`: The tool wrapper for the `FramePack` video generator.
-   `requirements.txt`: A unified list of all project dependencies.

---

## How to Use

The agent is designed for simplicity. All complex operations are handled internally.

### Step 1: Build the Knowledge Base (One-time setup)

Before the agent can reason about topics, it needs knowledge. You can provide it with documents (in the `knowledge/sample_data` directory) and run the build command once.

```bash
# This command is for manual knowledge base management if needed.
# The autonomous agent will use this tool automatically.
python knowledge/manager.py build knowledge/sample_data
```

### Step 2: Execute an Idea

This is the primary way to interact with the agent. Provide your high-level idea as a command-line argument.

**Usage:**
```bash
python main.py "Your creative idea here"
```

**Example:**
```bash
python main.py "Create a short, dramatic video about the rise and fall of the Roman Empire"
```

The agent will then initiate its autonomous workflow: thinking, planning, and executing each step. The final output (a video file) will be saved in the `video_gen/output/` directory.

---

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd agent_repository
    ```

2.  **Install all dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

*Note: The current implementation uses simulated models within the tool wrappers. To make it fully functional, you would need to download the actual model weights for SpikingBrain, Fooocus, and FramePack and implement the loading/inference logic within each respective `wrapper.py` file.*