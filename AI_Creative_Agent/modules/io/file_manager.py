import os
import json

class FileManager:
    """
    Handles all file input/output operations for the agent, ensuring
    a consistent and organized project structure.
    """
    def __init__(self, project_path):
        """
        Initializes the FileManager.

        Args:
            project_path (str): The root directory for the current project run.
        """
        if not project_path:
            raise ValueError("Project path cannot be None or empty.")
        self.project_path = project_path

    def _get_output_path(self, asset_type, filename):
        """
        Constructs a full, safe path for a new asset.

        Args:
            asset_type (str): The type of asset (e.g., 'text', 'images', 'videos').
            filename (str): The name of the file to be saved.

        Returns:
            str: The full path for the new file.
        """
        # Sanitize filename to prevent directory traversal issues
        if ".." in filename or filename.startswith(("/", "\\")):
            raise ValueError(f"Invalid filename: {filename}")

        output_dir = os.path.join(self.project_path, asset_type)
        os.makedirs(output_dir, exist_ok=True)
        return os.path.join(output_dir, filename)

    def save_text(self, filename, content, asset_type="text"):
        """
        Saves text content to a file.

        Args:
            filename (str): The name of the file (e.g., 'plot.txt').
            content (str): The text content to save.
            asset_type (str): The subdirectory to save into (defaults to 'text').

        Returns:
            str: The path to the saved file.
        """
        filepath = self._get_output_path(asset_type, filename)
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Saved text asset: {filepath}")
            return filepath
        except IOError as e:
            print(f"ERROR: Could not write to file {filepath}: {e}")
            return None

    def save_binary(self, filename, data, asset_type=""):
        """
        Saves binary data to a file.

        Args:
            filename (str): The name of the file (e.g., 'character.png').
            data (bytes): The binary data to save.
            asset_type (str): The subdirectory to save into.

        Returns:
            str: The path to the saved file.
        """
        filepath = self._get_output_path(asset_type, filename)
        try:
            with open(filepath, 'wb') as f:
                f.write(data)
            print(f"Saved binary asset: {filepath}")
            return filepath
        except IOError as e:
            print(f"ERROR: Could not write to file {filepath}: {e}")
            return None

    def save_json(self, filename, data, asset_type="data"):
        """
        Saves a Python dictionary as a JSON file.

        Args:
            filename (str): The name of the file (e.g., 'project_state.json').
            data (dict): The dictionary to serialize and save.
            asset_type (str): The subdirectory to save into (defaults to 'data').

        Returns:
            str: The path to the saved file.
        """
        filepath = self._get_output_path(asset_type, filename)
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            print(f"Saved JSON data: {filepath}")
            return filepath
        except (IOError, TypeError) as e:
            print(f"ERROR: Could not save JSON to file {filepath}: {e}")
            return None

    def read_text(self, filepath):
        """
        Reads text content from a file.
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except IOError as e:
            print(f"ERROR: Could not read file {filepath}: {e}")
            return None