import datetime
import re
from yandex_cloud_ml_sdk import YCloudML

import os
from dotenv import load_dotenv


load_dotenv()

folder_id = os.environ["FOLDER_ID"]
api_key = os.environ["API_KEY"]
folder_id = os.getenv("FOLDER_ID")
api_key   = os.getenv("API_KEY")

def price_extract(request: str) -> str:
    sdk = YCloudML(
        folder_id=folder_id,
        auth=api_key
    )
    model = sdk.models.completions("yandexgpt-lite", model_version="rc")
    model = model.configure(temperature=0.5)

    system_prompt = """
            "Ты бот для разбора поискового запроса. "
            "Ты должен найти в тексте среднее числовое значение (цену)"
        "Верни строго одного числовое значение и знак валюты рядом с ним.
    """

    user_prompt = (
        f"Дай среднюю цену в этом запросе:"
        f"{request}"
    )


    result = model.run([
        {"role": "system", "text": system_prompt},
        {"role": "user",   "text": user_prompt},
    ])

    price = result.alternatives[0].text.strip()
    return price
