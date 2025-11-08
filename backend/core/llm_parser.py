import json
import os
from openai import OpenAI
from pydantic import ValidationError
from models.receipt import Receipt, CategorizedReceiptItem
from data.prompts import prompts
from data.db_models import DbReceiptItem
from typing import List
from dotenv import load_dotenv
from data.prompts.prompt_utils import get_system_prompt
from core.logger import logger

load_dotenv()

GPT_MODEL = os.getenv("GPT_MODEL")
GPT_API_KEY = os.getenv("GPT_API_KEY")

client = OpenAI(api_key=GPT_API_KEY)


def convert_receipt_text_to_json(receipt: str) -> Receipt:
    print("Logger handlers:", logger.handlers)
    logger.debug("Test log")
    raw_json = _make_request(
        prompt=receipt, system_prompt_keyword=prompts.FORMAT_RECEIPT_AS_JSON_V3
    )

    data = json.loads(raw_json)

    try:
        return Receipt(**data)
    except ValidationError as e:
        logger.error("Validation error while openapi receipt response", e)
        # print("Validation error while parsing receipt:", e)
        raise


def classify_receipt_items(
    receipt_items: List[DbReceiptItem],
) -> List[CategorizedReceiptItem]:

    items = [
        CategorizedReceiptItem(row_id=item.id, name=item).model_dump()
        for item in receipt_items
    ]
    json_string = json.dumps(items, ensure_ascii=False)
    raw_json = _make_request(
        json_string, system_prompt_keyword=prompts.CLASSIFY_RECEIPT_ITEMS_V1
    )

    data = json.loads(raw_json)

    try:
        return [CategorizedReceiptItem.model_validate(item) for item in data]
    except ValidationError as e:
        logger.error("Validation error while openapi receipt items response", e)
        # print("Validation error while parsing receipt items:", e)
        raise

def _make_request(prompt, system_prompt_keyword) -> str:
    system_prompt = get_system_prompt(system_prompt_keyword)
    logger.debug(
        f"Sending request to {GPT_MODEL}. Using {prompts.FORMAT_RECEIPT_AS_JSON_V3}."
    )
    response = client.chat.completions.create(
        model=GPT_MODEL,
        response_format={"type": "json_object"},
        temperature=0,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
    )
    logger.debug(
        f"Response received from {GPT_MODEL} to {prompts.FORMAT_RECEIPT_AS_JSON_V3}."
    )

    return response.choices[0].message.content
