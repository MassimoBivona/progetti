import os
from pathlib import Path
from memvid import MemvidEncoder, MemvidChat
import sys

# Ensure the root directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.tool_interface import ToolInterface

class KnowledgeManager(ToolInterface):
    """
    A tool for managing the Memvid knowledge base. It can build a knowledge
    base from documents or retrieve information from an existing one.
    """
    def __init__(self, output_dir="knowledge/memory_output"):
        self.output_dir = Path(output_dir)
        self.video_path = self.output_dir / "memory.mp4"
        self.index_path = self.output_dir / "index.json"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @property
    def name(self) -> str:
        return "knowledge_retriever_and_builder"

    @property
    def description(self) -> str:
        return "A tool to build a knowledge base from a directory of documents or to retrieve context by asking a question to an existing knowledge base."

    def execute(self, action: str, **kwargs):
        """
        Executes a specific action for the knowledge tool.

        Args:
            action (str): The action to perform ('build' or 'chat').
            **kwargs: Arguments for the action.
                      - For 'build': `source_dir` (str)
                      - For 'chat': `query` (str)

        Returns:
            The result of the action (e.g., a success message or retrieved context).
        """
        if action == "build":
            source_dir = kwargs.get("source_dir")
            if not source_dir:
                return "Error: 'source_dir' is required for the 'build' action."
            return self._build_from_directory(source_dir)
        elif action == "chat":
            query = kwargs.get("query")
            if not query:
                return "Error: 'query' is required for the 'chat' action."
            return self._chat_with_memory(query)
        else:
            return f"Error: Unknown action '{action}' for KnowledgeManager."

    def _build_from_directory(self, source_dir: str):
        """Builds a video memory from all supported files in a directory."""
        if not Path(source_dir).is_dir():
            return f"Error: Source directory '{source_dir}' not found."

        print(f"[{self.name}] Starting to build memory from '{source_dir}'...")
        encoder = MemvidEncoder()

        supported_extensions = [".txt", ".md", ".pdf"]
        files_processed = 0
        for file_path in Path(source_dir).rglob('*'):
            if file_path.is_file() and file_path.suffix in supported_extensions:
                try:
                    if file_path.suffix == ".pdf":
                        encoder.add_pdf(str(file_path))
                    else:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            encoder.add_text(f.read())
                    files_processed += 1
                except Exception as e:
                    print(f"    - Could not process file {file_path.name}: {e}")

        if files_processed > 0:
            encoder.build_video(str(self.video_path), str(self.index_path))
            return f"Memory built successfully from {files_processed} file(s)."
        else:
            return "No supported files found to build memory."

    def _chat_with_memory(self, query: str) -> str:
        """Chats with the existing video memory."""
        if not self.video_path.exists() or not self.index_path.exists():
            return "Error: Memory not found. Please build it first."

        print(f"[{self.name}] Asking: '{query}'")
        try:
            chat = MemvidChat(str(self.video_path), str(self.index_path))
            response = chat.chat(query)
            return response
        except Exception as e:
            return f"An error occurred while chatting with memory: {e}"