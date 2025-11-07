import json
import os
from openai import OpenAI
from pydantic import ValidationError
from models.receipt import Receipt
from prompts import prompts
from dotenv import load_dotenv
from prompts.prompt_utils import get_system_prompt
from .logger import logger

load_dotenv()

GPT_MODEL = os.getenv("GPT_MODEL")
GPT_API_KEY = os.getenv("GPT_API_KEY")

client = OpenAI(api_key=GPT_API_KEY)


def convert_to_model(receipt: str) -> Receipt:
    system_prompt = get_system_prompt(prompts.FORMAT_RECEIPT_AS_JSON_V2)
    logger.debug(
        f"Sending request to {GPT_MODEL}. Using {prompts.FORMAT_RECEIPT_AS_JSON_V2}."
    )
    response = client.chat.completions.create(
        model=GPT_MODEL,
        response_format={"type": "json_object"},
        temperature=0,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": receipt},
        ],
    )
    logger.debug(f"Response received from {GPT_MODEL}.")

    raw_json = response.choices[0].message.content

    data = json.loads(raw_json)

    try:
        return Receipt(**data)
    except ValidationError as e:
        logger.error("Validation error while openapi receipt response", e)
        print("Validation error while parsing receipt:", e)
        raise
