import os
import time
from telegram import PhotoSize


class FileHandler:
    def __init__(self, base_dir: str):
        self.base_dir = base_dir

    def get_user_directory(self, uid: int) -> str:
        """Get or create user directory"""
        user_dir = os.path.join(self.base_dir, str(uid))
        os.makedirs(user_dir, exist_ok=True)
        return user_dir

    def generate_filename(self, prefix: str = "receipt") -> str:
        """Generate timestamped filename"""
        timestamp = int(time.time())
        return f"{prefix}_{timestamp}.jpg"

    async def download_photo(self, photo: PhotoSize, filepath: str) -> bytes:
        """Download photo and return bytes"""
        file = await photo.get_file()
        await file.download_to_drive(filepath)

        with open(filepath, "rb") as f:
            return f.read()
