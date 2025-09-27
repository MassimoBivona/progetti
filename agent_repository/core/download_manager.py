import requests
from tqdm import tqdm
import os

def download_file(url: str, destination: str, description: str = "Downloading model"):
    """
    Downloads a file from a URL to a destination, showing a progress bar.
    If the file already exists, the download is skipped.
    """
    if os.path.exists(destination):
        print(f"[Download Manager] File already exists: {destination}. Skipping download.")
        return

    print(f"[Download Manager] Downloading {description} from {url} to {destination}...")

    # Ensure the destination directory exists
    os.makedirs(os.path.dirname(destination), exist_ok=True)

    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            total_size_in_bytes = int(r.headers.get('content-length', 0))
            block_size = 1024  # 1 Kibibyte

            progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True, desc=description)
            with open(destination, 'wb') as f:
                for chunk in r.iter_content(chunk_size=block_size):
                    progress_bar.update(len(chunk))
                    f.write(chunk)
            progress_bar.close()

            if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
                print("[Download Manager] ERROR, something went wrong during download.")
            else:
                print(f"[Download Manager] Download complete: {destination}")

    except Exception as e:
        print(f"[Download Manager] Failed to download file. Error: {e}")
        # Clean up partial file if download fails
        if os.path.exists(destination):
            os.remove(destination)