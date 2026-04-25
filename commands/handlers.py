import os
import asyncio

from aiogram import F, Router
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import BufferedInputFile, CallbackQuery, Message

import commands.keyboards as kb
from ml import find_trip, message_processing, fan_facts
# from db import database
import codecs

# db = database.Database()
router = Router()

# messages: dict[int, str] = {}
messages = {}
data_proc = [None for x in range(6)]
with codecs.open("ml/example_trip.txt", "r", "utf-8") as trip_exemple_:
    trip_exemple = trip_exemple_.read()
with codecs.open("ml/listen_started_text.txt", "r", "utf-8") as listen_started_text_:
    listen_started_text = listen_started_text_.read()
with codecs.open("ml/almost_ready.txt", "r", "utf-8") as almost_ready_:
    almost_ready = almost_ready_.read()
with codecs.open("ml/knowledge.txt", "r", "utf-8") as knowledge_:
    knowledge = knowledge_.read().split("split")
with codecs.open("ml/start_text.txt", "r", "utf-8") as start_text_:
    start_text = start_text_.read()
interact_missing = {
    'min_cost': "минимального бюджета",
    'max_cost': "максимального бюджета",
    'city_from': "города отправления",
    'white_list': "желаемых мест",
    'black_list': "черного списка",
    'pref': "интересов",
    'with_dates': "дат начала путешествия",
    'end_dates': "дат конца путешествия"
}


# база данных, на данный момент отключено

# async def history_for_chat_id(chat_id: int, db: database.Database) -> str:
#     """
#     Получает историю чата из базы данных и форматирует ее в строку.
#
#     Args:
#         chat_id: ID чата, историю которого нужно получить.
#         db: Экземпляр класса Database для взаимодействия с базой данных.
#
#     Returns:
#         Строка с отформатированной историей чата.
#     """
#     history_list = await db.get_history(chat_id)
#     history_text = ""
#     if history_list:
#         for item in history_list:
#             history_text += f"{item.text}\n"
#     return history_text


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(text=start_text, reply_markup=kb.keyboard_main)


@router.callback_query(lambda call: call.data == "listen")
async def listen_setting(callback: CallbackQuery):
    await callback.message.reply(
        text="Выбор режима прослушки.", reply_markup=kb.keyboard_listen
    )
    await callback.answer("", show_alert=True)


@router.message(lambda message: message.text == "Включить")
async def listen_on(message: Message):
    chat_id = message.chat.id
    print(chat_id)
    if chat_id not in messages.keys():
        messages[chat_id] = ""
        await message.reply(
            text=listen_started_text, reply_markup=kb.keyboard_listen
        )
    else:
        await message.answer("Прослушка уже активна.")


@router.message(F.text != "Выключить")
async def collect_message(message: Message):
    chat_id = message.chat.id
    if chat_id in messages.keys():
        messages[chat_id] = messages.get(chat_id, "") + f"\n{message.text}"


@router.message(lambda message: message.text == "Выключить")
async def listen_off(message: Message):
    chat_id = message.chat.id

    if chat_id in messages:
        collected_text = messages[chat_id]
        data_proc = message_processing.trip_input(collected_text)
        print(data_proc)
        if (data_proc):
            if data_proc["max_cost"] == None:
                data_proc["max_cost"] = data_proc["min_cost"]
            elif data_proc["min_cost"] == None:
                data_proc["min_cost"] = data_proc["max_cost"]

        if not (data_proc):
            await message.answer("Нужно прислать хоть что-нибудь содержательное.")
            return None
        elif None in data_proc.values() or (None, None) in data_proc.values():
            await message.answer("Слишком мало данных.")
            missing = []

            for key in data_proc.keys():
                if not (data_proc[key]):
                    missing.append(interact_missing[key])
            await asyncio.sleep(1)
            await message.answer(f"Не хватает {", ".join(missing)}.")
            await asyncio.sleep(1.5)
            await message.answer(
                f"Пожалуйста, продолжайте обсуждение дальше или сразу введите в сообщениях недостающие данные.")
            return None
        # обработка выбивающихся случаев
        if data_proc["with_dates"]:
            if data_proc["with_dates"][:4] != "2025" or data_proc["end_dates"][:4] != "2025" or data_proc[
                "with_dates"] == None or data_proc["end_dates"] == None:
                for x in range(1, 10):
                    messages[chat_id] = messages[chat_id].replace(f"2{x}", "")
                await message.answer(
                    "Извините, что-то не так с датами. Я не умею планировать слишком далекие поездки. Возможно, вы не ввели год.")
                await asyncio.sleep(1)
                return None
        else:
            return None
        if data_proc["max_cost"]:
            if data_proc["max_cost"] < 5000:
                await asyncio.sleep(1)
                await message.answer(
                    "Извините, бюджет слишком маленький. Я не смогу спланировать путешествие с таким бюджетом.")
                await asyncio.sleep(1)
                await message.answer("Пришлите больший бюджет с пометкой \"окончательный\", пожалуйста.")
                data_proc["max_cost"] = None
                return None
        else:
            return None
        del messages[chat_id]

        await asyncio.sleep(1)
        await message.answer(text=f"{almost_ready}{fan_facts.fan_fact(data_proc["white_list"])}")
        await asyncio.sleep(2)
        await message.answer(
            text=f"{knowledge[0]}{", ".join(data_proc["white_list"].split())}{knowledge[1]}{data_proc["max_cost"]}{knowledge[2]}")
        print(data_proc)
        temp_trip = await find_trip.find_trip(data_proc)
        await message.answer(temp_trip, parse_mode="Markdown", reply_markup=kb.keyboard_main)
    else:
        await message.answer("Прослушка не была активна.")

# работа с базой данных, на данный момент отключено.

# @router.callback_query(lambda call: call.data == "past_trip")
# async def past_trip(callback: CallbackQuery):
#     text = await history_for_chat_id(callback.message.chat.id, db)
#     if text != "":
#         await callback.message.reply(
#             text=text,
#             reply_markup=kb.keyboard_main,
#             parse_mode="Markdown"
#         )
#     else:
#         await callback.message.reply(
#             text="Вы пока не создавали планов в этом чате.",
#             reply_markup=kb.keyboard_main,
#             parse_mode="Markdown"
#         )
#     await callback.answer("", show_alert=True)
