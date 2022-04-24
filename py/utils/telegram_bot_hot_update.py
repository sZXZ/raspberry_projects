
import argparse
from datetime import datetime

from py.utils import code_secrets
from telegram import Bot


def get_context():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--user")
    parser.add_argument("--msg")
    return parser.parse_args()


def shoping_list():
    pass


def replay(user, msg):
    bot = Bot(code_secrets.TELEGRAM)
    if "Купить " in msg:
        from pymongo import MongoClient

        client = MongoClient("localhost", 27017)
        db = client.list.list
        db.insert_one({"name": msg[7:]})
        bot.send_message(text=f"Добавил в список:{msg[7:]}", chat_id=user)
        return 0
    if "Убрать " in msg:
        from pymongo import MongoClient

        client = MongoClient("localhost", 27017)
        db = client.list.list
        if db.delete_one({"name": msg[7:]}).deleted_count > 0:
            bot.send_message(text=f"Убрал из списка:{msg[7:]}", chat_id=user)
        else:
            bot.send_message(text=f"Не нашёл:{msg[7:]}", chat_id=user)
        return 0
    if "Удалить список покупок" in msg:
        from pymongo import MongoClient

        client = MongoClient("localhost", 27017)
        db = client.list.list
        new_name = f"list{datetime.now():%Y%m%d}"
        db.rename(new_name)
        bot.send_message(text=f"Убрал список в архив: {new_name}", chat_id=user)
        return 0
    if "Список покупок" in msg:
        from pymongo import MongoClient

        client = MongoClient("localhost", 27017)
        db = client.list.list
        product_list = []
        for doc in db.find({}):
            product_list.append(doc["name"])
        msg = "\n".join(product_list)
        bot.send_message(text=f"Cписок:\n{msg}", chat_id=user)
        return 0
    if "Пыльца" in msg:
        offset = msg.split(" ")[-1]
        try:
            offset = int(offset)
        except:
            offset = 0
        try:
            bot.send_message(
                text=f"{get_pollen(offset)}", chat_id=user, parse_mode="Markdown"
            )
        except Exception as ex:
            bot.send_message(text=f"{ex}", chat_id=user)
        return 0
    if "Бэкап" in msg:
        from subprocess import run

        run(["/home/ubuntu/venv/bin/python", "/home/ubuntu/py/backup.py"])
        bot.send_message(text=f"Cделал бэкап файлов", chat_id=user)
        return 0
    bot.send_message(text=f"Hi, I don't know how to: \n'{msg}''", chat_id=user)


def get_pollen(offset: int):
    from datetime import datetime

    import cv2
    import numpy as np
    import requests

    track = ["birch", "alder"]
    track_dict = {
        "alder": [
            "Ольха",
            [
                "0",
                "0.1-1",
                "1-5",
                "5-10",
                "10-25",
                "25-50",
                "50-100",
                "100-500",
                "500-1000",
                "1000+",
            ],
        ],
        "birch": [
            "Береза",
            [
                "0",
                "1-5",
                "5-10",
                "10-25",
                "25-50",
                "50-100",
                "100-500",
                "500-1000",
                "1000-5000",
                "5000+",
            ],
        ],
    }
    info = f"[Пыльца через {offset} часов](https://silam.fmi.fi/pollen.html?parameter=birch&amp;region=regional):\n"
    pollen_data = [info]
    for t in track:
        try:
            url = f"https://silam.fmi.fi/AQ/operational/regional/pollen/000/{t}_srf_0{datetime.now().hour+offset:02d}.png"
            img_c = requests.get(url).content
        except Exception as ex:
            info = f"Пыльца через {48-datetime.now().hour} часов:\n"
            url = f"https://silam.fmi.fi/AQ/operational/regional/pollen/000/{t}_srf_048.png"
            img_c = requests.get(url).content
        print(url)
        im_bytes = np.frombuffer(bytearray(img_c), dtype=np.uint8)
        im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
        image = cv2.imdecode(im_arr, -1)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        vilnius1 = image[480][392]
        vilnius2 = image[480][393]
        vilnius3 = image[481][390]
        vilnius4 = image[481][393]
        gap = 39
        start = 415
        schema = {
            tuple(image[start + gap][555]): f"{track_dict[t][1][0]} белый",
            tuple(image[start][555]): f"{track_dict[t][1][1]} серый",
            tuple(image[start - gap][555]): f"{track_dict[t][1][2]} зеленый",
            tuple(
                image[start - (gap * 2)][555]
            ): f"{track_dict[t][1][3]} зеленый-желтый",
            tuple(image[start - (gap * 3)][555]): f"{track_dict[t][1][4]} желтый",
            tuple(
                image[start - (gap * 4)][555]
            ): f"{track_dict[t][1][5]} ярко-ораньжевый",
            tuple(image[start - (gap * 5)][555]): f"{track_dict[t][1][6]} ораньжевый",
            tuple(image[start - (gap * 6)][555]): f"{track_dict[t][1][7]} красный",
            tuple(image[start - (gap * 7)][555]): f"{track_dict[t][1][8]} розовый",
            tuple(image[start - (gap * 8)][555]): f"{track_dict[t][1][9]} фиолетовый",
        }
        pollen_data.append(
            f"[{track_dict[t][0]}]({url}):\n{schema[tuple(vilnius1)]} уровень опасности \n{schema[tuple(vilnius4)]} уровень опасности"
        )
    return "\n".join(pollen_data)


if __name__ == "__main__":
    context = get_context()
    replay(context.user, context.msg)
