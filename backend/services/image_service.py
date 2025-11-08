# import uuid
# from pathlib import Path
# from typing import Dict
# from datetime import datetime
# from core.logger import logger

# class ImageService:
#     """Handle image storage operations"""

#     def __init__(self, base_path: str = "storage/receipts"):
#         """
#         Initialize image service

#         Args:
#             base_path: Base directory for storing images
#         """
#         self.base_path = Path(base_path)
#         self.base_path.mkdir(parents=True, exist_ok=True)

#     def save_receipt_image(
#         self, image_bytes: bytes, user_id: str, file_extension: str = "jpg"
#     ) -> Dict[str, str]:
#         """
#         Save receipt image to disk

#         Args:
#             image_bytes: Image data as bytes
#             user_id: User ID for organizing files
#             file_extension: File extension (jpg, png, etc.)

#         Returns:
#             Dict with success status and file paths
#         """
#         try:
#             # Create user-specific directory
#             user_dir = self.base_path / user_id
#             user_dir.mkdir(parents=True, exist_ok=True)

#             # Generate unique filename
#             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#             unique_id = str(uuid.uuid4())[:8]
#             filename = f"receipt_{timestamp}_{unique_id}.{file_extension}"

#             # Full path
#             file_path = user_dir / filename

#             # Write bytes to file
#             with open(file_path, "wb") as f:
#                 f.write(image_bytes)

#             logger.info(f"Image saved successfully: {file_path}")

#             return {
#                 "success": True,
#                 "absolute_path": str(file_path.absolute()),
#                 "relative_path": str(file_path.relative_to(self.base_path.parent)),
#                 "filename": filename,
#                 "size_bytes": len(image_bytes),
#             }

#         except Exception as e:
#             logger.error(f"Error saving image: {str(e)}", exc_info=True)
#             return {"success": False, "error": str(e)}

#     def delete_image(self, file_path: str) -> bool:
#         """
#         Delete image from disk

#         Args:
#             file_path: Path to image file

#         Returns:
#             True if deleted successfully
#         """
#         try:
#             path = Path(file_path)
#             if path.exists():
#                 path.unlink()
#                 logger.info(f"Image deleted: {file_path}")
#                 return True
#             else:
#                 logger.warning(f"Image not found: {file_path}")
#                 return False
#         except Exception as e:
#             logger.error(f"Error deleting image: {str(e)}", exc_info=True)
#             return False

#     def get_storage_stats(self, user_id: str) -> Dict:
#         """
#         Get storage statistics for a user

#         Args:
#             user_id: User ID

#         Returns:
#             Dict with storage stats
#         """
#         user_dir = self.base_path / user_id

#         if not user_dir.exists():
#             return {"total_images": 0, "total_size_bytes": 0, "total_size_mb": 0}

#         images = list(user_dir.glob("receipt_*.jpg"))
#         total_size = sum(f.stat().st_size for f in images)

#         return {
#             "total_images": len(images),
#             "total_size_bytes": total_size,
#             "total_size_mb": round(total_size / (1024 * 1024), 2),
#         }
