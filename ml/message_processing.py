import datetime
import re
from yandex_cloud_ml_sdk import YCloudML
import codecs
import os
from dotenv import load_dotenv

load_dotenv()

folder_id = os.environ["FOLDER_ID"]
api_key = os.environ["API_KEY"]

with codecs.open("ml/promt_fact.txt", "r", "utf-8") as promt_fact_:
    promt_fact = promt_fact_.read()


def trip_input(raw_text) -> dict:
    sdk = YCloudML(
        folder_id=folder_id,
        auth=api_key
    )
    model = sdk.models.completions("yandexgpt-lite", model_version="rc")
    model = model.configure(temperature=0.0)

    system_prompt = promt_fact
    user_prompt = f"RAW_INPUT:\n{raw_text}"

    response_iter = model.run([
        {"role": "system", "text": system_prompt},
        {"role": "user", "text": user_prompt},
    ])
    alt = next(iter(response_iter), None)

    raw = alt.text

    # Убираем markdown-кодовые блоки, если есть
    raw = re.sub(r"^```(?:\w+)?\s*", "", raw.strip())
    raw = re.sub(r"\s*```$", "", raw, flags=re.MULTILINE)
    raw = raw.strip()

    try:
        parsed = eval(raw, {"datetime": datetime})
    except Exception as e:
        print("Ошибка при разборе eval:", e)
        return None

    data = [parsed.get("min_budget"), parsed.get("max_budget"), parsed.get("city_from"), parsed.get("whitelist"),
            parsed.get("blacklist"),
            parsed.get("preferences"), parsed.get("with_dates"), parsed.get("end_dates")]

    min_cost, max_cost, city_from, white_list, black_list, pref, with_dates, end_dates = data

    data_dict = {}
    for name in ["min_cost", "max_cost", "city_from", "white_list", "black_list", "pref", "with_dates", "end_dates"]:
        data_dict[name] = eval(name)
    if data_dict["white_list"] == "":
        data_dict["white_list"] = None
    return data_dict
