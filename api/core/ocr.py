from paddleocr import PaddleOCR
import cv2
import numpy as np
from typing import List, Dict


def extract_text_blocks(image_bytes: bytes) -> List[Dict]:
    """
    Perform OCR using PaddleOCR and return row-level text blocks.

    Args:
        image_path: Path to the receipt image

    Returns:
        List of dictionaries containing text, confidence, and position info
    """
    ocr = PaddleOCR(lang="ro", use_angle_cls=True)

    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"Cannot read image from bytes {image}")

    # Use predict() which returns a list of result dictionaries
    results = ocr.predict(image)

    text_blocks = []

    # results is a list, typically with one element for single-page images
    if results and len(results) > 0:
        result = results[0]

        rec_texts = result.get("rec_texts", [])
        rec_scores = result.get("rec_scores", [])
        rec_polys = result.get("rec_polys", [])

        for i, (text, score, poly) in enumerate(zip(rec_texts, rec_scores, rec_polys)):
            # Calculate center coordinates from polygon
            y_coords = [point[1] for point in poly]
            center_y = sum(y_coords) / len(y_coords)

            x_coords = [point[0] for point in poly]
            center_x = sum(x_coords) / len(x_coords)

            text_blocks.append(
                {
                    "text": text.strip(),
                    "confidence": score,
                    "poly": poly.tolist() if hasattr(poly, "tolist") else poly,
                    "center_x": center_x,
                    "center_y": center_y,
                }
            )

    # Sort by vertical position (top to bottom)
    text_blocks.sort(key=lambda x: x["center_y"])

    return text_blocks


def group_text_by_rows(
    text_blocks: List[Dict], y_threshold: int = 20
) -> List[List[Dict]]:
    """
    Group text blocks into rows based on vertical position.

    Args:
        text_blocks: List of text block dictionaries
        y_threshold: Maximum vertical distance to consider blocks in same row

    Returns:
        List of rows, where each row is a list of text blocks
    """
    if not text_blocks:
        return []

    rows = []
    current_row = [text_blocks[0]]

    for block in text_blocks[1:]:
        # Check if block is close enough vertically to be in same row
        if abs(block["center_y"] - current_row[0]["center_y"]) <= y_threshold:
            current_row.append(block)
        else:
            # Sort current row by x position (left to right)
            current_row.sort(key=lambda x: x["center_x"])
            rows.append(current_row)
            current_row = [block]

    # Add the last row
    if current_row:
        current_row.sort(key=lambda x: x["center_x"])
        rows.append(current_row)

    return rows


def format_receipt_text(rows: List[List[Dict]]) -> str:
    """
    Format grouped rows into readable receipt text.

    Args:
        rows: List of rows from group_text_by_rows

    Returns:
        Formatted receipt text as string
    """
    output = []

    for row in rows:
        # Combine text from all blocks in the row
        row_text = " ".join([block["text"] for block in row])
        output.append(row_text)

    return "\n".join(output)


def extract_receipt_info(image_bytes: bytes) -> tuple:
    """
    Extract and parse receipt information from image.

    Args:
        image_path: Path to receipt image

    Returns:
        Dictionary containing extracted text blocks, rows, and formatted text
    """
    # Extract all text blocks
    text_blocks = extract_text_blocks(image_bytes)

    # Group into rows
    rows = group_text_by_rows(text_blocks)

    # Format as readable text
    formatted_text = format_receipt_text(rows)

    return (
        formatted_text,
        len(text_blocks),
        # len(rows),
    )
