import os
from langchain_google_community import GoogleSearchAPIWrapper
from langchain_core.tools import Tool
from dotenv import load_dotenv

load_dotenv()


# api_key = os.environ["API_KEY"]
# folder_id = os.getenv("FOLDER_ID")
# api_key   = os.getenv("API_KEY")

def web_search_transport(city_from, to_city):
    os.environ["GOOGLE_API_KEY"] = os.environ["GOOGLE_API_KEY"]
    os.environ["GOOGLE_CSE_ID"] = os.environ["GOOGLE_CSE_ID"]

    # Создаём обёртку поиска
    search = GoogleSearchAPIWrapper()

    tool = Tool(
        name="google_search",
        description="Поиск в Google",
        func=search.run,
    )

    # Пример запроса
    _ = tool.run(f"посмотри примерную цену на билет от {city_from} до {to_city}")
    print(_)
    return _


def web_search_resident(to_city):
    os.environ["GOOGLE_API_KEY"] = os.environ["GOOGLE_API_KEY"]
    os.environ["GOOGLE_CSE_ID"] = os.environ["GOOGLE_CSE_ID"]

    # Создаём обёртку поиска
    search = GoogleSearchAPIWrapper()

    tool = Tool(
        name="google_search",
        description="Поиск в Google",
        func=search.run,
    )

    # Пример запроса
    _ = tool.run(f"посмотри примерную цену за ночь проживания в трехзвездночном отеле в городе {to_city}")
    print(_)
    return _
