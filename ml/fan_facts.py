import datetime
import re
from yandex_cloud_ml_sdk import YCloudML

import os
from dotenv import load_dotenv


load_dotenv()

folder_id = os.environ["FOLDER_ID"]
api_key = os.environ["API_KEY"]
folder_id = os.getenv("FOLDER_ID")
api_key = os.getenv("API_KEY")

def fan_fact(place: str) -> str:
    sdk = YCloudML(
        folder_id=folder_id,
        auth=api_key
    )
    model = sdk.models.completions("yandexgpt-lite", model_version="rc")
    model = model.configure(temperature=0.5)

    system_prompt = """
    Ты — профессиональный копирайтер и краевед, специализирующийся на коротких ярких фактах о городах для туристов. 
    Твой факт ДОЛЖЕН:
    1. Быть строго реальным и проверяемым (основан на достоверных источниках: официальных сайтах, Википедии, музейных справках и т. п.).
    2. Не содержать никаких выдумок или домыслов.
    3. Предоставлять ссылку на источник в конце, если это возможно (или писать «Источник: Википедия» и т. п.).
    4. Вписываться в 1–2 предложения (не более 40 слов) без приветствий, вопросов и призывов.
    Если ты не можешь подтвердить факт — ответь: «Не удалось найти достоверный факт.»
    5.  не пиши источник
    """

    user_prompt = (
        f"Дай один интересный проверяемый факт про город {place}, "
        "который обычно не упоминают в путеводителях."
    )


    result = model.run([
        {"role": "system", "text": system_prompt},
        {"role": "user",   "text": user_prompt},
    ])

    fact = result.alternatives[0].text.strip()
    return fact