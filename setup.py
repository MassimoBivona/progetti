from setuptools import setup, find_packages

setup(
    name="keystone_agent",
    version="1.0.0",
    author="Jules The AI Agent",
    description="Project Keystone: A real, working, autonomous creative agent, ready for its LLM brain.",
    packages=find_packages(),
    python_requires='>=3.9',
    install_requires=[
        "gradio",
        "torch",
        "diffusers[torch]",
        "transformers",
        "accelerate",
        "safetensors",
        "tqdm",
        "requests",
    ]
)