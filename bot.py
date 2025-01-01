import requests
from random import randint
import openpyxl
from telethon import TelegramClient, events, Button
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
import config
import sqlite3
import funections
from navlib import paginate
from funections import *
import os
import time
from service import Manager
import asyncio
from pathlib import Path
import jdatetime
from pymongo import MongoClient


api_id = config.API_ID
api_hash = config.API_HASH
bot_token = config.BOT_TOKEN
pay_token = config.PAY_TOKEN
session_name = config.SESSION_NAME
proxy = config.PROXY
if proxy:
    print("connecting...")
    proxy_type = config.PROXY_TYPE
    proxy_address = config.PROXY_ADDRESS
    proxy_port = config.PROXY_PORT
    bot = TelegramClient(session_name, api_id, api_hash, proxy=(proxy_type, proxy_address, proxy_port))
    # bot = TelegramClient(session_name, api_id, api_hash)
    # Create an instance of the TelegramClient
    bot.start(bot_token=bot_token)
    print("connected!")
else:
    bot = TelegramClient(session_name, api_id, api_hash)
    # Create an instance of the TelegramClient
    bot.start(bot_token=bot_token)

# DB
con = sqlite3.connect(config.DB_NAME)
cur = con.cursor()
# connect to mongodb
client = MongoClient("127.0.0.1:27017")
db = client["f1"]
reply_collection = db["reply"]
# ---------
manager = Manager()
user_messages = {}
bot_text = config.TEXT
all_datas_list = [bot_text["rpm"],bot_text["overtake"],bot_text["map_viz"],bot_text["down_force"],bot_text["top_speed"],
     bot_text["start_reaction"],bot_text["all_info"],bot_text["driver"],bot_text["lap_times"],bot_text["map_break"],
     bot_text["all"],bot_text["strategy"],bot_text["data_to_pole"],bot_text["lap_times_table"],
     bot_text["brake_configurations"],bot_text["composite_perfomance"], bot_text["degradation_tyre"],
     bot_text["weather_data"], bot_text["tyre_performance"], bot_text["ers_analysis"],
     bot_text["comparison_fastest_lap"], bot_text["efficiency_breakdown"], bot_text["stress_index"]]
data_scores = {
     bot_text["rpm"]: {
         "1": 3,
         "2": 2,
         "3": 1,
     },
     bot_text["overtake"]: {
         "1": 1,
         "2": 0,
         "3": 0,
     },
     bot_text["map_viz"]: {
         "1": 2,
         "2": 1,
         "3": 1,
     },
     bot_text["down_force"]: {
         "1": 2,
         "2": 1,
         "3": 1,
     },
     bot_text["top_speed"]: {
         "1": 2,
         "2": 1,
         "3": 0,
     },
     bot_text["start_reaction"]: {
         "1": 2,
         "2": 1,
         "3": 1,
     },
     bot_text["all_info"]: {
         "1": 0,
         "2": 0,
         "3": 0,
     },
     bot_text["driver"]: {
         "1": 0,
         "2": 0,
         "3": 0,
     },
     bot_text["lap_times"]: {
         "1": 2,
         "2": 1,
         "3": 1,
     },
     bot_text["map_break"]: {
         "1": 1,
         "2": 0,
         "3": 0,
     },
     bot_text["all"]: {
         "1": 5,
         "2": 3,
         "3": 3,
     },
     bot_text["strategy"]: {
         "1": 1,
         "2": 1,
         "3": 0,
     },
     bot_text["data_to_pole"]: {
         "1": 1,
         "2": 0,
         "3": 0,
     },
     bot_text["lap_times_table"]: {
         "1": 3,
         "2": 2,
         "3": 1,
     },
     bot_text["brake_configurations"]: {
         "1": 3,
         "2": 2,
         "3": 1,
     },
     bot_text["composite_perfomance"]: {
         "1": 2,
         "2": 1,
         "3": 1,
     },
     bot_text["degradation_tyre"]: {
         "1": 3,
         "2": 3,
         "3": 2,
     },
     bot_text["weather_data"]: {
         "1": 1,
         "2": 0,
         "3": 0,
     },
     bot_text["tyre_performance"]: {
         "1": 3,
         "2": 2,
         "3": 1,
     },
     bot_text["ers_analysis"]: {
         "1": 1,
         "2": 1,
         "3": 0,
     },
     bot_text["comparison_fastest_lap"]: {
         "1": 1,
         "2": 0,
         "3": 0,
     },
     bot_text["efficiency_breakdown"]: {
         "1": 2,
         "2": 1,
         "3": 1,
     },
     bot_text["stress_index"]: {
         "1": 2,
         "2": 2,
         "3": 1,
     }
}
driver_short_codes = {
    "Max_Verstappen": "VER",
    "Lewis_Hamilton": "HAM",
    "Charles_Leclerc": "LEC",
    "Sergio_Pérez": "PER",
    "Carlos_Sainz": "SAI",
    "Lando_Norris": "NOR",
    "Daniel_Ricciardo": "RIC",
    "Fernando_Alonso": "ALO",
    "George_Russell": "RUS",
    "Pierre_Gasly": "GAS",
    "Esteban_Ocon": "OCO",
    "Valtteri_Bottas": "BOT",
    "Yuki_Tsunoda": "TSU",
    "Kevin_Magnussen": "MAG",
    "Nico_Hülkenberg": "HUL",
    "Alexander_Albon": "ALB",
    "Lance_Stroll": "STR",
    "Oscar_Piastri": "PIA",
    "Guanyu_Zhou": "ZHO",
    "Franco_Colapinto": "COL",
}
driver_buy_code_en = {
    "VER": "Max_Verstappen",
    "HAM": "Lewis_Hamilton",
    "LEC": "Charles_Leclerc",
    "PER": "Sergio_Pérez",
    "SAI": "Carlos_Sainz",
    "NOR": "Lando_Norris",
    "RIC": "Daniel_Ricciardo",
    "ALO": "Fernando_Alonso",
    "RUS": "George_Russell",
    "GAS": "Pierre_Gasly",
    "OCO": "Esteban_Ocon",
    "BOT": "Valtteri_Bottas",
    "TSU": "Yuki_Tsunoda",
    "MAG": "Kevin_Magnussen",
    "HUL": "Nico_Hülkenberg",
    "ALB": "Alexander_Albon",
    "STR": "Lance_Stroll",
    "PIA": "Oscar_Piastri",
    "ZHO": "Guanyu_Zhou",
    "COL": "Franco_Colapinto",
}
driver_buy_code_fa = {
    "VER": "مکس ورستپن",
    "HAM": "لوئیس همیلتون",
    "LEC": "شارل لکلرک",
    "PER": "سرجیو پرز",
    "SAI": "کارلوس ساینز",
    "NOR": "لندو نوریس",
    "RIC": "دنیل ریکاردو",
    "ALO": "فرناندو آلونسو",
    "RUS": "جورج راسل",
    "GAS": "پیر گسلی",
    "OCO": "استبان اوکون",
    "BOT": "والتری بوتاس",
    "TSU": "یوکی سونودا",
    "MAG": "کوین مگنوسن",
    "HUL": "نیکو هالکنبرگ",
    "ALB": "الکس آلبون",
    "STR": "لنس استرول",
    "PIA": "اسکار پیاستری",
    "ZHO": "گوانیو ژو",
    "COL": "فرانکو کولاپینتو",
    "DOO": "جک دوهان"
}
ergast_data = {"MRData":{"xmlns":"http://ergast.com/mrd/1.5","series":"f1","url":"http://ergast.com/api/f1/2024/16/drivers.json","limit":"30","offset":"0","total":"20","DriverTable":{"season":"2024","round":"16","Drivers":[{"driverId":"albon","permanentNumber":"23","code":"ALB","url":"http://en.wikipedia.org/wiki/Alexander_Albon","givenName":"Alexander","familyName":"Albon","dateOfBirth":"1996-03-23","nationality":"Thai"},{"driverId":"alonso","permanentNumber":"14","code":"ALO","url":"http://en.wikipedia.org/wiki/Fernando_Alonso","givenName":"Fernando","familyName":"Alonso","dateOfBirth":"1981-07-29","nationality":"Spanish"},{"driverId":"bottas","permanentNumber":"77","code":"BOT","url":"http://en.wikipedia.org/wiki/Valtteri_Bottas","givenName":"Valtteri","familyName":"Bottas","dateOfBirth":"1989-08-28","nationality":"Finnish"},{"driverId":"colapinto ","permanentNumber":"43","code":"COL","url":"http://en.wikipedia.org/wiki/Franco_Colapinto","givenName":"Franco","familyName":"Colapinto ","dateOfBirth":"2003-05-27","nationality":"Argentinian "},{"driverId":"gasly","permanentNumber":"10","code":"GAS","url":"http://en.wikipedia.org/wiki/Pierre_Gasly","givenName":"Pierre","familyName":"Gasly","dateOfBirth":"1996-02-07","nationality":"French"},{"driverId":"hamilton","permanentNumber":"44","code":"HAM","url":"http://en.wikipedia.org/wiki/Lewis_Hamilton","givenName":"Lewis","familyName":"Hamilton","dateOfBirth":"1985-01-07","nationality":"British"},{"driverId":"hulkenberg","permanentNumber":"27","code":"HUL","url":"http://en.wikipedia.org/wiki/Nico_H%C3%BClkenberg","givenName":"Nico","familyName":"Hülkenberg","dateOfBirth":"1987-08-19","nationality":"German"},{"driverId":"leclerc","permanentNumber":"16","code":"LEC","url":"http://en.wikipedia.org/wiki/Charles_Leclerc","givenName":"Charles","familyName":"Leclerc","dateOfBirth":"1997-10-16","nationality":"Monegasque"},{"driverId":"kevin_magnussen","permanentNumber":"20","code":"MAG","url":"http://en.wikipedia.org/wiki/Kevin_Magnussen","givenName":"Kevin","familyName":"Magnussen","dateOfBirth":"1992-10-05","nationality":"Danish"},{"driverId":"norris","permanentNumber":"4","code":"NOR","url":"http://en.wikipedia.org/wiki/Lando_Norris","givenName":"Lando","familyName":"Norris","dateOfBirth":"1999-11-13","nationality":"British"},{"driverId":"ocon","permanentNumber":"31","code":"OCO","url":"http://en.wikipedia.org/wiki/Esteban_Ocon","givenName":"Esteban","familyName":"Ocon","dateOfBirth":"1996-09-17","nationality":"French"},{"driverId":"perez","permanentNumber":"11","code":"PER","url":"http://en.wikipedia.org/wiki/Sergio_P%C3%A9rez","givenName":"Sergio","familyName":"Pérez","dateOfBirth":"1990-01-26","nationality":"Mexican"},{"driverId":"piastri","permanentNumber":"81","code":"PIA","url":"http://en.wikipedia.org/wiki/Oscar_Piastri","givenName":"Oscar","familyName":"Piastri","dateOfBirth":"2001-04-06","nationality":"Australian"},{"driverId":"ricciardo","permanentNumber":"3","code":"RIC","url":"http://en.wikipedia.org/wiki/Daniel_Ricciardo","givenName":"Daniel","familyName":"Ricciardo","dateOfBirth":"1989-07-01","nationality":"Australian"},{"driverId":"russell","permanentNumber":"63","code":"RUS","url":"http://en.wikipedia.org/wiki/George_Russell_(racing_driver)","givenName":"George","familyName":"Russell","dateOfBirth":"1998-02-15","nationality":"British"},{"driverId":"sainz","permanentNumber":"55","code":"SAI","url":"http://en.wikipedia.org/wiki/Carlos_Sainz_Jr.","givenName":"Carlos","familyName":"Sainz","dateOfBirth":"1994-09-01","nationality":"Spanish"},{"driverId":"stroll","permanentNumber":"18","code":"STR","url":"http://en.wikipedia.org/wiki/Lance_Stroll","givenName":"Lance","familyName":"Stroll","dateOfBirth":"1998-10-29","nationality":"Canadian"},{"driverId":"tsunoda","permanentNumber":"22","code":"TSU","url":"http://en.wikipedia.org/wiki/Yuki_Tsunoda","givenName":"Yuki","familyName":"Tsunoda","dateOfBirth":"2000-05-11","nationality":"Japanese"},{"driverId":"max_verstappen","permanentNumber":"33","code":"VER","url":"http://en.wikipedia.org/wiki/Max_Verstappen","givenName":"Max","familyName":"Verstappen","dateOfBirth":"1997-09-30","nationality":"Dutch"},{"driverId":"zhou","permanentNumber":"24","code":"ZHO","url":"http://en.wikipedia.org/wiki/Zhou_Guanyu","givenName":"Guanyu","familyName":"Zhou","dateOfBirth":"1999-05-30","nationality":"Chinese"}]}}}

drivers_translate = {
    "Max_Verstappen": "مکس ورستپن",
    "Nyck_de Vries": "نیک دوریس",
    "German_Grand_Prix": "گرندپری آلمان",
    "Liam_Lawson": "لیام لاوسون",
    "Kimi_Räikkönen": "کیمی رایکونن",                                                                                          
    "Sergio_Pérez": "سرجیو پرز",
    "Lewis_Hamilton": "لوئیس همیلتون",
    "George_Russell": "جورج راسل",
    "Oliver_Bearman": "اولیور برمن",
    "Mick_Schumacher": "میک شوماخر",
    "Charles_Leclerc": "شارل لکلرک",
    "Robert_Kubica": "رابرت کوبیتسا",
    "Nikita_Mazepin": "نیکیتا مازپین",
    "Carlos_Sainz": "کارلوس ساینز",
    "Alexander_Albon": "الکس آلبون",
    "Antonio_Giovinazzi": "آنتونیو جیووناتزی",
    "Sebastian_Vettel": "سباستین فتل",
    "Logan_Sargeant": "لوگان سارجنت",
    "Nicholas_Latifi": "نیکولاس لطیفی",
    "Guanyu_Zhou": "گوانیو ژو",
    "Nyck_De_Vries": "نیک دوریس",
    "Valtteri_Bottas": "والتری بوتاس",
    "Daniel_Ricciardo": "دنیل ریکاردو",
    "Lando_Norris": "لندو نوریس",
    "Oscar_Piastri": "اسکار پیاستری",
    "Lance_Stroll": "لنس استرول",
    "Fernando_Alonso": "فرناندو آلونسو",
    "Pierre_Gasly": "پیر گسلی",
    "Esteban_Ocon": "استبان اوکون",
    "Yuki_Tsunoda": "یوکی سونودا",
    "Nico_Hülkenberg": "نیکو هالکنبرگ",
    "Kevin_Magnussen": "کوین مگنوسن",
    "Franco_Colapinto ": "فرانکو کولاپینتو",
    "Franco_Colapinto": 'فرانکو کولاپینتو',
    "Jack_Doohan": "جک دوهان"
}

country_tr = {
    "Bahrain_Grand_Prix": "گرندپری بحرین",
    "Saudi_Arabian_Grand_Prix": "گرندپری عربستان",
    "Australian_Grand_Prix": "گرندپری استرالیا",
    "Azerbaijan_Grand_Prix": "گرندپری آذربایجان",
    "United_States_Grand_Prix": "گرندپری آمریکا",
    "Miami_Grand_Prix": "گرندپری میامی",
    "Monaco_Grand_Prix": "گرندپری موناکو",
    "Spanish_Grand_Prix": "گرندپری اسپانیا",
    "Canadian_Grand_Prix": "گرندپری کانادا",
    "Austrian_Grand_Prix": "گرندپری اتریش",
    "British_Grand_Prix": "گرندپری بریتانیا",
    "Hungarian_Grand_Prix": "گرندپری مجارستان",
    "Belgian_Grand_Prix": "گرندپری بلژیک",
    "Dutch_Grand_Prix": "گرندپری هلند",
    "Italian_Grand_Prix": "گرندپری ایتالیا",
    "Singapore_Grand_Prix": "گرندپری سنگاپور",
    "Japanese_Grand_Prix": "گرندپری ژاپن",
    "Qatar_Grand_Prix": "گرندپری قطر",
    "Mexico_City_Grand_Prix": "گرندپری مکزیک",
    "São_Paulo_Grand_Prix": "گرندپری برزیل",
    "Abu_Dhabi_Grand_Prix": "گرندپری ابوظبی",
    "Las_Vegas_Grand_Prix": "گرندپری لاس وگاس",
    "Emilia_Romagna_Grand_Prix": "گرندپری امیلیا رومانیا",
    "Portuguese_Grand_Prix": "گرند پری پرتغال",
    "French_Grand_Prix": "گرند پری فرانسه",
    "Styrian_Grand_Prix": "گرند پری استراین",
    "Turkish_Grand_Prix": "گرند پری ترکیه",
    "Russian_Grand_Prix": "گرند پری روسیه",
    "Tuscan_Grand_Prix": "گرند پری توسکان",
    "Eifel_Grand_Prix": "گرند پری ایفل",
    "Sakhir_Grand_Prix": "گرند پری ساخیر",
    "Chinese_Grand_Prix": "گرند پری چین",
    "German_Grand_Prix": "گرندپری آلمان",
    "Mexican_Grand_Prix": "گرندپری مکزیک",
    "Brazilian_Grand_Prix": "گرندپری برزیل",
    "70th_Anniversary_Grand_Prix": "گرندپری بریتانیا (70 سالگی)"
}

sessions_convert = {
    "Practice_1": "FP1",
    "Practice_2": "FP2",
    "Practice_3": "FP3",
    "Sprint_Qualifying": "SQ"
}
type_tr = {
    "Practice_1": "تمرین اول",
    "Practice_2": "تمرین دوم",
    "Practice_3": "تمرین سوم",
    "FP1": "تمرین اول",
    "FP2": "تمرین دوم",
    "FP3": "تمرین سوم",
    "Qualifying": "تعیین خط",
    "Race": "مسابقه"
}
def check_and_limit(user_id):
    current_time = time.time()
    if user_id not in user_messages:
        user_messages[user_id] = []
    user_messages[user_id] = [t for t in user_messages[user_id] if current_time - t < 30]
    user_messages[user_id].append(current_time)
    if len(user_messages[user_id]) > 20:
        return True
    return False


def check_admin(user_id):
    is_admin = cur.execute(f"SELECT * FROM admins WHERE _id = {user_id}").fetchone()
    return True if is_admin is not None else False

def check_lang(user_id):
    user = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
    if user is None:
        lang = None
    else:
        lang = user[1]
    print(lang)
    return lang

def check_date_passed(input_date):
    # تبدیل تاریخ ورودی به شی datetime
    input_datetime = datetime.strptime(input_date, '%Y-%m-%d')
    
    # تاریخ امروز
    today = datetime.now().date()
    
    # بررسی آیا تاریخ ورودی از امروز گذشته است یا خیر
    if input_datetime.date() < today:
        return True
    else:
        return False
def get_public_keys(user_id):
    user = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
    if user is None:
        lang = None
        return None
    else:
        lang = user[1]
        bot_text = None
        if lang == 1:
            bot_text = config.EN_TEXT
        else:
            bot_text = config.TEXT
        k = [
            [Button.text(bot_text["archive"], resize=True)],
            [Button.text(bot_text["reply"]), Button.text(bot_text["championship_calendar"])],
            [Button.text(bot_text["rules"]), Button.text(bot_text["sports_meeting"]), Button.text(bot_text["account"])],
        ]
        return k
def admin_public_keys(user_id):
    user = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
    if user is None:
        lang = None
        return None
    else:
        lang = user[1]
        bot_text = None
        if lang == 1:
            bot_text = config.EN_TEXT
        else:
            bot_text = config.TEXT
        k = [
                [Button.text(bot_text["panel"])],
                [Button.text(bot_text["archive"], resize=True)],
                [Button.text(bot_text["reply"]), Button.text(bot_text["championship_calendar"])],
                [Button.text(bot_text["rules"]), Button.text(bot_text["sports_meeting"]), Button.text(bot_text["account"])],
        ]
        return k
@bot.on(events.CallbackQuery())
async def call_handler(event):
    user_id = event.sender_id
    msg_id = event.original_update.msg_id
    if event.data == b'lang:en':
        en = 1
        up_en = cur.execute(f"UPDATE users SET lang = {en} WHERE id={user_id}")
        con.commit()
        bot_text = config.EN_TEXT
        en = bot_text["EN_SELECTED"]
        is_admin = check_admin(user_id)
        keys = get_public_keys(user_id)
        if is_admin:
            keys = admin_public_keys(user_id)
        await bot.delete_messages(user_id, msg_id)
        await bot.send_message(user_id, en, buttons=keys)
    elif event.data == b'lang:fa':
        fa = 2
        up_fa = cur.execute(f"UPDATE users SET lang = {fa} WHERE id={user_id}")
        con.commit()
        bot_text = config.TEXT
        fa = bot_text["FA_SELECTED"]
        is_admin = check_admin(user_id)
        keys = get_public_keys(user_id)
        if is_admin:
            keys = admin_public_keys(user_id)
        await bot.delete_messages(user_id, msg_id)
        await bot.send_message(user_id, fa, buttons=keys)


@bot.on(events.NewMessage(chats=[1647875091]))
async def save_msg(event):
    text = event.raw_text
    msg_id = event.original_update.message.id
    hashtags = config.extract_hashtags(text)
    if len(hashtags) == 0:
        return
    for hashtag in hashtags:
        data = [
            (msg_id, "#" + hashtag)
        ]
        cur.executemany("INSERT INTO hashtag VALUES(?,?)", data)
        con.commit()
    print("hashtags saved to database")


@bot.on(events.NewMessage())
async def pay(event):
    user_id = event.sender_id
    if check_admin(user_id) is False:
        if check_and_limit(user_id):
            await event.reply("شما بیش از حد مجاز پیام ارسال کرده‌اید. لطفاً 30 ثانیه صبر کنید.")
            return
    lang = check_lang(user_id)
    if lang == 1:
        bot_text = config.EN_TEXT
    else:
        bot_text = config.TEXT
    back = Button.text(bot_text["back"], resize=True)
    if type(event.message.peer_id) == PeerChannel:
        chat_type = 'channel'
    elif type(event.message.peer_id) == PeerChat:
        chat_type = 'group'
    elif type(event.message.peer_id) == PeerUser:
        chat_type = 'user'
    else:
        chat_type = None
    if chat_type == 'group' or chat_type == 'channel':
        return
    join, entity = await config.join_check(user_id, bot)
    if join is False:
        full_info = await bot(GetFullChannelRequest(entity))
        chat_title = full_info.chats[0].title
        channel_username = full_info.chats[0].username
        if channel_username is None:
            channel_username = full_info.full_chat.exported_invite.link
        else:
            channel_username = f'https://t.me/{channel_username}'
        key = [
            [Button.url(text=chat_title, url=channel_username)],
            [Button.url(bot_text["Membership_Confirmation"], url=f"{config.BOT_ID}?start=check")]
        ]
        await event.reply(bot_text["pls_join"], buttons=key)
    else:
        user = cur.execute(f"SELECT * FROM users WHERE id={user_id}").fetchone()
        text = event.raw_text
        amount = 0
        end = False
        you = False
        pay = False
        if text == bot_text["big_heart"]:
            amount = 2000000
            pay = True
        elif text == bot_text["rules"]:
            keys = [
                [
                    Button.text(bot_text["rules_show"], resize=True),
                ],
                [
                    Button.text(bot_text["account_setup"]),
                    Button.text(bot_text["language"]),
                ],
                [
                    Button.text(bot_text["version"]),
                    Button.text(bot_text["delete_account"]),
                    Button.text(bot_text["upgrade_level"]),
                ],
                [
                    back
                ],
            ]
            await event.reply(bot_text["select"], buttons=keys)
        elif text == bot_text["delete_account"]:
            keys = [
                [
                    Button.inline(bot_text["yes"], b'yes'),
                    Button.inline(bot_text["no"], b'no')
                ],
                [
                    Button.inline(bot_text["cancel"], b'cancel')
                ]
            ]
            async with bot.conversation(user_id, timeout=200) as conv:
                await conv.send_message(bot_text["sure_delete"], buttons=keys)
                response = await conv.wait_event(events.CallbackQuery())
                data = response.data
                if data == b'yes':
                    find_user = cur.execute(f"SELECT * FROM users WHERE id={user_id}").fetchone()
                    cur.execute(f"DELETE FROM users WHERE id = {user_id}")
                    cur.execute(f"DELETE FROM invite WHERE user_id = {user_id}")
                    con.commit()
                    print(int(time.time()))
                    print(find_user)
                    cur.execute(f"INSERT INTO deleted_accounts VALUES ({user_id}, {find_user[1]}, {find_user[2]}, '{find_user[3]}', {find_user[4]}, {find_user[5]}, {find_user[6]}, {find_user[7]}, {find_user[8]}, '{find_user[9]}', {find_user[10]}, '{find_user[11]}', {int(time.time())})")
                    con.commit()
                    await conv.send_message(bot_text["account_deleted"])
                    return
                else:
                    await conv.send_message(bot_text["canceled"])
                    return
        elif text == bot_text["delete_list"]:
            text = ""
            delete_users = cur.execute("SELECT * FROM deleted_accounts").fetchall()
            for user in delete_users:
                print(user)
                num_id = user[0]
                join_date = user[3]
                sub_count = user[4]
                score = user[5]
                protection = user[7]
                fantasy = user[6]
                validity = user[8]
                user_level = user[10]
                delete_time = user[12]
                dt_obj = datetime.fromtimestamp(delete_time)
                delete_time = jdatetime.datetime.fromgregorian(
                    year=dt_obj.year,
                    month=dt_obj.month,
                    day=dt_obj.day,
                    hour=dt_obj.hour,
                    minute=dt_obj.minute,
                    second=dt_obj.second,
                )
                delete_time = f"{delete_time.year}-{delete_time.month}-{delete_time.day} {delete_time.hour}:{delete_time.minute}:{delete_time.second}"
                if user_level == "1":
                    user_level = bot_text["level_one"]
                elif user_level == "2":
                    user_level = bot_text["level_two"]
                elif user_level == "3":
                    user_level = bot_text["level_three"]
                tel_user = await bot.get_entity(num_id)
                first_name = tel_user.first_name
                last_name = tel_user.last_name
                username = tel_user.username if tel_user.username is not None else '❌'
                full_name = first_name + last_name if last_name is not None else first_name
                a_tag = f'<a href="tg://user?id={num_id}">{full_name}</a>'
                c_tag = f'<code>{num_id}</code>'
                if lang == 1:
                    b_tag = "<b>info</b>"
                    text += "\n{btag}\n\n" \
                                "⁣👦🏻name: {name}\n" \
                                "🌐id: {username}\n" \
                                "👤number id: {num_id}\n" \
                                "🕰join date: {join_date}\n" \
                                "🌟level: {user_level}\n" \
                                "⭐️score count: {score}\n" \
                                "💳validity: {validity}\n" \
                                "💰sub collection count: {sub_count}\n" \
                                "💵amount of support: {protection}\n" \
                                "💎fantasy coins: {fantasy}\n" \
                                "delete time: {delete_time}\n".format(num_id=c_tag, join_date=join_date,
                                                                      sub_count=sub_count,
                                                                      protection=protection, score=score,
                                                                      fantasy=fantasy,
                                                                      validity=validity, name=a_tag, username=username,
                                                                      btag=b_tag,user_level=user_level,
                                                                      delete_time=delete_time)
                    text += "\n" + "➖➖➖➖➖➖➖➖➖"
                else:
                    b_tag = f'<b>اطلاعات</b>'
                    text += "\n{btag}\n\n" \
                                "⁣👦🏻نام: {name}\n" \
                                "🌐آیدی: {username}\n" \
                                "👤آیدی عددی: {num_id}\n" \
                                "🕰زمان عضویت: {join_date}\n" \
                                "🌟سطح عضویت: {user_level}\n" \
                                "⭐️تعداد امتیاز: {score}\n" \
                                "💳میزان اعتبار: {validity}\n" \
                                "💰تعداد زیر مجموعه: {sub_count}\n" \
                                "💵مقدار حمایت: {protection}\n" \
                                "💎تعداد سکه فانتزی: {fantasy}\n" \
                                "تاریخ حذف: {delete_time}".format(num_id=c_tag, join_date=join_date,
                                                                      sub_count=sub_count,
                                                                      protection=protection, score=score,
                                                                      fantasy=fantasy,
                                                                      validity=validity, name=a_tag, username=username,
                                                                      btag=b_tag,
                                                                      user_level=user_level, delete_time=delete_time)
                    text += "\n" + "➖➖➖➖➖➖➖➖➖"
            await bot.send_message(user_id, text, parse_mode="html")
        elif text == bot_text["sports_meeting"]:
            await event.reply(bot_text["updating"])
            # keys = [
            #     [
            #         Button.text(bot_text["scores"]),
            #     ],
            #     [
            #         Button.text(bot_text["fantasy"]),
            #         Button.text(bot_text["forecast"], resize=True),
            #     ],
            #     [
            #         Button.text(bot_text["show_table"]),
            #         Button.text(bot_text["set_notifications"]),
            #         Button.text(bot_text["in_person_meeting"]),
            #     ],
            #     [
            #         back
            #     ]
            # ]
            # await event.reply(bot_text["select"], buttons=keys)
        elif text == bot_text["account_setup"]:
            keys = [
                [
                    Button.text(bot_text["time_setup"]),
                    Button.text(bot_text["set_notifications"])
                ],
                [
                    Button.text(bot_text["back"], resize=1)
                ]
            ]
            await event.reply(bot_text["select"], buttons=keys)
        elif text == bot_text["set_notifications"]:
            keys = [
                [
                    Button.text(bot_text["enable_notifications"]),
                    Button.text(bot_text["disable_notifications"])
                ],
                [
                    Button.text(bot_text["back"])
                ]
            ]
            await event.reply(bot_text["select"], buttons=keys)
        elif text == bot_text["enable_notifications"]:
            cur.execute(f"UPDATE users SET notifications = 'yes' WHERE id = {user_id}")
            await event.reply(bot_text["notifications_enabled"])
        elif text == bot_text["disable_notifications"]:
            cur.execute(f"UPDATE users SET notifications = 'no' WHERE id = {user_id}")
            await event.reply(bot_text["notifications_disabled"])
        elif text == bot_text["language"]:
            keys = [
                [
                    Button.text(bot_text["fa"]),
                    Button.text(bot_text["en"]),
                ],
                [
                    Button.text(bot_text["back"], resize=True)
                ]
            ]
            await event.reply(bot_text["select_lang"], buttons=keys)
        elif text == bot_text["fa"]:
            cur.execute(f"UPDATE users SET lang = 2 WHERE id = {user_id}")
            con.commit()
            bot_text = config.TEXT
            ch = check_admin(user_id)
            if ch is False:
                keys = get_public_keys(user_id)
            else:
                keys = admin_public_keys(user_id)
            await event.reply(bot_text["FA_SELECTED"], buttons= keys)
        elif text == bot_text["en"]:
            cur.execute(f"UPDATE users SET lang = 1 WHERE id = {user_id}")
            con.commit()
            bot_text = config.EN_TEXT
            ch = check_admin(user_id)
            if ch is False:
                keys = get_public_keys(user_id)
            else:
                keys = admin_public_keys(user_id)
            await event.reply(bot_text["EN_SELECTED"], buttons= keys)
        elif text == bot_text["join_channel_btn"]:
            is_admin = check_admin(user_id)
            if is_admin is False:
                keys = get_public_keys(user_id)
                await event.reply(bot_text["select"], buttons=keys)
            else:
                keys = [
                    [
                        Button.text(bot_text["create_join_channel"], resize=True),
                        Button.text(bot_text["show_join_channel"])
                    ],
                    [
                        Button.text(bot_text["back"])
                    ]
                ]
                await event.reply(bot_text["select"], buttons=keys)
        elif text == bot_text["create_join_channel"]:
            is_admin = check_admin(user_id)
            if is_admin is False:
                keys = get_public_keys(user_id)
                await event.reply(bot_text["select"], buttons=keys)
            else:
                async with bot.conversation(user_id) as conv:
                    await conv.send_message(bot_text["enter_channel_id"])
                    try:
                        channel_id = await conv.get_response(timeout=120)
                        channel_id = channel_id.raw_text
                    except asyncio.exceptions.TimeoutError:
                        await conv.send_message(bot_text["timeout_error"])
                        return
                    if channel_id == bot_text["cancel"] or channel_id == bot_text["back"]:
                        await conv.send_message(bot_text["canceled"])
                        return
                    channel_num = randint(1000, 9999)
                    cur.execute(f"INSERT INTO join_channel VALUES ('{channel_id}', {False}, {channel_num})")
                    con.commit()
                    await conv.send_message(bot_text["successfully"])
        elif text == bot_text["show_join_channel"]:
            count_channels = cur.execute("SELECT * FROM join_channel").fetchall()
            count_channels = len(list(count_channels))
            if count_channels == 0:
                await event.reply(bot_text["not_found"])
            else:
                channels = cur.execute("SELECT * FROM join_channel").fetchall()[:5]
                for channel_link, senior, channel_num in channels:
                    key = [
                        Button.inline(bot_text["delete_btn"], str.encode("delete_channel:" + str(channel_num))),
                    ]
                    if senior == 0:
                        key.append(Button.inline(bot_text["senior_channel"], str.encode("senior_channel:" + str(channel_num))))
                    else:
                        key.append(Button.inline(bot_text["down_channel"], str.encode("down_channel:" + str(channel_num))))
                    full_text = f"{ bot_text['channel_id'] }: {channel_link} \n {bot_text['senior']}: {senior}"
                    await event.reply(full_text, buttons=key)
                if count_channels > 5:
                    items_per_page = 5
                    pages = count_channels // items_per_page
                    if count_channels % items_per_page != 0:
                        pages += 1
                    paginate_keys = paginate('show_join', 1, pages, ':')
                    await event.reply(bot_text["come_next"], buttons=paginate_keys)   
        elif text == bot_text["rules_show"]:
            await event.reply(bot_text["rules_text"])
        elif text == bot_text["archive"]:
            keys = [
                [
                    Button.text(bot_text["page_one"], resize=True)
                ],
                [
                    Button.text(bot_text["page_two"]),
                    Button.text(bot_text["page_three"])
                ],
                [
                    Button.text(bot_text["forth_page"])
                ],
                [
                    back
                ]
            ]
            await event.reply(bot_text["select"], buttons=keys)
        elif text == bot_text["fantasy"]:
            await event.reply(bot_text["coming_soon"])
        # elif text == bot_text["reply"]:
        #     await event.reply(bot_text["updating"])
        elif text == bot_text["championship_calendar"]:
            buttons = [
                [
                    Button.text(bot_text["calender_by_year"], resize=True),
                    Button.text(bot_text["next_grand_prix"], resize=True),
                ],
                [
                    Button.text(bot_text["time_until"])
                ],
                [
                    back
                ]
            ]
            await event.reply(bot_text["select"], buttons=buttons)
        elif text == bot_text["time_until"]:
            time_until = funections.get_time_until()
            if time_until is None:
                time_until = bot_text["session_ended"]
            await event.reply(time_until)
        elif text == bot_text["next_grand_prix"]:
            next_grand = funections.next_grand_prix()
            if next_grand is None:
                next_grand = bot_text["session_ended"]
            await event.reply(next_grand)
        elif text == bot_text["calender_by_year"]:
            async with bot.conversation(user_id) as conv:
                year_keys = [
                    [
                        Button.inline("2025", b'2025')
                    ],
                    [
                        Button.inline("2024", b'2024')
                    ],
                    [
                        Button.inline("2023", b'2023')
                    ],
                    [
                        Button.inline("2022", b'2022')
                    ],
                    [
                        Button.inline("2021", b'2021')
                    ],
                    [
                        Button.inline("2020", b'2020')
                    ],
                    [
                        Button.inline("2019", b'2019')
                    ],
                    [
                        Button.inline("2018", b'2018')
                    ],
                    [
                        Button.inline(bot_text["cancel"], b'cancel')
                    ]
                ]
                ask_year = await conv.send_message(bot_text["select_year"], buttons=year_keys)
                try:
                    year_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                    await bot.delete_messages(user_id, ask_year.id)
                except TimeoutError:
                    await conv.send_message(bot_text["timeout_error"])
                    await bot.delete_messages(user_id, ask_year.id)
                    return
                year_data = year_res.data
                if year_data == b'cancel':
                    await conv.send_message(bot_text["canceled"])
                    await bot.delete_messages(user_id, ask_year.id)
                    await conv.cancel_all()
                else:
                    year = int(year_data)
                    text = get_year_calender(year)
                    await event.reply(text)
        elif text == bot_text["account"]:
            keys = [
                [
                    Button.text(bot_text["user_information"]),
                ],
                [
                    Button.text(bot_text["sub_collection"], resize=1),
                    Button.text(bot_text["personal_account"]),
                ],
                [
                    Button.text(bot_text["support"]),
                    Button.text(bot_text["protection"]),
                    Button.text(bot_text["search"]),
                ],
                [
                    Button.text(bot_text["back"])
                ]
            ]
            await event.reply(bot_text["select"], buttons=keys)
        elif text == bot_text["search"]:
            keys = [
                [
                    Button.text(bot_text["search_in_channel"]),
                    Button.text(bot_text["search_in_bot"], resize=True)
                ],
                [
                    Button.text(bot_text["back"])
                ]
            ]
            await event.reply(bot_text["select"], buttons=keys)
        elif text == bot_text["support"]:
            keys = [
                [
                    Button.text(bot_text["connect_admin"],resize=1),
                    Button.text(bot_text["idealization"])
                ],
                [
                    Button.text(bot_text["back"])
                ]
            ]
            await event.reply(bot_text["select"], buttons=keys)
        elif text == bot_text["all_send"]:
            is_admin = check_admin(user_id)
            if is_admin:
                async with bot.conversation(user_id, timeout=1000) as conv:

                    await conv.send_message(bot_text["all_send_text"])

                    image_msg = await conv.get_response()

                    image_path = None

                    if image_msg.media is not None:

                        image_path = await image_msg.download_media()

                        await conv.send_message(bot_text["all_send_tx"])

                        text = await conv.get_response()

                        q_text = text.message

                    else:

                        if image_msg.message == bot_text["back"]:

                            key = [

                                Button.text(bot_text["back"], resize=1)

                            ]

                            await bot.send_message(user_id, bot_text['canceled'], buttons=key)

                            return

                        else:

                            q_text = image_msg.message

                    users = cur.execute(f"SELECT id FROM users").fetchall()
                    for user in users:

                        user_id_ = user[0]

                        try:

                            await bot.send_message(user_id_, q_text, file=image_path)

                        except:

                            continue
        elif text == bot_text["one_send"]:
            is_admin = check_admin(user_id)
            if is_admin:
                async with bot.conversation(user_id, timeout=1000) as conv:
                    ask_user_id = await conv.send_message(bot_text["enter_user_id"])
                    while True:
                        try:
                            user_id_get = await conv.get_response(timeout=120)
                            if user_id_get.raw_text == bot_text["cancel"] or user_id_get.raw_text == bot_text["back"]:
                                await conv.send_message(bot_text["canceled"])
                                await bot.delete_messages(user_id, ask_user_id.id)
                                return
                            user_id_get = int(user_id_get.raw_text)
                            break
                        except ValueError:
                            await conv.send_message(bot_text["just_num"])
                        except TimeoutError:
                            await conv.send_message(bot_text["timeout_error"])
                            await bot.delete_messages(user_id, ask_user_id.id)
                            return
                    find_user = cur.execute(f"SELECT score FROM users WHERE id = {user_id_get}").fetchone()
                    if find_user is None:
                        await event.reply(bot_text["not_found"])
                        return
                    else:
                        await conv.send_message(bot_text["all_send_text"])

                        image_msg = await conv.get_response()

                        image_path = None

                        if image_msg.media is not None:

                            image_path = await image_msg.download_media()

                            await conv.send_message(bot_text["all_send_tx"])

                            text = await conv.get_response()

                            q_text = text.message

                        else:

                            if image_msg.message == bot_text["back"]:

                                key = [

                                    Button.text(bot_text["back"], resize=1)

                                ]

                                await bot.send_message(user_id, bot_text['canceled'], buttons=key)

                                return

                            else:

                                q_text = image_msg.message

                        user = cur.execute(f"SELECT id FROM users WHERE id = {user_id_get}").fetchone()
                        user_id_ = user[0]
                        print(user_id_)
                        try:

                            await bot.send_message(user_id_, q_text, file=image_path)

                        except Exception as e:
                            print(e)
                            pass
        elif text == bot_text["idealization"]:
            idealization_count = len(list(cur.execute(f"SELECT * FROM idealization WHERE user_id = {user_id}").fetchall()))
            if idealization_count + 1 > 2:
                await event.reply(bot_text["idealization_full"])
                return
            async with bot.conversation(user_id, timeout=1000) as conv:
                await conv.send_message(bot_text["question_image_idea"])
                image_msg = await conv.get_response()
                image_path = None
                if image_msg.media is not None:
                    image_path = await image_msg.download_media()
                    await conv.send_message(bot_text["question_text_idea"])
                    text = await conv.get_response()
                    q_text = text.message
                else:
                    if image_msg.message == bot_text["cancel"] or image_msg.message == bot_text["back"]:
                        key = [
                            Button.text(bot_text["back"])
                        ]
                        await bot.send_message(user_id, bot_text['canceled'], buttons=key)
                        return
                    else:
                        q_text = image_msg.message
            if q_text == bot_text["cancel"] or q_text == bot_text["back"]:
                await conv.send_message(bot_text["canceled"])
                await conv.cancel_all()
            find_user = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
            join_time = find_user[3]
            user_level = find_user[10]
            tel_user = await bot.get_entity(user_id)
            first_name = tel_user.first_name
            last_name = tel_user.last_name
            username = tel_user.username if tel_user.username is not None else '❌'
            full_name = first_name + last_name if last_name is not None else first_name
            if lang == 1:
                full_text = f"idea text: **{q_text}**\nuser id: `{user_id}`\nusername: {username}\nfull name: {full_name}\nJoin Date: {join_time}"
            else:
                full_text = f"متن ایده: **{q_text}**\nآیدی کاربر: `{user_id}`\nنام کاربری: {username}\nنام کامل: {full_name}\nزمان عضویت: {join_time}"
            admins = cur.execute("SELECT * FROM admins").fetchall()
            for admin in admins:
                await bot.send_message(int(admin[0]), full_text, file=image_path)
            cur.execute(f"INSERT INTO idealization VALUES ({user_id})")
            con.commit()
            await event.reply(bot_text["successfully"])

        elif text == bot_text["tickets"]:
            is_admin = check_admin(user_id)
            if is_admin is False:
                keys = get_public_keys(user_id)
                await event.reply(bot_text["select"], buttons=keys)
            else:
                find_count = len(cur.execute("SELECT * FROM tickets WHERE status='open'").fetchall())
                if find_count == 0:
                    await bot.send_message(user_id, bot_text["not_found"])
                    return
                await bot.send_message(user_id, bot_text['welcome_show_tickets'])
                tickets = cur.execute("SELECT * FROM tickets WHERE status='open'").fetchall()[:5]
                items_per_page = 5
                pages = find_count // items_per_page
                if find_count % items_per_page != 0:
                    pages += 1
                paginate_keys = paginate('show_ticket', 1, pages, ':')
                for ticket in tickets:
                    banner_media = ticket[0]
                    banner_text = ticket[1]
                    banner_user = ticket[3]
                    ticket_count = ticket[2]
                    full_question = f'{bot_text["ticket_text"]}:{banner_text}\n' \
                                    f'{bot_text["ticket_count"]}:{ticket_count}\n' \
                                    f'{bot_text["ticket_user_id"]}:`{banner_user}`'

                    key = [
                        Button.inline(bot_text['ticket_answer'], data=str.encode('ticket_answer:' + str(ticket_count))),
                        Button.inline(bot_text['close_ticket'],data=str.encode('close_ticket:' + str(ticket_count))),
                    ]
                    try:
                        await bot.send_message(user_id, full_question, file=banner_media, buttons=key)
                    except:
                        await bot.send_message(user_id,full_question, buttons=key)
                try:
                    await bot.send_message(user_id, bot_text['come_next'], buttons=paginate_keys)
                except:
                    pass
        elif text == bot_text["connect_admin"]:
            async with bot.conversation(user_id, timeout=1000) as conv:
                await conv.send_message(bot_text["question_image"])
                image_msg = await conv.get_response()
                image_path = None
                if image_msg.media is not None:
                    image_path = await image_msg.download_media()
                    await conv.send_message(bot_text["question_text"])
                    text = await conv.get_response()
                    q_text = text.message
                else:
                    if image_msg.message == bot_text["cancel"] or image_msg.message == bot_text["back"]:
                        key = [
                            Button.text(bot_text["back"])
                        ]
                        await bot.send_message(user_id, bot_text['canceled'], buttons=key)
                        return
                    else:
                        q_text = image_msg.message
            if q_text == bot_text["cancel"] or q_text == bot_text["back"]:
                await conv.send_message(bot_text["canceled"])
                await conv.cancel_all()
            find_count = cur.execute("SELECT COUNT(*) FROM tickets").fetchone()[0] + 1
            data = [
                (image_path, q_text, find_count, user_id, 'open')
            ]
            cur.executemany("INSERT INTO tickets(media,text,count,user_id,status) VALUES(?,?,?,?,?)", data)
            con.commit()
            key = [
                Button.text(bot_text["back"])
            ]
            await bot.send_message(user_id, bot_text["ticket_successfully"], buttons=key)
            admins = cur.execute("SELECT * FROM admins").fetchall()
            for admin in admins:
                ad_id = admin[0]
                print(ad_id)
                key = [
                    Button.inline(bot_text["ticket_answer"],
                    data=str.encode('ticket_answer:' + str(find_count)))
                ]
                user_details = await bot.get_entity(user_id)
                full_name = user_details.first_name + user_details.last_name if user_details.last_name is not None else user_details.first_name
                await bot.send_message(ad_id,
                                    bot_text["admin_notification"].format(num=find_count,
                                                                                                        text=q_text,
                                                                                                        id=user_id,
                                                                                                        name=full_name,
                                                                                                        username=user_details.username
                                                                                                        ),
                                    buttons=key)
        elif text == bot_text["search_in_channel"]:
            async with bot.conversation(user_id, timeout=1000) as conv:
                await conv.send_message(bot_text["enter_hashtag"])
                hashtag = await conv.get_response()
                if hashtag.raw_text == bot_text["cancel"] or hashtag.raw_text == bot_text["back"]:
                    key = Button.text(bot_text["back"], resize=True)
                    await conv.send_message(bot_text["canceled"], buttons=key)
                    await conv.cancel_all()
                query = f"SELECT * FROM hashtag WHERE text LIKE '%{hashtag.raw_text}%'"
                search = cur.execute(query).fetchall()
                if len(search) == 0:
                    key = Button.text(bot_text["back"], resize=True)
                    await conv.send_message(bot_text["not_found"], buttons=key)
                    await conv.cancel_all()
                result = "\nنتایج پیدا شده👇\n"
                for tag in search:
                    result += config.CHANNEL_ID + "/" + str(tag[0]) + "\n"
                await conv.send_message(result)
        elif text == bot_text["search_in_bot"]:
            async with bot.conversation(user_id, timeout=1000) as conv:
                msg = await conv.send_message(bot_text["enter_button"])
                btn = await conv.get_response()
                if btn.raw_text == bot_text["cancel"] or btn.raw_text == bot_text["back"]:
                    key = Button.text(bot_text["back"], resize=True)
                    await conv.send_message(bot_text["canceled"], buttons=key)
                    await conv.cancel_all()
                if btn.raw_text.startswith("_") is False:
                    await event.reply(bot_text["underline"])
                    return
                query = f"SELECT * FROM btn WHERE text LIKE '%{btn.raw_text}%'"
                search = cur.execute(query).fetchall()
                if len(search) == 0:
                    key = Button.text(bot_text["back"], resize=True)
                    await conv.send_message(bot_text["not_found"], buttons=key)
                    await conv.cancel_all()
                keys = []
                for s in search:
                    key = [
                        Button.text(s[1])
                    ]
                    keys.append(key)
                result = "\nنتایج پیدا شده👇\n"

                await conv.send_message(result, buttons=keys)
                return
        elif text == bot_text["protection"]:
            keys = [
                [Button.text(bot_text["big_heart"])],
                [Button.text(bot_text["coffee"]), Button.text(bot_text["dinner"])],
                [Button.text(bot_text["small_party"]), Button.text(bot_text["big_party"]),
                 Button.text(bot_text["you_pay"], resize=True)],
                [Button.text(bot_text["back"])]
            ]
            await event.reply(bot_text["select"], buttons=keys)
        elif text == bot_text["soon"]:
            await event.reply(bot_text["coming_soon"])
        elif text == bot_text["bot_ping"]:
            start = time.time()
            pm = await event.reply(bot_text["getting_ping"])
            end = time.time()
            ping = end - start
            if lang == 1:
                await pm.edit(f"bot ping is {ping:.2f}s")
            else:
                await pm.edit(f"پینگ ربات {ping:.2f} ثانیه است")
            time.sleep(5)
            await bot.delete_messages(user_id, pm.id)
        elif text.startswith("/start") or text == bot_text["back"]:
            start_parameter = event.message.message.split()
            if len(start_parameter) == 2:
                if start_parameter[1] != "check":
                    start_parameter = int(start_parameter[1])
                    f_user = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
                    if start_parameter != user_id and f_user is None:
                        find_user = cur.execute(f"SELECT * FROM users WHERE id = {start_parameter}").fetchone()
                        if find_user is None:
                            return
                        sub_count = find_user[4]
                        user_score = find_user[5]
                        find_invite = cur.execute(f"SELECT * FROM invite WHERE user_id = {user_id}").fetchone()
                        if find_invite is None:
                            find_invites = len(cur.execute(f"SELECT * FROM invite WHERE invite_id = {start_parameter}").fetchall())
                            if find_invites + 1 == 3:
                                await bot.send_message(start_parameter, bot_text["three_sub_count"])
                                cur.execute(f"UPDATE users SET score = {user_score + 10} WHERE id = {start_parameter}")
                                con.commit()
                            elif find_invites + 1 == 5:
                                await bot.send_message(start_parameter, bot_text["five_sub_count"])
                                cur.execute(f"UPDATE users SET score = {user_score + 20} WHERE id = {start_parameter}")
                                con.commit()
                            data = [
                                (user_id, start_parameter)
                            ]
                            cur.executemany(f"INSERT INTO invite VALUES (?,?)", data)
                            con.commit()
                            score_sub = user_score + config.SUB_COIN
                            print(score_sub)
                            cur.execute(f"UPDATE users SET score = {score_sub} WHERE id = {start_parameter}")
                            con.commit()
                            sub_score = sub_count + 1
                            if sub_score >= 10:
                                if find_user[10] == "1":
                                    cur.execute(f"UPDATE users SET level = 2 WHERE id = {start_parameter}")
                                    await bot.send_message(start_parameter, bot_text["level_two_up"])
                            if sub_score >= 20:
                                if find_user[10] == "2":
                                    cur.execute(f"UPDATE users SET level = 2 WHERE id = {start_parameter}")
                                    await bot.send_message(start_parameter, bot_text["level_three_up"])
                            print(sub_score)
                            cur.execute(f"UPDATE users SET sub_count = {sub_score} WHERE id = {start_parameter}")
                            con.commit()


            user = cur.execute(f"SELECT * FROM users WHERE id={user_id}").fetchone()
            if user is None:
                currentDateAndTime = datetime.now()
                score_time = currentDateAndTime + timedelta(days=1)
                currentTime = currentDateAndTime.strftime("%Y-%m-%d %H:%M:%S")
                current_score_time = score_time.strftime("%Y-%m-%d %H:%M:%S")
                start_score_add = config.START_SCORE + config.DAILY_COIN
                data = [
                    (user_id, None, False, currentTime, 0, start_score_add, 0, 0, 0, current_score_time, 1, "iran"),
                ]
                cur.executemany(f"INSERT INTO users VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", data)
                con.commit()
                await event.reply(bot_text["start_score"])
                await event.reply(bot_text["daily_coin"])
                keys = [
                    [Button.inline(bot_text["en"], b'lang:en'),
                     Button.inline(bot_text["fa"], b'lang:fa')
                     ]
                ]
                select = bot_text["select_lang"]
                await event.reply(select, buttons=keys)
            else:
                lang_ch = user[1]
                if lang_ch is None:
                    keys = [
                        [Button.inline(bot_text["en"], b'lang:en'),
                         Button.inline(bot_text["fa"], b'lang:fa')
                         ]
                    ]
                    select = bot_text["select_lang"]
                    await event.reply(select, buttons=keys)
                else:
                    is_admin = cur.execute(f"SELECT * FROM admins WHERE _id = {user_id}").fetchone()
                    keys = get_public_keys(user_id)
                    if is_admin is not None:
                        keys = admin_public_keys(user_id)
                    await event.reply(bot_text["select"], buttons=keys)
        elif text == bot_text["panel"]:
            is_admin = check_admin(user_id)
            if is_admin is False:
                keys = get_public_keys(user_id)
                await event.reply(bot_text["select"], buttons=keys)
            else:
                pn_keys = [
                    [
                        Button.text(bot_text["management"]),
                        Button.text(bot_text["data_management"]),
                        Button.text(bot_text["users"], resize=1)
                    ],
                    [
                        Button.text(bot_text["back"], resize=True)
                    ]
                ]
                await event.reply(bot_text["select"], buttons=pn_keys)
        elif text == bot_text["management"]:
            is_admin = check_admin(user_id)
            if is_admin is False:
                keys = get_public_keys(user_id)
                await event.reply(bot_text["select"], buttons=keys)
            else:
                keys = [
                    [
                        Button.text(bot_text["join_channel_btn"])
                    ],
                    [
                        Button.text(bot_text["words"], resize=True),
                        Button.text(bot_text["tickets"]),
                    ],
                    [
                        Button.text(bot_text["statistics_data"]),
                        Button.text(bot_text["statistics_small"]),
                        Button.text(bot_text["statistics_all"]),
                    ],
                    [
                        Button.text(bot_text["all_send"]),
                        Button.text(bot_text["one_send"])
                    ],
                    [
                        Button.text(bot_text["delete_list"])
                    ],
                    [
                        Button.text(bot_text["fia_info_management"])
                    ],
                    [Button.text(bot_text['back'])],
                ]
                await event.reply(bot_text["select"], buttons=keys)
        elif text == bot_text["statistics_data"]:
            count = len(cur.execute(f"SELECT * FROM statistics_all").fetchall())
            await event.reply(bot_text["statistics_data_text"].format(count=count))
        elif text == bot_text["statistics"]:
            keys = [
                [
                    Button.text(bot_text["statistics_all"]),
                    Button.text(bot_text["statistics_small"], resize=1),
                    Button.text(bot_text["statistics_data"], resize=1)
                ],
            ]
            await event.reply(bot_text["select"], buttons=keys)
        elif text == bot_text["statistics_small"]:
            async with bot.conversation(user_id, timeout=1000) as conv_all:
                keys_all = [
                    [
                        Button.inline(bot_text["rpm_statistics"], b'rs'),
                        Button.inline(bot_text["overtake_statistics"], b'os'),
                    ],
                    [
                        Button.inline(bot_text["map_viz_statistics"], b'ms'),
                        Button.inline(bot_text["downforce_statistics"], b'ds'),
                    ],
                    [
                        Button.inline(bot_text["top_trap_statistics"], b'ts'),
                        Button.inline(bot_text["start_reaction_statistics"], b'sr'),
                    ],
                    [
                        Button.inline(bot_text["g_force_all_info"], b'gr'),
                        Button.inline(bot_text["g_force_driver"], b'gd'),
                    ],
                    [
                        Button.inline(bot_text["plot_lap_times"], b'pd'),
                        Button.inline(bot_text["map_break_statistics"], b'mbs'),
                    ],
                    [
                        Button.inline(bot_text["all_statistics"], b'as'),
                        Button.inline(bot_text["strategy_statistics"], b'ss'),
                    ],
                    [
                        Button.inline(bot_text["data_to_pole"], b'dp'),
                        Button.inline(bot_text["lap_times_table"], b'lt'),
                    ],
                    [
                        Button.inline(bot_text["brake_configurations"], b'bc'),
                        Button.inline(bot_text["composite_perfomance"], b'cp'),
                    ],
                    [
                        Button.inline(bot_text["degradation_tyre"], b'dt'),
                        Button.inline(bot_text["weather_data"], b'wd'),
                    ],
                    [
                        Button.inline(bot_text["tyre_performance"], b'tp'),
                        Button.inline(bot_text["ers_analysis"], b'ea')
                    ],
                    [
                        Button.inline(bot_text["comparison_fastest_lap"], b'cf'),
                        Button.inline(bot_text["efficiency_breakdown"], b'eb'),
                    ],
                    [
                        Button.inline(bot_text["stress_index"], b'si')
                    ],
                    [
                        Button.inline(bot_text["cancel"], b'cancel')
                    ]
                ]
                await conv_all.send_message(bot_text["enter_statistics"], buttons=keys_all)
                response = await conv_all.wait_event(events.CallbackQuery())
                statistics_value = None
                if response.data == b'rs':
                    statistics_value = bot_text["rpm"]
                elif response.data == b'os':
                    statistics_value = bot_text["overtake"]
                elif response.data == b'ms':
                    statistics_value = bot_text["map_viz"]
                elif response.data == b'ds':
                    statistics_value = bot_text["down_force"]
                elif response.data == b'ts':
                    statistics_value = bot_text["top_speed"]
                elif response.data == b'sr':
                    statistics_value = bot_text["start_reaction"]
                elif response.data == b'gr':
                    statistics_value = bot_text["all_info"]
                elif response.data == b'gd':
                    statistics_value = bot_text["driver"]
                elif response.data == b'pd':
                    statistics_value = bot_text["lap_times"]
                elif response.data == b'mbs':
                    statistics_value = bot_text["map_break"]
                elif response.data == b'as':
                    statistics_value = bot_text["all"]
                elif response.data == b'ss':
                    statistics_value = bot_text["strategy"]
                elif response.data == b'dp':
                    statistics_value = bot_text["data_to_pole"]
                elif response.data == b'lt':
                    statistics_value = bot_text["lap_times_table"]
                elif response.data == b'bc':
                    statistics_value = bot_text["brake_configurations"]
                elif response.data == b'cp':
                    statistics_value = bot_text["composite_perfomance"]
                elif response.data == b'dt':
                    statistics_value = bot_text["degradation_tyre"]
                elif response.data == b'wd':
                    statistics_value = bot_text["weather_data"]
                elif response.data == b'tp':
                    statistics_value = bot_text["tyre_performance"]
                elif response.data == b'ea':
                    statistics_value = bot_text["ers_analysis"]
                elif response.data == b'cf':
                    statistics_value = bot_text["comparison_fastest_lap"]
                elif response.data == b'eb':
                    statistics_value = bot_text["efficiency_breakdown"]
                elif response.data == b'si':
                    statistics_value = bot_text["stress_index"]
                elif response.data == b'cancel':
                    return
                else:
                    await conv_all.send_message(bot_text["action_not_found"])
                    return
                count_all = cur.execute(f"SELECT * FROM statistics_small WHERE data = '{statistics_value}'").fetchall()
                count_all = len(count_all)
                await conv_all.send_message(bot_text["statistics_small_text"].format(data=statistics_value, count=count_all))
                return
        elif text == bot_text["statistics_all"]:
            async with bot.conversation(user_id, timeout=1000) as conv_all:
                keys_all = [
                    [
                        Button.inline(bot_text["rpm_statistics"], b'rs'),
                        Button.inline(bot_text["overtake_statistics"], b'os'),
                    ],
                    [
                        Button.inline(bot_text["map_viz_statistics"], b'ms'),
                        Button.inline(bot_text["downforce_statistics"], b'ds'),
                    ],
                    [
                        Button.inline(bot_text["top_trap_statistics"], b'ts'),
                        Button.inline(bot_text["start_reaction_statistics"], b'sr'),
                    ],
                    [
                        Button.inline(bot_text["g_force_all_info"], b'gr'),
                        Button.inline(bot_text["g_force_driver"], b'gd'),
                    ],
                    [
                        Button.inline(bot_text["plot_lap_times"], b'pd'),
                        Button.inline(bot_text["map_break_statistics"], b'mbs'),
                    ],
                    [
                        Button.inline(bot_text["all_statistics"], b'as'),
                        Button.inline(bot_text["strategy_statistics"], b'ss'),
                    ],
                    [
                        Button.inline(bot_text["data_to_pole"], b'dp'),
                        Button.inline(bot_text["lap_times_table"], b'lt'),
                    ],
                    [
                        Button.inline(bot_text["brake_configurations"], b'bc'),
                        Button.inline(bot_text["composite_perfomance"], b'cp'),
                    ],
                    [
                        Button.inline(bot_text["degradation_tyre"], b'dt'),
                        Button.inline(bot_text["weather_data"], b'wd')
                    ],
                    [
                        Button.inline(bot_text["tyre_performance"], b'tp'),
                        Button.inline(bot_text["ers_analysis"], b'ea')
                    ],
                    [
                        Button.inline(bot_text["comparison_fastest_lap"], b'cf'),
                        Button.inline(bot_text["efficiency_breakdown"], b'eb'),
                    ],
                    [
                        Button.inline(bot_text["stress_index"], b'si')
                    ],
                    [
                        Button.inline(bot_text["cancel"], b'cancel')
                    ]
                ]
                await conv_all.send_message(bot_text["enter_statistics"], buttons=keys_all)
                response = await conv_all.wait_event(events.CallbackQuery())
                statistics_value = None
                if response.data == b'rs':
                    statistics_value = bot_text["rpm"]
                elif response.data == b'os':
                    statistics_value = bot_text["overtake"]
                elif response.data == b'ms':
                    statistics_value = bot_text["map_viz"]
                elif response.data == b'ds':
                    statistics_value = bot_text["down_force"]
                elif response.data == b'ts':
                    statistics_value = bot_text["top_speed"]
                elif response.data == b'sr':
                    statistics_value = bot_text["start_reaction"]
                elif response.data == b'gr':
                    statistics_value = bot_text["all_info"]
                elif response.data == b'gd':
                    statistics_value = bot_text["driver"]
                elif response.data == b'pd':
                    statistics_value = bot_text["lap_times"]
                elif response.data == b'mbs':
                    statistics_value = bot_text["map_break"]
                elif response.data == b'as':
                    statistics_value = bot_text["all"]
                elif response.data == b'ss':
                    statistics_value = bot_text["strategy"]
                elif response.data == b'dp':
                    statistics_value = bot_text["data_to_pole"]
                elif response.data == b'lt':
                    statistics_value = bot_text["lap_times_table"]
                elif response.data == b'bc':
                    statistics_value = bot_text["brake_configurations"]
                elif response.data == b'cp':
                    statistics_value = bot_text["composite_perfomance"]
                elif response.data == b'dt':
                    statistics_value = bot_text["degradation_tyre"]
                elif response.data == b'wd':
                    statistics_value = bot_text["weather_data"]
                elif response.data == b'tp':
                    statistics_value = bot_text["tyre_performance"]
                elif response.data == b'ea':
                    statistics_value = bot_text["ers_analysis"]
                elif response.data == b'cf':
                    statistics_value = bot_text["comparison_fastest_lap"]
                elif response.data == b'eb':
                    statistics_value = bot_text["efficiency_breakdown"]
                elif response.data == b'si':
                    statistics_value = bot_text["stress_index"]
                elif response.data == b'cancel':
                    return
                else:
                    await conv_all.send_message(bot_text["action_not_found"])
                    return
                count_all = cur.execute(f"SELECT * FROM statistics_all WHERE data = '{statistics_value}'").fetchall()
                count_all = len(count_all)
                await conv_all.send_message(bot_text["statistics_all_text"].format(data=statistics_value, count=count_all))
                return
        elif text == bot_text["data_management"]:
            is_admin = check_admin(user_id)
            if is_admin is False:
                keys = get_public_keys(user_id)
                await event.reply(bot_text["select"], buttons=keys)
            else:
                keys = [
                    [
                        Button.text(bot_text["users_level"], resize=1),
                        Button.text(bot_text["coin_management"])
                    ],
                    [
                        Button.text(bot_text["grand"]),
                        Button.text(bot_text["grand_time"]),
                    ],
                    [
                        Button.text(bot_text["off_data"]),
                        Button.text(bot_text["off_all"]),
                    ],
                    [
                        Button.text(bot_text["save_reply"])
                    ],
                    [
                        Button.text(bot_text["back"])
                    ]
                ]
                await event.reply(bot_text["select"], buttons=keys)
        elif text == bot_text["grand_time"]:
            is_admin = check_admin(user_id)
            if is_admin is False:
                keys = get_public_keys(user_id)
                await event.reply(bot_text["select"], buttons=keys)
            else:
                keys = [
                    [
                        Button.text(bot_text["add_grand_time"]),
                        Button.text(bot_text["show_grand_time"])
                    ],
                    [
                        Button.text(bot_text["back"], resize=True)
                    ]
                ]
                await event.reply(bot_text["select"], buttons=keys)
        elif text == bot_text["add_grand_time"]:
            is_admin = check_admin(user_id)
            if is_admin is False:
                keys = get_public_keys(user_id)
                await event.reply(bot_text["select"], buttons=keys)
            else:
                async with bot.conversation(user_id, timeout=1000) as conv:
                    await conv.send_message(bot_text["ask_grand"])
                    grand_prix = await conv.get_response()
                    grand_prix = grand_prix.raw_text
                    if grand_prix == bot_text["cancel"] or grand_prix == bot_text["back"]:
                        await conv.send_message(bot_text["canceled"])
                        return
                    await conv.send_message(bot_text["ask_grand_event"])
                    session_type = await conv.get_response()
                    session_type = session_type.raw_text
                    session_dict = {
                        "FP1": "Practice_1",
                        "FP2": "Practice_2",
                        "FP3": "Practice_3",
                    }
                    if session_type in session_dict:
                        session_type = session_dict[session_type]
                    if session_type == bot_text["cancel"] or session_type == bot_text["back"]:
                        await conv.send_message(bot_text["canceled"])
                        return
                    await conv.send_message(bot_text["ask_time"])
                    grand_time = await conv.get_response()
                    grand_time = grand_time.raw_text
                    if grand_time == bot_text["cancel"] or grand_time == bot_text["back"]:
                        await conv.send_message(bot_text["canceled"])
                        return
                    await conv.send_message(bot_text["ask_date"])
                    grand_date = await conv.get_response()
                    grand_date = grand_date.raw_text
                    if grand_date == bot_text["cancel"] or grand_date == bot_text["back"]:
                        await conv.send_message(bot_text["canceled"])
                        return
                    notification_keys = [
                        [Button.inline(bot_text["yes"], b'yes_notification'), Button.inline(bot_text["no"], b'no_notification')]
                    ]
                    await conv.send_message(bot_text["select_notification"], buttons=notification_keys)
                    check_notification = await conv.wait_event(events.CallbackQuery())
                    if check_notification.data == b'no_notification':
                        check_notification = "no"
                    elif check_notification.data == b'yes_notification':
                        check_notification = "yes"
                    else:
                        await event.reply(bot_text["action_not_found"])
                        return
                    time_num = randint(1000, 9999)
                    cur.execute(f"INSERT INTO grand_time VALUES (?,?,?,?,?,?)", (grand_prix, session_type, grand_time, time_num, check_notification, grand_date))
                    con.commit()
                    await conv.send_message(bot_text["successfully"])
                    await conv.cancel_all()
        elif text == bot_text["show_grand_time"]:
            find_count = len(cur.execute("SELECT * FROM grand_time").fetchall())
            if find_count == 0:
                await event.reply(bot_text['not_found'])
                return
            await event.reply(bot_text['welcome_show_time'])
            find_grands = cur.execute("SELECT * FROM grand_time").fetchall()[:5]
            items_per_page = 5
            pages = find_count // items_per_page
            if find_count % items_per_page != 0:
                pages += 1
            paginate_keys = paginate('show_time', 1, pages, ':')
            for grand in find_grands:
                grand_num = grand[3]
                grand_name = grand[0]
                grand_time = grand[2]
                grand_event = grand[1]
                key = [
                    [
                        Button.inline(bot_text['delete_grand'], 'delete_time:' + str(grand_num)),
                    ]
                ]
                full_channel = f'{bot_text["grand_name"]}:{grand_name}\n{bot_text["time_event"]}:{grand_event}\n{bot_text["time"]}:`{grand_time}`'
                await bot.send_message(user_id, full_channel, buttons=key)
            try:
                await bot.send_message(user_id, bot_text['come_next'], buttons=paginate_keys)
            except:
                pass
        elif text == bot_text["coin_management"]:
            is_admin = check_admin(user_id)
            if is_admin is False:
                keys = get_public_keys(user_id)
                await event.reply(bot_text["select"], buttons=keys)
            else:
                keys = [
                    [
                        Button.text(bot_text["all_coin"], resize=1),
                        Button.text(bot_text["one_coin"])
                    ],
                    [
                        Button.text(bot_text["down_all_coin"])
                    ],
                    [
                        Button.text(bot_text["back"])
                    ]
                ]
                await event.reply(bot_text["select"], buttons=keys)
        elif text == bot_text["all_coin"]:
            is_admin = check_admin(user_id)
            if is_admin is False:
                keys = get_public_keys(user_id)
                await event.reply(bot_text["select"], buttons=keys)
            else:
                async with bot.conversation(user_id) as conv:
                    ask_coin = await conv.send_message(bot_text["ask_all_coin"])
                    while True:
                        try:
                            amount = await conv.get_response(timeout=120)
                            if amount.raw_text == bot_text["cancel"] or amount.raw_text == bot_text["back"]:
                                await conv.send_message(bot_text["canceled"])
                                await bot.delete_messages(user_id, ask_coin.id)
                                return
                            amount = int(amount.raw_text)
                            break
                        except ValueError:
                            await conv.send_message(bot_text["just_num"])
                        except TimeoutError:
                            await conv.send_message(bot_text["timeout_error"])
                            await bot.delete_messages(user_id, ask_coin.id)
                            return
                    loading_coins = await event.reply(bot_text["adding_coin_to_users"])
                    users = cur.execute("SELECT id,score FROM users").fetchall()
                    for user in users:
                        score = int(user[1]) + amount
                        user_num_id = user[0]
                        cur.execute(f"UPDATE users SET score = {score} WHERE id = {user_num_id}")
                        con.commit()
                        try:
                            await bot.send_message(user_num_id, bot_text["coin_from_admin"].format(coin=amount))
                        except UserIsBlockedError:
                            pass
                    await bot.delete_messages(user_id, loading_coins.id)
                    await event.reply(bot_text["coins_added"])
        elif text == bot_text["down_all_coin"]:
            is_admin = check_admin(user_id)
            if is_admin is False:
                keys = get_public_keys(user_id)
                await event.reply(bot_text["select"], buttons=keys)
            else:
                async with bot.conversation(user_id) as conv:
                    ask_coin = await conv.send_message(bot_text["ask_all_coin"])
                    while True:
                        try:
                            amount = await conv.get_response(timeout=120)
                            if amount.raw_text == bot_text["cancel"] or amount.raw_text == bot_text["back"]:
                                await conv.send_message(bot_text["canceled"])
                                await bot.delete_messages(user_id, ask_coin.id)
                                return
                            amount = int(amount.raw_text)
                            break
                        except ValueError:
                            await conv.send_message(bot_text["just_num"])
                        except TimeoutError:
                            await conv.send_message(bot_text["timeout_error"])
                            await bot.delete_messages(user_id, ask_coin.id)
                            return
                    loading_coins = await event.reply(bot_text["adding_coin_to_users"])
                    users = cur.execute("SELECT id,score FROM users").fetchall()
                    for user in users:
                        score = int(user[1]) - amount
                        if score < 0:
                            score = 0
                        user_num_id = user[0]
                        cur.execute(f"UPDATE users SET score = {score} WHERE id = {user_num_id}")
                        con.commit()
                    await bot.delete_messages(user_id, loading_coins.id)
                    await event.reply(bot_text["coins_added"])
        elif text == bot_text["one_coin"]:
            is_admin = check_admin(user_id)
            if is_admin is False:
                keys = get_public_keys(user_id)
                await event.reply(bot_text["select"], buttons=keys)
            else:
                async with bot.conversation(user_id) as conv:
                    action_keys = [
                        [
                            Button.inline(bot_text["low_off"], data=b'low_off')
                        ],
                        [
                            Button.inline(bot_text["add_coin"], data=b'add_coin')
                        ]
                    ]
                    ask_action = await conv.send_message(bot_text["select"], buttons=action_keys)
                    try:
                        action = await conv.wait_event(events.CallbackQuery(), timeout=120)
                        action = action.data
                    except TimeoutError:
                        await conv.send_message(bot_text["timeout_error"])
                        await bot.delete_messages(user_id, ask_action.id)
                        return
                    ask_user_id = await conv.send_message(bot_text["enter_user_id"])
                    while True:
                        try:
                            user_id_get = await conv.get_response(timeout=120)
                            if user_id_get.raw_text == bot_text["cancel"] or user_id_get.raw_text == bot_text["back"]:
                                await conv.send_message(bot_text["canceled"])
                                await bot.delete_messages(user_id, ask_user_id.id)
                                return
                            user_id_get = int(user_id_get.raw_text)
                            break
                        except ValueError:
                            await conv.send_message(bot_text["just_num"])
                        except TimeoutError:
                            await conv.send_message(bot_text["timeout_error"])
                            await bot.delete_messages(user_id, ask_user_id.id)
                            return
                    find_user = cur.execute(f"SELECT score FROM users WHERE id = {user_id_get}").fetchone()
                    if find_user is None:
                        await event.reply(bot_text["not_found"])
                        return
                    else:
                        ask_amount = await conv.send_message(bot_text["enter_coin_amount"])
                        while True:
                            try:
                                amount = await conv.get_response(timeout=120)
                                if amount.raw_text == bot_text["cancel"] or amount.raw_text == bot_text["back"]:
                                    await conv.send_message(bot_text["canceled"])
                                    await bot.delete_messages(user_id, ask_amount.id)
                                    return
                                amount = int(amount.raw_text)
                                break
                            except ValueError:
                                await conv.send_message(bot_text["just_num"])
                            except TimeoutError:
                                await conv.send_message(bot_text["timeout_error"])
                                await bot.delete_messages(user_id, ask_amount.id)
                                return
                        loading_coin = await conv.send_message(bot_text["loading_coin"])
                        if action == b"add_coin":
                            user_score = find_user[0] + amount
                            cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id_get}")
                            con.commit()
                        elif action == b"low_off":
                            user_score = find_user[0] - amount
                            cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id_get}")
                            con.commit()
                        else:
                            await conv.send_message(bot_text["action_not_found"])
                            return
                        await bot.delete_messages(user_id, loading_coin.id)
                        await conv.send_message(bot_text["coin_added"])
                        if action == b"add_coin":
                            await bot.send_message(user_id_get, bot_text["coin_added_notification"].format(coin=amount))
                            await conv.cancel_all()
                        else:
                            await bot.send_message(user_id_get, bot_text["coin_low_off"].format(coin=amount))
                            await conv.cancel_all()                            
        elif text == bot_text["users"]:
            is_admin = check_admin(user_id)
            if is_admin is False:
                keys = get_public_keys(user_id)
                await event.reply(bot_text["select"], buttons=keys)
            else:
                us_keys = [
                    [
                        Button.text(bot_text["robot_statistics"]),
                    ],
                    [
                        Button.text(bot_text["users_excel"]),
                        Button.text(bot_text["new_users"])
                    ],
                    [
                        Button.text(bot_text["users_coin_gt"]),
                        Button.text(bot_text["users_sub_count"]),
                    ],
                    [
                        Button.text(bot_text['back'], resize=True)
                    ],
                ]
                await event.reply(bot_text["select"], buttons=us_keys)
        elif text == bot_text["users_level"]:
            is_admin = check_admin(user_id)
            if is_admin is False:
                keys = get_public_keys(user_id)
                await event.reply(bot_text["select"], buttons=keys)
            else:
                async with bot.conversation(user_id) as conv:
                    ask_user_id = await conv.send_message(bot_text["enter_user_id"])
                    while True:
                        try:
                            user_id_get = await conv.get_response(timeout=120)
                            if user_id_get.raw_text == bot_text["cancel"] or user_id_get.raw_text == bot_text["back"]:
                                await conv.send_message(bot_text["canceled"])
                                await bot.delete_messages(user_id, ask_user_id.id)
                                return
                            user_id_get = int(user_id_get.raw_text)
                            break
                        except ValueError:
                            await conv.send_message(bot_text["just_num"])
                        except TimeoutError:
                            await conv.send_message(bot_text["timeout_error"])
                            await bot.delete_messages(user_id, ask_user_id.id)
                            return
                    find_user = cur.execute(f"SELECT * FROM users WHERE id = {user_id_get}").fetchone()
                    if find_user is None:
                        await event.reply(bot_text["not_found"])
                        return
                    else:
                        keys = [
                            [
                                Button.inline(bot_text["level_one"], b'1')
                            ],
                            [
                                Button.inline(bot_text["level_two"], b'2')
                            ],
                            [
                                Button.inline(bot_text["level_three"], b'3')
                            ]
                        ]
                        ask_level = await conv.send_message(bot_text["select"], buttons=keys)
                        try:
                            level = await conv.wait_event(events.CallbackQuery())
                            level = level.data
                        except TimeoutError:
                            await conv.send_message(bot_text["timeout_error"])
                            await bot.delete_messages(user_id, ask_level.id)
                            return
                        if level == b'1':
                            level = 1
                        elif level == b'2':
                            level = 2
                        elif level == b'3':
                            level = 3
                        else:
                            await conv.send_message(bot_text["action_not_found"])
                            return
                        cur.execute(f"UPDATE users SET level = {level} WHERE id = {user_id_get}")
                        con.commit()
                        await conv.send_message(bot_text["level_updated"])
                        await conv.cancel_all()
        elif text == bot_text["users_coin_gt"]:
            users = cur.execute(f"SELECT * FROM users ORDER BY score DESC LIMIT 10").fetchall()
            if lang == 1:
                text = "Top users by score:\n"
            else:
                text = "برترین کاربران بر اساس امتیاز:\n"
            for user in users:
                get_user = await bot.get_entity(user[0])
                user_id_ = get_user.id
                last_name = get_user.last_name
                full_name = get_user.first_name + last_name if last_name is not None else get_user.first_name 
                username = get_user.username if get_user.username is not None else "❌"
                if lang == 1:
                    text += f"User id: `{user[0]}`\nUserScore: **{user[5]}**\nUsername: {username}\nFullName: {full_name}" + "\n➖➖➖➖➖➖➖➖\n"
                else:
                    text += f"آیدی عددی: `{user[0]}`\nامتیاز: **{user[5]}**\nنام کاربری: {username}\nنام کامل: {full_name}" + "\n➖➖➖➖➖➖➖➖\n"
            await event.reply(text)
        elif text == bot_text["users_sub_count"]:
            users = cur.execute(f"SELECT * FROM users ORDER BY sub_count DESC LIMIT 10").fetchall()
            if lang == 1:
                text = "Top users by sub-count:\n"
            else:
                text = "برترین کاربران بر اساس زیر مجموعه:\n"
            for user in users:
                if lang == 1:
                    text += f"User id: `{user[0]}`\nUserSubCount: **{user[4]}**" + "\n➖➖➖➖➖➖➖➖\n"
                else:
                    text += f"آیدی عددی: `{user[0]}`\n زیر مجموعه: **{user[4]}**" + "\n➖➖➖➖➖➖➖➖\n"
            await event.reply(text)
        elif text == bot_text["users_excel"]:
            users = cur.execute("SELECT * FROM users").fetchall()
            # Create a new Excel workbook
            workbook = openpyxl.Workbook()
            # Select the default sheet (usually named 'Sheet')
            sheet = workbook.active
            # Add data to the Excel sheet
            data = [
                ["Name", "ID"],
            ]
            for user in users:
                user_id_ = user[0]
                get_user = await bot.get_entity(user_id_)
                full_name = get_user.first_name + get_user.last_name if get_user.last_name is not None else get_user.first_name
                user_data = [full_name, user_id_]
                data.append(user_data)
            for row in data:
                sheet.append(row)
            # Save the workbook to a file
            name = str(randint(0, 2747)) + ".xlsx"
            workbook.save(name)
            workbook.close()
            # Print a success message
            await bot.send_file(user_id, name, caption=bot_text["users_excel_caption"])
        elif text == bot_text["new_users"]:
            is_admin = check_admin(user_id)
            if is_admin is False:
                keys = get_public_keys(user_id)
                await event.reply(bot_text["select"], buttons=keys)
            else:
                text = ""
                users = cur.execute("SELECT * FROM users ORDER BY join_time DESC LIMIT 10;").fetchall()
                for user in users:
                    get_user = await bot.get_entity(user[0])
                    user_id_ = get_user.id
                    last_name = get_user.last_name
                    full_name = get_user.first_name + last_name if last_name is not None else get_user.first_name 
                    username = get_user.username if get_user.username is not None else "❌"
                    a_tag = f'<a href="tg://user?id={user_id_}">{full_name}</a>'
                    if lang == 1:
                        text += f"Number Id: {user_id_}\nUserName: {username}\nFullName: {a_tag} \n➖➖➖➖➖➖\n"
                    else:
                        text += f"آیدی عددی: {user_id_}\nنام کاربری: {username}\nنام: {a_tag}\n➖➖➖➖➖➖\n"
                await event.reply(text, parse_mode="html")
        elif text == bot_text["robot_statistics"]:
            is_admin = check_admin(user_id)
            if is_admin is False:
                keys = get_public_keys(user_id)
                await event.reply(bot_text["select"], buttons=keys)
            else:
                # users = 111
                users = len(cur.execute("SELECT * FROM users").fetchall())
                await event.reply(bot_text["statistics_text"].format(users=users))
        # elif text == bot_text["fia_info_management"]:
        #     ch_admin = check_admin(user_id=user_id)
        #     if ch_admin:
        #         await bot.send_file(user_id, )
        elif text == bot_text["words"]:
            is_admin = check_admin(user_id)
            if is_admin is False:
                keys = get_public_keys(user_id)
                await event.reply(bot_text["select"], buttons=keys)
            else:
                keys = [
                    [
                        Button.text(bot_text["add_word"]),
                        Button.text(bot_text["show_words"], resize=True),
                    ],
                    [Button.text(bot_text['back'])],
                ]
                await event.reply(bot_text["select"], buttons=keys)
        elif text == bot_text["scores"]:
            join_ch, entity = await config.join_check_plus(user_id, bot)
            if join_ch is False:
                full_info = await bot(GetFullChannelRequest(entity))
                chat_title = full_info.chats[0].title
                channel_username = full_info.chats[0].username
                if channel_username is None:
                    channel_username = full_info.full_chat.exported_invite.link
                else:
                    channel_username = f'https://t.me/{channel_username}'
                key = [
                    [Button.url(text=chat_title, url=channel_username)],
                ]
                await event.reply(bot_text["pls_join"], buttons=key)
            else:
                keys = [
                    [
                        Button.text(bot_text["add_score"], resize=True),
                        Button.text(bot_text["show_table"]),
                    ],
                    [
                        Button.text(bot_text["back"], resize=True)
                    ],
                ]
                await event.reply(bot_text["select"], buttons=keys)
        elif text == bot_text["down_all_coin"]:
            async with bot.conversation(user_id, timeout=1000) as conv:
                await conv.send_message(bot_text["enter_down_all_coin"])
                while True:
                    try:
                        amount = await conv.get_response()
                        amount = amount.raw_text
                        if amount == bot_text["cancel"] or amount == bot_text["back"]:
                            await conv.send_message(bot_text["canceled"])
                            return
                        amount = int(amount)
                        break
                    except ValueError:
                        await conv.send_message(bot_text["just_num"])
            users = cur.execute("SELECT * FROM users").fetchall()
            for user in users:
                user_coin = int(user[5])
                if user_coin - amount < 0:
                    user_coin = 0
                else:
                    user_coin = user_coin - amount
                cur.execute(f"UPDATE users SET score = {user_coin} WHERE id = {user[0]}")
                con.commit()
            await event.reply(bot_text["all_down_su"])
        elif text == bot_text["add_score"]:
            find_grands = cur.execute("SELECT * FROM grand ORDER BY num ASC").fetchall()
            if len(find_grands) == 0:
                await event.reply(bot_text["grands_not_found"], buttons=back)
                return
            inline_keys = []
            for grand in find_grands:
                grand_name = grand[1]
                grand_num = grand[0]
                print(grand_num)
                key = [Button.inline(grand_name, str.encode("get_drivers" + ":" + str(grand_num)))]
                inline_keys.append(key)
            await event.reply(bot_text["select_grand"], buttons=inline_keys)
        elif text == bot_text["show_table"]:
            grands = cur.execute("SELECT * FROM grand ORDER BY num").fetchall()
            if len(grands) == 0:
                await event.reply(bot_text["grands_not_found"])
            else:
                keys = []
                for grand in grands:
                    grand_num = grand[0]
                    grand_text = grand[1]
                    key = [Button.inline(grand_text, str.encode("see_score" + ":" + str(grand_num)))]
                    keys.append(key)
                await event.reply(bot_text["select_see_grand"], buttons=keys)
        elif text == bot_text["grand"]:
            keys = [
                [
                    Button.text(bot_text["add_grand"]),
                    Button.text(bot_text["show_grand"], resize=True)
                ],
                [back]
            ]
            await event.reply(bot_text["select"], buttons=keys)
        elif text == bot_text["add_word"]:
            is_admin = check_admin(user_id)
            if is_admin is False:
                keys = get_public_keys(user_id)
                await event.reply(bot_text["select"], buttons=keys)
            else:
                async with bot.conversation(user_id, timeout=1000) as conv:
                    await conv.send_message(bot_text["enter_word"])
                    word = await conv.get_response()
                    if word.raw_text == bot_text["cancel"] or word.raw_text == bot_text["back"]:
                        await conv.send_message(bot_text["canceled"])
                        await conv.cancel_all()
                    else:
                        words = str(word.raw_text).split("\n")
                        if len(words) != 1:
                            for w in words:
                                tag_word = w.split("_")
                                data = [
                                    (tag_word[0], tag_word[1])
                                ]
                                cur.executemany(f"INSERT INTO btn VALUES (?,?)", data)
                                con.commit()
                            await conv.send_message(bot_text["saved"])
                            await conv.cancel_all()
                        else:
                            tag_word = word.raw_text.split("_")
                            data_m = [
                                (tag_word[0], tag_word[1])
                            ]
                            cur.executemany(f"INSERT INTO btn VALUES (?,?)", data_m)
                            con.commit()
                            await conv.send_message(bot_text["saved"])
                            await conv.cancel_all()
        elif text == bot_text["upgrade_level"]:
            keys = [
                [
                    Button.text(bot_text["now_plan"], resize=True),
                    Button.text(bot_text["up_plan"], resize=True),
                ],
                [
                    back
                ]
            ]
            await event.reply(bot_text["select"], buttons=keys)
        elif text == bot_text["up_plan"]:
            await event.reply(bot_text["soon"])
        elif text == bot_text["now_plan"]:
            find_user_level = cur.execute(f"SELECT level FROM users WHERE id={user_id}").fetchone()
            level_dict = {
                "1": bot_text["level_one"],
                "2": bot_text["level_two"],
                "3": bot_text["level_three"],
            }
            user_level_fa = level_dict[f"{find_user_level[0]}"]
            try:
                next_level = level_dict[str(int(find_user_level[0]) + 1)]
            except KeyError:
                next_level = level_dict["3"]
            text = bot_text["now_plan_text"].format(level=user_level_fa, next_level=next_level)
            datas_text = ""
            for k, v in data_scores.items():
                datas_text += f"{k}: {v[f'{find_user_level[0]}']}" + "\n"
            text += "\n\n" + datas_text
            await event.reply(text)
        elif text == bot_text["fia"]:
            keys = [
                [
                    Button.text(bot_text["fia_tec"], resize=True),
                    Button.text(bot_text["fia_race_data"])
                ],
                [
                    Button.text(bot_text["back"])
                ]
            ]
            await event.reply(bot_text["select"], buttons=keys)
        elif text == bot_text["fia_tec"]:
            folder_path = Path("fia_tech")
            files = ["fia_tech/" + f.name for f in folder_path.iterdir() if f.is_file()]
            await event.reply(bot_text["fia_tec"], file=files)
        elif text == bot_text["fia_race_data"]:
            year = 2024
            async with bot.conversation(user_id, timeout=1000) as conv:
                response = manager.get_event(year=year)["Country"]
                gp_keys = []
                for gp in response:
                    if lang == 1:
                        gp_text = gp["t"]
                    else:
                        gp_text = country_tr[gp["tr"]]
                    gp_data = gp["t"].encode()
                    key = Button.inline(gp_text, data=gp_data)
                    gp_keys.append(key)
                result = []
                for i in range(0, len(gp_keys), 2):
                    if i + 1 < len(gp_keys):
                        result.append([gp_keys[i], gp_keys[i + 1]])
                    else:
                        result.append([gp_keys[i]])
                result.append([Button.inline(bot_text["cancel"], b'cancel')])
                ask_gp = await conv.send_message(bot_text["select_gp"], buttons=result)
                try:
                    gp_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                    await bot.delete_messages(user_id, ask_gp.id)
                except TimeoutError:
                    await conv.send_message(bot_text["timeout_error"])
                    await bot.delete_messages(user_id, ask_gp.id)
                    return
                gp_data = gp_res.data
                if gp_data == b'cancel':
                    await conv.send_message(bot_text["canceled"])
                    await conv.cancel_all()
                else:
                    gp = gp_data.decode()
                    gp = gp.replace(" ", "_")
                    print(gp)
                    await event.reply(bot_text["loading_fia"])
                    url = f"http://127.0.0.1:8000/get-pdf/?grand_name={gp}"
                    response = requests.get(url)
                    rjson = response.json()
                    status = rjson["status"]
                    if status == 500:
                        await event.reply(bot_text["cant_get_fia"])
                    else:
                        response = rjson["pdfs_path"]
                        new_pdfs = []
                        for r in response:
                            new_pdfs.append("/root/pdf_test/" + r)
                        await bot.send_file(user_id, file=new_pdfs)
        elif text == bot_text["time_setup"]:
            keys = [
                [
                    Button.text(bot_text["london_time"]),
                    Button.text(bot_text["iran_time"]),
                ],
                [
                    Button.text(bot_text["back"], resize=1)
                ]
            ]
            await event.reply(bot_text["select_time"], buttons=keys)
        elif text == bot_text["iran_time"]:
            user_id = event.sender_id
            update_user_time = cur.execute(f"UPDATE users SET time_zone = 'iran' WHERE id = {user_id}")
            con.commit()
            await event.reply(bot_text["iran_time_set"])
        elif text == bot_text["london_time"]:
            user_id = event.sender_id
            update_user_time = cur.execute(f"UPDATE users SET time_zone = 'london' WHERE id = {user_id}")
            con.commit()
            await event.reply(bot_text["london_time_set"])
        elif text == bot_text["page_one"]:
            keys = [
                [
                    Button.text(bot_text["rpm"]),
                ],
                [
                    Button.text(bot_text["top_speed"]),
                    Button.text(bot_text["map_viz"]),
                ],
                [
                    Button.text(bot_text["lap_times_table"]),
                    Button.text(bot_text["overtake"]),
                    Button.text(bot_text["map_break"]),
                ],
                [
                    Button.text(bot_text["back"], resize=1)
                ]
            ]
            await event.reply(bot_text["select"], buttons=keys)
        elif text == bot_text["page_two"]:
            keys = [
                [
                    Button.text(bot_text["g_force"]),
                ],
                [
                    Button.text(bot_text["down_force"]),
                    Button.text(bot_text["lap_times"]),
                ],
                [
                    Button.text(bot_text["all"]),
                    Button.text(bot_text["brake_configurations"]),
                    Button.text(bot_text["composite_perfomance"])
                ],
                [
                    Button.text(bot_text["back"], resize=1)
                ]
            ]
            await event.reply(bot_text["select"], buttons=keys)
        elif text == bot_text["page_three"]:
            keys = [
                [
                    Button.text(bot_text["strategy"]),
                ],
                [
                    Button.text(bot_text["start_reaction"]),
                    Button.text(bot_text["data_to_pole"]),
                ],
                [
                    Button.text(bot_text["degradation_tyre"]),
                    Button.text(bot_text["weather_data"]),
                    Button.text(bot_text["tyre_performance"])
                ],
                [
                    Button.text(bot_text["back"], resize=1)
                ]
            ]
            await event.reply(bot_text["select"], buttons=keys)
        elif text == bot_text["forth_page"]:
            keys = [
                [
                    Button.text(bot_text["ers_analysis"])
                ],
                [
                    Button.text(bot_text["comparison_fastest_lap"], resize=1),
                    Button.text(bot_text["efficiency_breakdown"])
                ],
                [
                    Button.text(bot_text["stress_index"]),
                    Button.text(bot_text["fia"])
                ],
                [
                    Button.text(bot_text["back"])
                ]
            ]
            await event.reply(bot_text["select"], buttons=keys)
        # All bot datas
        elif text == bot_text["overtake"]:
            find_status = cur.execute(f"SELECT status FROM data_status WHERE data = '{event.message.message}'").fetchone()
            if find_status[0] == 'off' or find_status[0] is None:
                await event.reply(bot_text["data_is_off"])
                return
            user_find = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
            user_scores = user_find[5]
            user_level = user_find[10]
            score_dict = {
                "1": 1,
                "2": 0,
                "3": 0,
            }
            score_get = score_dict[f"{user_level}"]
            if user_scores - score_get < 0:
                key = [
                    Button.inline(bot_text["account"], data=b'user_account')
                ]
                await event.reply(bot_text["coin_not_enough"].format(score=user_scores), buttons=key)
                return
            async with bot.conversation(user_id) as conv:
                year_keys = [
                    [
                        Button.inline("2024", b'2024')
                    ],
                    [
                        Button.inline("2023", b'2023')
                    ],
                    [
                        Button.inline("2022", b'2022')
                    ],
                    [
                        Button.inline("2021", b'2021')
                    ],
                    [
                        Button.inline("2020", b'2020')
                    ],
                    [
                        Button.inline("2019", b'2019')
                    ],
                    [
                        Button.inline("2018", b'2018')
                    ],
                    [
                        Button.inline(bot_text["cancel"], b'cancel')
                    ]
                ]
                ask_year = await conv.send_message(bot_text["select_year"], buttons=year_keys)
                try:
                    year_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                    await bot.delete_messages(user_id, ask_year.id)
                except TimeoutError:
                    await conv.send_message(bot_text["timeout_error"])
                    await bot.delete_messages(user_id, ask_year.id)
                    return
                year_data = year_res.data
                if year_data == b'cancel':
                    await conv.send_message(bot_text["canceled"])
                    await bot.delete_messages(user_id, ask_year.id)
                    await conv.cancel_all()
                else: 
                    year = int(year_data)
                    response = manager.get_event(year=year)["Country"]
                    gp_keys = []
                    for gp in response:
                        if lang == 1:
                            gp_text = gp["t"]
                        else:
                            gp_text = country_tr[gp["tr"]]
                        gp_data = gp["t"].encode()
                        key = Button.inline(gp_text, data=gp_data)
                        gp_keys.append(key)
                    result = []
                    for i in range(0, len(gp_keys), 2):
                        if i + 1 < len(gp_keys):
                            result.append([gp_keys[i], gp_keys[i + 1]])
                        else:
                            result.append([gp_keys[i]])
                    result.append([Button.inline(bot_text["cancel"], b'cancel')])
                    ask_gp = await conv.send_message(bot_text["select_gp"], buttons=result)
                    try:
                        gp_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                        await bot.delete_messages(user_id, ask_gp.id)
                    except TimeoutError:
                        await conv.send_message(bot_text["timeout_error"])
                        await bot.delete_messages(user_id, ask_gp.id)
                        return
                    gp_data = gp_res.data
                    if gp_data == b'cancel':
                        await conv.send_message(bot_text["canceled"])
                        await conv.cancel_all()
                    else:
                        gp = gp_data.decode()
                        sessions = manager.get_session(year=year, country=gp)["sessions"]
                        type_tr = {
                            "Sprint": "اسپرینت",
                            "Race": "مسابقه"
                        }
                        sessions_keys = []
                        for session in sessions:
                            if session != "Race" and session != "Sprint":
                                continue
                            else:
                                if lang == 1:
                                    session_text = session
                                else:
                                    session_text = type_tr[session]
                                session_key = [
                                    Button.inline(session_text, session.encode()),
                                ]
                                sessions_keys.append(session_key)
                        ask_event = await event.reply(bot_text["select_session"], buttons=sessions_keys)
                        try:
                            session_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                            await bot.delete_messages(user_id, ask_event.id)
                        except TimeoutError:
                            await conv.send_message(bot_text["timeout_error"])
                            await bot.delete_messages(user_id, ask_event.id)
                            return
                        event_data = session_res.data
                        if event_data == b'cancel':
                            await conv.send_message(bot_text["canceled"])
                            await conv.cancel_all()
                        else:
                            session = event_data.decode()
                            if year == 2024:
                                # ساعت مسابقه به عنوان یک رشته

                                # دریافت تاریخ مسابقه از API
                                check_date = f"https://ergast.com/api/f1/{year}.json"
                                check_date = requests.get(check_date).json()["MRData"]["RaceTable"]["Races"]

                                for grand in check_date:
                                    if grand["raceName"] == gp:
                                        now = datetime.now()
                                        now_date_str = f"{now.year}-{now.month:02d}-{now.day:02d}"
                                        now_time_str = now.strftime("%H:%M:%S")
                                        
                                        # ترکیب تاریخ و ساعت فعلی
                                        now_datetime_str = f"{now_date_str} {now_time_str}"
                                        now_datetime = datetime.strptime(now_datetime_str, "%Y-%m-%d %H:%M:%S")
                                        
                                        if session == "Race":
                                            race_date = grand["date"]
                                        elif session == "Sprint":
                                            race_date = grand["Sprint"]["date"]
                                        else:
                                            await conv.send_message(bot_text["action_not_found"])
                                            return
                                        if check_date_passed(race_date) is False:
                                            race_hour = cur.execute(f"SELECT time FROM grand_time WHERE grand = '{gp}' AND session_type = '{session}';").fetchone()
                                            if race_hour is None:
                                                await conv.send_message(bot_text["problem"])
                                                return
                                            race_hour = race_hour[0]
                                            # ترکیب تاریخ و ساعت مسابقه
                                            race_datetime_str = f"{race_date} {race_hour}"
                                            race_datetime = datetime.strptime(race_datetime_str, "%Y-%m-%d %H:%M:%S")
                                            
                                            if now_datetime < race_datetime:
                                                await conv.send_message(bot_text["dont_time"])
                                                return
                            if lang == 1:
                                loading = await conv.send_message(bot_text["loading"].format(year=year, gp=gp, event=session))
                            else:
                                loading = await conv.send_message(bot_text["loading"].format(year=year, gp=country_tr[gp.replace(" ", "_")], event=type_tr[session]))
                            BASE_DIR = Path(__file__).resolve().parent
                            image_over = f"{year}-{gp}-{session}-overtake.png"
                            image_base_over = fr"{BASE_DIR}/{image_over}"
                            if os.path.exists(image_base_over) is False:
                                try:
                                    overtakepath = overtake(year, gp, session)
                                except:
                                    pass
                            await bot.delete_messages(user_id, loading.id)

                            await bot.send_file(user_id, caption="overtake", file=image_base_over)
                            await bot.send_file(user_id, caption="overtake", file=image_base_over, force_document=True)
                            config.all_statistics(event.message.message, user_id)
                            config.small_statistics(event.message.message, user_id)
                            user_find = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
                            user_level = user_find[10]
                            level_dict = {
                                "1": bot_text["level_one"],
                                "2": bot_text["level_two"],
                                "3": bot_text["level_three"],
                            }
                            user_level_fa = level_dict[f"{user_level}"]
                            if user_level == "1":
                                user_score = user_find[5]
                                user_score -= 1
                                cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                con.commit()
                                await event.reply(bot_text["score_data"].format(coin=1, level=user_level_fa))
                            await conv.cancel_all()
        elif text == bot_text["top_speed"]:
            find_status = cur.execute(f"SELECT status FROM data_status WHERE data = '{event.message.message}'").fetchone()
            if find_status[0] == 'off' or find_status[0] is None:
                await event.reply(bot_text["data_is_off"])
                return
            user_find = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
            user_scores = user_find[5]
            user_level = user_find[10]
            score_dict = {
                "1": 2,
                "2": 1,
                "3": 0,
            }
            score_get = score_dict[f"{user_level}"]
            if user_scores - score_get < 0:
                key = [
                    Button.inline(bot_text["account"], data=b'user_account')
                ]
                await event.reply(bot_text["coin_not_enough"].format(score=user_scores), buttons=key)
                return
            async with bot.conversation(user_id) as conv:
                year_keys = [
                    [
                        Button.inline("2024", b'2024')
                    ],
                    [
                        Button.inline("2023", b'2023')
                    ],
                    [
                        Button.inline("2022", b'2022')
                    ],
                    [
                        Button.inline("2021", b'2021')
                    ],
                    [
                        Button.inline("2020", b'2020')
                    ],
                    [
                        Button.inline("2019", b'2019')
                    ],
                    [
                        Button.inline("2018", b'2018')
                    ],
                    [
                        Button.inline(bot_text["cancel"], b'cancel')
                    ]
                ]
                ask_year = await conv.send_message(bot_text["select_year"], buttons=year_keys)
                try:
                    year_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                    await bot.delete_messages(user_id, ask_year.id)
                except TimeoutError:
                    await conv.send_message(bot_text["timeout_error"])
                    await bot.delete_messages(user_id, ask_year.id)
                    return
                year_data = year_res.data
                if year_data == b'cancel':
                    await conv.send_message(bot_text["canceled"])
                    await bot.delete_messages(user_id, ask_year.id)
                    await conv.cancel_all()
                else: 
                    year = int(year_data)
                    response = manager.get_event(year=year)["Country"]
                    gp_keys = []
                    for gp in response:
                        if lang == 1:
                            gp_text = gp["t"]
                        else:
                            gp_text = country_tr[gp["tr"]]

                        gp_data = gp["t"].encode()
                        key = Button.inline(gp_text, data=gp_data)
                        gp_keys.append(key)
                    result = []
                    for i in range(0, len(gp_keys), 2):
                        if i + 1 < len(gp_keys):
                            result.append([gp_keys[i], gp_keys[i + 1]])
                        else:
                            result.append([gp_keys[i]])
                    result.append([Button.inline(bot_text["cancel"], b'cancel')])
                    ask_gp = await conv.send_message(bot_text["select_gp"], buttons=result)
                    try:
                        gp_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                        await bot.delete_messages(user_id, ask_gp.id)
                    except TimeoutError:
                        await conv.send_message(bot_text["timeout_error"])
                        await bot.delete_messages(user_id, ask_gp.id)
                        return
                    gp_data = gp_res.data
                    if gp_data == b'cancel':
                        await conv.send_message(bot_text["canceled"])
                        await conv.cancel_all()
                    else:
                        gp = gp_data.decode()        
                        # url = f"https://f1datas.com/api/v1/fastf1/session?year={year}&country={gp}"
                        sessions = manager.get_session(year=year, country=gp)["sessions"]
                        # sessions = requests.get(url).json()["sessions"]
                        type_tr = {
                            "Practice_1": "تمرین اول",
                            "Practice_2": "تمرین دوم",
                            "Practice_3": "تمرین سوم",
                            "Sprint": "اسپرینت",
                            "Sprint_Shootout": "اسپرینت شوت آوت",
                            "Sprint_Qualifying": "تعیین خط اسپرینت",
                            "Qualifying": "تعیین خط",
                            "Race": "مسابقه"
                        }
                        sessions_keys = []
                        for session in sessions:
                            if lang == 1:
                                session_text = session
                            else:
                                session_text = type_tr[session]
                            session_key = [
                                Button.inline(session_text, session.encode()),
                            ]
                            sessions_keys.append(session_key)
                        ask_event = await event.reply(bot_text["select_session"], buttons=sessions_keys)
                        try:
                            session_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                            await bot.delete_messages(user_id, ask_event.id)
                        except TimeoutError:
                            await conv.send_message(bot_text["timeout_error"])
                            await bot.delete_messages(user_id, ask_event.id)
                            return
                        event_data = session_res.data
                        if event_data == b'cancel':
                            await conv.send_message(bot_text["canceled"])
                            await conv.cancel_all()
                        else:
                            session = event_data.decode()
                            if year == 2024:
                                # دریافت تاریخ مسابقه از API
                                check_date = f"https://ergast.com/api/f1/{year}.json"
                                check_date = requests.get(check_date).json()["MRData"]["RaceTable"]["Races"]

                                for grand in check_date:
                                    if grand["raceName"] == gp:
                                        now = datetime.now()
                                        now_date_str = f"{now.year}-{now.month:02d}-{now.day:02d}"
                                        now_time_str = now.strftime("%H:%M:%S")
                                        
                                        # ترکیب تاریخ و ساعت فعلی
                                        now_datetime_str = f"{now_date_str} {now_time_str}"
                                        now_datetime = datetime.strptime(now_datetime_str, "%Y-%m-%d %H:%M:%S")
                                        
                                        if session == "Race":
                                            race_date = grand["date"]
                                        elif session == "Sprint":
                                            race_date = grand["Sprint"]["date"]
                                        elif session == "Practice_1":
                                            race_date = grand["FirstPractice"]["date"]
                                        elif session == "Practice_2":
                                            race_date = grand["SecondPractice"]["date"]
                                        elif session == "Practice_3":
                                            race_date = grand["ThirdPractice"]["date"]
                                        elif session == "Qualifying":
                                            race_date = grand["Qualifying"]["date"]
                                        else:
                                            await conv.send_message(bot_text["action_not_found"])
                                            return
                                        if check_date_passed(race_date) is False:
                                            race_hour = cur.execute(f"SELECT time FROM grand_time WHERE grand = '{gp}' AND session_type = '{session}';").fetchone()
                                            if race_hour is None:
                                                await conv.send_message(bot_text["problem"])
                                                return
                                            race_hour = race_hour[0]
                                            # ترکیب تاریخ و ساعت مسابقه
                                            race_datetime_str = f"{race_date} {race_hour}"
                                            race_datetime = datetime.strptime(race_datetime_str, "%Y-%m-%d %H:%M:%S")
                                            
                                            if now_datetime < race_datetime:
                                                await conv.send_message(bot_text["dont_time"])
                                                return
                            if lang == 1:
                                loading = await conv.send_message(bot_text["loading"].format(year=year, gp=gp, event=session))
                            else:
                                loading = await conv.send_message(bot_text["loading"].format(year=year, gp=country_tr[gp.replace(" ", "_")], event=type_tr[session.replace(" ", "_")]))
                            BASE_DIR = Path(__file__).resolve().parent
                            if session == "Practice_1" or session == "Practice_2" or session == "Practice_3":
                                session = sessions_convert[session]
                            image_top = f"{year}-{gp}-{session}-top_speed.png"
                            image_base_top = fr"{BASE_DIR}/{image_top}"
                            image_trap = f"{year}-{gp}-{session}-speed_trap.png"
                            image_base_trap = fr"{BASE_DIR}/{image_trap}"
                            if os.path.exists(image_base_top) is False and os.path.exists(image_base_trap) is False:
                                try:
                                    top_speed_path, speed_trap_path = top_speed(year, gp, session)
                                except:
                                    pass
                            await bot.delete_messages(user_id, loading.id)
                            await bot.send_file(user_id, caption="top speed", file=image_base_top)
                            await bot.send_file(user_id, caption="speed trap", file=image_base_trap)
                            await bot.send_file(user_id, caption="top speed", file=image_base_top, force_document=True)
                            await bot.send_file(user_id, caption="speed trap", file=image_base_trap, force_document=True)
                            config.all_statistics(event.message.message, user_id)
                            config.small_statistics(event.message.message, user_id)
                            user_find = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
                            user_level = user_find[10]
                            level_dict = {
                                "1": bot_text["level_one"],
                                "2": bot_text["level_two"],
                                "3": bot_text["level_three"],
                            }
                            user_level_fa = level_dict[f"{user_level}"]
                            if user_level == "1":
                                user_score = user_find[5]
                                user_score -= 2
                                cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                con.commit()
                                await event.reply(bot_text["score_data"].format(coin=2, level=user_level_fa))
                            elif user_level == "2":
                                user_score = user_find[5]
                                user_score -= 1
                                cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                con.commit()
                                await event.reply(bot_text["score_data"].format(coin=1, level=user_level_fa))
                            await conv.cancel_all()
        elif text == bot_text["lap_times"]:
            find_status = cur.execute(f"SELECT status FROM data_status WHERE data = '{event.message.message}'").fetchone()
            if find_status[0] == 'off' or find_status[0] is None:
                await event.reply(bot_text["data_is_off"])
                return
            user_find = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
            user_scores = user_find[5]
            user_level = user_find[10]
            score_dict = {
                "1": 2,
                "2": 1,
                "3": 1,
            }
            score_get = score_dict[f"{user_level}"]
            if user_scores - score_get < 0:
                key = [
                    Button.inline(bot_text["account"], data=b'user_account')
                ]
                await event.reply(bot_text["coin_not_enough"].format(score=user_scores), buttons=key)
                return
            async with bot.conversation(user_id) as conv:
                year_keys = [
                    [
                        Button.inline("2024", b'2024')
                    ],
                    [
                        Button.inline("2023", b'2023')
                    ],
                    [
                        Button.inline("2022", b'2022')
                    ],
                    [
                        Button.inline("2021", b'2021')
                    ],
                    [
                        Button.inline("2020", b'2020')
                    ],
                    [
                        Button.inline("2019", b'2019')
                    ],
                    [
                        Button.inline("2018", b'2018')
                    ],
                    [
                        Button.inline(bot_text["cancel"], b'cancel')
                    ]
                ]
                ask_year = await conv.send_message(bot_text["select_year"], buttons=year_keys)
                try:
                    year_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                    await bot.delete_messages(user_id, ask_year.id)
                except TimeoutError:
                    await conv.send_message(bot_text["timeout_error"])
                    await bot.delete_messages(user_id, ask_year.id)
                    return
                year_data = year_res.data
                if year_data == b'cancel':
                    await conv.send_message(bot_text["canceled"])
                    await bot.delete_messages(user_id, ask_year.id)
                    await conv.cancel_all()
                else: 
                    year = int(year_data)
                    response = manager.get_event(year=year)["Country"]
                    gp_keys = []
                    for gp in response:
                        if lang == 1:
                            gp_text = gp["t"]
                        else:
                            gp_text = country_tr[gp["tr"]]
                        gp_data = gp["t"].encode()
                        key = Button.inline(gp_text, data=gp_data)
                        gp_keys.append(key)
                    result = []
                    for i in range(0, len(gp_keys), 2):
                        if i + 1 < len(gp_keys):
                            result.append([gp_keys[i], gp_keys[i + 1]])
                        else:
                            result.append([gp_keys[i]])
                    result.append([Button.inline(bot_text["cancel"], b'cancel')])
                    ask_gp = await conv.send_message(bot_text["select_gp"], buttons=result)
                    try:
                        gp_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                        await bot.delete_messages(user_id, ask_gp.id)
                    except TimeoutError:
                        await conv.send_message(bot_text["timeout_error"])
                        await bot.delete_messages(user_id, ask_gp.id)
                        return
                    gp_data = gp_res.data
                    if gp_data == b'cancel':
                        await conv.send_message(bot_text["canceled"])
                        await conv.cancel_all()
                    else:
                        gp = gp_data.decode()        
                        # url = f"https://f1datas.com/api/v1/fastf1/session?year={year}&country={gp}"
                        sessions = manager.get_session(year=year, country=gp)["sessions"]
                        # sessions = requests.get(url).json()["sessions"]
                        type_tr = {
                            "Practice_1": "تمرین اول",
                            "Practice_2": "تمرین دوم",
                            "Practice_3": "تمرین سوم",
                            "Sprint": "اسپرینت",
                            "Sprint_Shootout": "اسپرینت شوت آوت",
                            "Sprint_Qualifying": "تعیین خط اسپرینت",
                            "Qualifying": "تعیین خط",
                            "Race": "مسابقه"
                        }
                        sessions_keys = []
                        for session in sessions:
                            if lang == 1:
                                session_text = session
                            else:
                                session_text = type_tr[session]
                            session_key = [
                                Button.inline(session_text, session.encode()),
                            ]
                            sessions_keys.append(session_key)
                        ask_event = await event.reply(bot_text["select_session"], buttons=sessions_keys)
                        try:
                            session_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                            await bot.delete_messages(user_id, ask_event.id)
                        except TimeoutError:
                            await conv.send_message(bot_text["timeout_error"])
                            await bot.delete_messages(user_id, ask_event.id)
                            return
                        event_data = session_res.data
                        if event_data == b'cancel':
                            await conv.send_message(bot_text["canceled"])
                            await conv.cancel_all()
                        else:
                            session = event_data.decode()
                            if year == 2024:
                                # دریافت تاریخ مسابقه از API
                                check_date = f"https://ergast.com/api/f1/{year}.json"
                                check_date = requests.get(check_date).json()["MRData"]["RaceTable"]["Races"]

                                for grand in check_date:
                                    if grand["raceName"] == gp:
                                        now = datetime.now()
                                        now_date_str = f"{now.year}-{now.month:02d}-{now.day:02d}"
                                        now_time_str = now.strftime("%H:%M:%S")
                                        
                                        # ترکیب تاریخ و ساعت فعلی
                                        now_datetime_str = f"{now_date_str} {now_time_str}"
                                        now_datetime = datetime.strptime(now_datetime_str, "%Y-%m-%d %H:%M:%S")
                                        
                                        if session == "Race":
                                            race_date = grand["date"]
                                        elif session == "Sprint":
                                            race_date = grand["Sprint"]["date"]
                                        elif session == "Practice_1":
                                            race_date = grand["FirstPractice"]["date"]
                                        elif session == "Practice_2":
                                            race_date = grand["SecondPractice"]["date"]
                                        elif session == "Practice_3":
                                            race_date = grand["ThirdPractice"]["date"]
                                        elif session == "Qualifying":
                                            race_date = grand["Qualifying"]["date"]
                                        else:
                                            await conv.send_message(bot_text["action_not_found"])
                                            return
                                        if check_date_passed(race_date) is False:
                                            race_hour = cur.execute(f"SELECT time FROM grand_time WHERE grand = '{gp}' AND session_type = '{session}';").fetchone()
                                            if race_hour is None:
                                                print("race hour", race_hour)
                                                print("session and grand", gp, session)
                                                print("check date", check_date_passed(race_date))
                                                await conv.send_message(bot_text["problem"])
                                                return
                                            race_hour = race_hour[0]
                                            # ترکیب تاریخ و ساعت مسابقه
                                            race_datetime_str = f"{race_date} {race_hour}"
                                            race_datetime = datetime.strptime(race_datetime_str, "%Y-%m-%d %H:%M:%S")
                                            
                                            if now_datetime < race_datetime:
                                                await conv.send_message(bot_text["dont_time"])
                                                return
                            if lang == 1:
                                loading = await conv.send_message(bot_text["loading"].format(year=year, gp=gp, event=session))
                            else:
                                loading = await conv.send_message(bot_text["loading"].format(year=year, gp=country_tr[gp.replace(" ", "_")], event=type_tr[session.replace(" ", "_")]))
                            BASE_DIR = Path(__file__).resolve().parent
                            if session == "Practice_1" or session == "Practice_2" or session == "Practice_3":
                                session = sessions_convert[session]
                            image_lap = f"{year}-{gp}-{session}-lap_times.png"
                            image_base_lap = fr"{BASE_DIR}/{image_lap}"
                            if os.path.exists(image_base_lap) is False:
                                lap_times_path = lap_times(year, gp, session)
                            await bot.delete_messages(user_id, loading.id)
                            await bot.send_file(user_id, caption="Lap Times", file=image_base_lap)
                            await bot.send_file(user_id, caption="Lap Times", file=image_base_lap, force_document=True)
                            config.all_statistics(event.message.message, user_id)
                            config.small_statistics(event.message.message, user_id)
                            user_find = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
                            user_level = user_find[10]
                            level_dict = {
                                "1": bot_text["level_one"],
                                "2": bot_text["level_two"],
                                "3": bot_text["level_three"],
                            }
                            user_level_fa = level_dict[f"{user_level}"]
                            if user_level == "1":
                                user_score = user_find[5]
                                user_score -= 2
                                cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                con.commit()
                                await event.reply(bot_text["score_data"].format(coin=2, level=user_level_fa))
                            elif user_level == "2":
                                user_score = user_find[5]
                                user_score -= 1
                                cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                con.commit()
                                await event.reply(bot_text["score_data"].format(coin=1, level=user_level_fa))
                            elif user_level == "3":
                                user_score = user_find[5]
                                user_score -= 1
                                cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                con.commit()
                                await event.reply(bot_text["score_data"].format(coin=1, level=user_level_fa))

                            await conv.cancel_all()
        elif text == bot_text["rpm"]:
            find_status = cur.execute(f"SELECT status FROM data_status WHERE data = '{event.message.message}'").fetchone()
            if find_status[0] == 'off' or find_status[0] is None:
                await event.reply(bot_text["data_is_off"])
                return
            user_find = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
            user_scores = user_find[5]
            user_level = user_find[10]
            score_dict = {
                "1": 3,
                "2": 2,
                "3": 1,
            }
            score_get = score_dict[f"{user_level}"]
            if user_scores - score_get < 0:
                key = [
                    Button.inline(bot_text["account"], data=b'user_account')
                ]
                await event.reply(bot_text["coin_not_enough"].format(score=user_scores), buttons=key)
                return
            async with bot.conversation(user_id) as conv:
                year_keys = [
                    [
                        Button.inline("2024", b'2024')
                    ],
                    [
                        Button.inline("2023", b'2023')
                    ],
                    [
                        Button.inline("2022", b'2022')
                    ],
                    [
                        Button.inline("2021", b'2021')
                    ],
                    [
                        Button.inline("2020", b'2020')
                    ],
                    [
                        Button.inline("2019", b'2019')
                    ],
                    [
                        Button.inline("2018", b'2018')
                    ],
                    [
                        Button.inline(bot_text["cancel"], b'cancel')
                    ]
                ]
                ask_year = await conv.send_message(bot_text["select_year"], buttons=year_keys)
                try:
                    year_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                    await bot.delete_messages(user_id, ask_year.id)
                except TimeoutError:
                    await conv.send_message(bot_text["timeout_error"])
                    await bot.delete_messages(user_id, ask_year.id)
                    return
                year_data = year_res.data
                if year_data == b'cancel':
                    await conv.send_message(bot_text["canceled"])
                    await bot.delete_messages(user_id, ask_year.id)
                    await conv.cancel_all()
                else: 
                    year = int(year_data)
                    response = manager.get_event(year=year)["Country"]
                    gp_keys = []
                    for gp in response:
                        if lang == 1:
                            gp_text = gp["t"]
                        else:
                            gp_text = country_tr[gp["tr"]]
                        gp_data = str.encode(gp["t"] + ":" + str(gp["round_num"]))
                        key = Button.inline(gp_text, data=gp_data)
                        gp_keys.append(key)
                    result = []
                    for i in range(0, len(gp_keys), 2):
                        if i + 1 < len(gp_keys):
                            result.append([gp_keys[i], gp_keys[i + 1]])
                        else:
                            result.append([gp_keys[i]])
                    result.append([Button.inline(bot_text["cancel"], b'cancel')])
                    ask_gp = await conv.send_message(bot_text["select_gp"], buttons=result)
                    try:
                        gp_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                        await bot.delete_messages(user_id, ask_gp.id)
                    except TimeoutError:
                        await conv.send_message(bot_text["timeout_error"])
                        await bot.delete_messages(user_id, ask_gp.id)
                        return
                    gp_data = gp_res.data
                    if gp_data == b'cancel':
                        await conv.send_message(bot_text["canceled"])
                        await conv.cancel_all()
                    else:
                        gp_country = gp_data.decode().split(":")[0]
                        gp_round = int(gp_data.decode().split(":")[1])
                        sessions = manager.get_session(year=year, country=gp_round)["sessions"]
                        type_tr = {
                            "Practice_1": "تمرین اول",
                            "Practice_2": "تمرین دوم",
                            "Practice_3": "تمرین سوم",
                            "Sprint": "اسپرینت",
                            "Sprint_Shootout": "اسپرینت شوت آوت",
                            "Sprint_Qualifying": "تعیین خط اسپرینت",
                            "Qualifying": "تعیین خط",
                            "Race": "مسابقه"
                        }
                        sessions_keys = []
                        for session in sessions:
                            if lang == 1:
                                try:
                                    session_text = sessions_convert[session]
                                except KeyError:
                                    session_text = session
                            else:
                                session_text = type_tr[session]
                            session_key = [
                                Button.inline(session_text, session.encode()),
                            ]
                            sessions_keys.append(session_key)
                        ask_event = await event.reply(bot_text["select_session"], buttons=sessions_keys)
                        try:
                            session_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                            await bot.delete_messages(user_id, ask_event.id)
                        except TimeoutError:
                            await conv.send_message(bot_text["timeout_error"])
                            await bot.delete_messages(user_id, ask_event.id)
                            return
                        event_data = session_res.data
                        if event_data == b'cancel':
                            await conv.send_message(bot_text["canceled"])
                            await conv.cancel_all()
                        else:
                            session = event_data.decode()
                            if year == 2024:
                                # دریافت تاریخ مسابقه از API
                                check_date = f"https://ergast.com/api/f1/{year}.json"
                                check_date = requests.get(check_date).json()["MRData"]["RaceTable"]["Races"]

                                for grand in check_date:
                                    if grand["raceName"] == gp:
                                        now = datetime.now()
                                        now_date_str = f"{now.year}-{now.month:02d}-{now.day:02d}"
                                        now_time_str = now.strftime("%H:%M:%S")
                                        
                                        # ترکیب تاریخ و ساعت فعلی
                                        now_datetime_str = f"{now_date_str} {now_time_str}"
                                        now_datetime = datetime.strptime(now_datetime_str, "%Y-%m-%d %H:%M:%S")
                                        
                                        if session == "Race":
                                            race_date = grand["date"]
                                        elif session == "Sprint":
                                            race_date = grand["Sprint"]["date"]
                                        elif session == "Practice_1":
                                            race_date = grand["FirstPractice"]["date"]
                                        elif session == "Practice_2":
                                            race_date = grand["SecondPractice"]["date"]
                                        elif session == "Practice_3":
                                            race_date = grand["ThirdPractice"]["date"]
                                        elif session == "Qualifying":
                                            race_date = grand["Qualifying"]["date"]
                                        else:
                                            await conv.send_message(bot_text["action_not_found"])
                                            return
                                        print("rpm session", session)
                                        if check_date_passed(race_date) is False:
                                            race_hour = cur.execute(f"SELECT time FROM grand_time WHERE grand = '{gp}' AND session_type = '{session}';").fetchone()
                                            if race_hour is None:
                                                print("race hour", race_hour)
                                                print("session and grand", gp, session)
                                                print("check date", check_date_passed(race_date))
                                                await conv.send_message(bot_text["problem"])
                                                return
                                            race_hour = race_hour[0]
                                            # ترکیب تاریخ و ساعت مسابقه
                                            race_datetime_str = f"{race_date} {race_hour}"
                                            race_datetime = datetime.strptime(race_datetime_str, "%Y-%m-%d %H:%M:%S")
                                            
                                            if now_datetime < race_datetime:
                                                await conv.send_message(bot_text["dont_time"])
                                                return
                            url = f"http://ergast.com/api/f1/{year}/{gp_round}/drivers.json"
                            if config.ergast:
                                drivers = requests.get(url).json()["MRData"]["DriverTable"]["Drivers"]
                            else:
                                drivers = ergast_data["MRData"]["DriverTable"]["Drivers"]
                            drivers_keys = []
                            if config.ergast:
                                for driver in drivers:
                                    if lang == 1:
                                        driver_name = driver["givenName"] + driver["familyName"]
                                    else:
                                        driver_name = drivers_translate[driver["givenName"] + "_" + driver["familyName"]]
                                    driver_code = driver["code"]
                                    key = Button.inline(driver_name, data=driver_code.encode())
                                    drivers_keys.append(key)
                            else:
                                for driver in drivers:
                                    if lang == 1:
                                        driver_name = driver["givenName"] + driver["familyName"]
                                    else:
                                        driver_name = drivers_translate[driver["givenName"] + "_" + driver["familyName"]]
                                        driver_code = driver["code"]
                                        key = Button.inline(driver_name, data=driver_code.encode())
                                        drivers_keys.append(key)
                            result = []
                            for dv in range(0, len(drivers_keys), 2):
                                if dv + 1 < len(drivers_keys):
                                    result.append([drivers_keys[dv], drivers_keys[dv + 1]])
                                else:
                                    result.append([drivers_keys[dv]])
                            cancel_btn = [Button.inline(bot_text["cancel"], b'cancel')]
                            result.append(cancel_btn)
                            ask_driver = await conv.send_message(bot_text["ask_driver_one"], buttons=result)
                            try:
                                dr_event = await conv.wait_event(events.CallbackQuery(), timeout=60)
                                print(dr_event)
                                await bot.delete_messages(user_id, ask_driver.id)
                            except TimeoutError:
                                await conv.send_message(bot_text["timeout_error"])
                                await bot.delete_messages(user_id, ask_driver.id)
                                return
                            driver_data = dr_event.data
                            if driver_data == b'cancel':
                                await conv.send_message(bot_text["canceled"])
                                await conv.cancel_all()
                            else:
                                driver_one_name = driver_data.decode()
                                gp_round = int(gp_data.decode().split(":")[1])
                                url = f"http://ergast.com/api/f1/{year}/{gp_round}/drivers.json"
                                if config.ergast:
                                    drivers = requests.get(url).json()["MRData"]["DriverTable"]["Drivers"]
                                else:
                                    drivers = ergast_data["MRData"]["DriverTable"]["Drivers"]
                                drivers_keys = []
                                if config.ergast:
                                    for driver in drivers:
                                        if lang == 1:
                                            driver_name = driver["givenName"] + driver["familyName"]
                                        else:
                                            driver_name = drivers_translate[driver["givenName"] + "_" + driver["familyName"]]
                                        driver_code = driver["code"]
                                        key = Button.inline(driver_name, data=driver_code.encode())
                                        drivers_keys.append(key)
                                else:
                                    for driver in drivers:
                                        if lang == 1:
                                            driver_name = driver["givenName"] + driver["familyName"]
                                        else:
                                            driver_name = drivers_translate[driver["givenName"] + "_" + driver["familyName"]]
                                            driver_code = driver["code"]
                                            key = Button.inline(driver_name, data=driver_code.encode())
                                            drivers_keys.append(key)
                                result = []
                                for dv in range(0, len(drivers_keys), 2):
                                    if dv + 1 < len(drivers_keys):
                                        result.append([drivers_keys[dv], drivers_keys[dv + 1]])
                                    else:
                                        result.append([drivers_keys[dv]])
                                cancel_btn = [Button.inline(bot_text["cancel"], b'cancel')]
                                result.append(cancel_btn)
                                ask_driver = await conv.send_message(bot_text["ask_driver_two"], buttons=result)
                                try:
                                    dr_event = await conv.wait_event(events.CallbackQuery(), timeout=60)
                                    await bot.delete_messages(user_id, ask_driver.id)
                                except TimeoutError:
                                    await conv.send_message(bot_text["timeout_error"])
                                    await bot.delete_messages(user_id, ask_driver.id)
                                    return
                                driver_data_two = dr_event.data
                                if driver_data == b"cancel":
                                    await conv.send_message(bot_text["canceled"])
                                    await conv.cancel_all()
                                else:
                                    driver_one_code = driver_data.decode()
                                    driver_two_code = driver_data_two.decode()
                                    session = event_data.decode()
                                    if lang == 1:
                                        loading = await conv.send_message(bot_text["loading_two"].format(year=year, gp=gp_country, event=session, driver_one=driver_buy_code_en[driver_one_code], driver_two=driver_buy_code_en[driver_two_code]))
                                    else:
                                        loading = await conv.send_message(bot_text["loading_two"].format(year=year, gp=country_tr[gp_country.replace(" ", "_")], event=type_tr[session.replace(" ", "_")], driver_one=driver_buy_code_fa[driver_one_code], driver_two=driver_buy_code_fa[driver_two_code]))
                                    BASE_DIR = Path(__file__).resolve().parent
                                    if session == "Practice_1" or session == "Practice_2" or session == "Practice_3" or session == "Sprint_Qualifying":
                                        session = sessions_convert[session]
                                    image_rpm = f"{year}-{gp_round}-{session}-{driver_one_code}-{driver_two_code}-rpm.png"
                                    image_base_rpm = fr"{BASE_DIR}/{image_rpm}"
                                    if os.path.exists(image_base_rpm) is False:
                                        image_rpm_path = speed_rpm_delta(year, gp_round, session, driver_one_code, driver_two_code)
                                    await bot.delete_messages(user_id, loading.id)
                                    await bot.send_file(user_id, caption="rpm", file=image_base_rpm)
                                    await bot.send_file(user_id, caption="rpm", file=image_base_rpm, force_document=True)
                                    config.all_statistics(event.message.message, user_id)
                                    config.small_statistics(event.message.message, user_id)
                                    user_find = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
                                    user_level = user_find[10]
                                    level_dict = {
                                        "1": bot_text["level_one"],
                                        "2": bot_text["level_two"],
                                        "3": bot_text["level_three"],
                                    }
                                    user_level_fa = level_dict[f"{user_level}"]
                                    if user_level == "1":
                                        user_score = user_find[5]
                                        user_score -= 3
                                        cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                        con.commit()
                                        await event.reply(bot_text["score_data"].format(coin=3, level=user_level_fa))
                                    elif user_level == "2":
                                        user_score = user_find[5]
                                        user_score -= 2
                                        cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                        con.commit()
                                        await event.reply(bot_text["score_data"].format(coin=2, level=user_level_fa))
                                    elif user_level == "3":
                                        user_score = user_find[5]
                                        user_score -= 1
                                        cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                        con.commit()
                                        await event.reply(bot_text["score_data"].format(coin=1, level=user_level_fa))
                                    await conv.cancel_all()
        elif text == bot_text["map_viz"]:
            find_status = cur.execute(f"SELECT status FROM data_status WHERE data = '{event.message.message}'").fetchone()
            if find_status[0] == 'off' or find_status[0] is None:
                await event.reply(bot_text["data_is_off"])
                return
            user_find = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
            user_scores = user_find[5]
            user_level = user_find[10]
            score_dict = {
                "1": 2,
                "2": 1,
                "3": 1,
            }
            score_get = score_dict[f"{user_level}"]
            if user_scores - score_get < 0:
                key = [
                    Button.inline(bot_text["account"], data=b'user_account')
                ]
                await event.reply(bot_text["coin_not_enough"].format(score=user_scores), buttons=key)
                return
            async with bot.conversation(user_id) as conv:
                year_keys = [
                    [
                        Button.inline("2024", b'2024')
                    ],
                    [
                        Button.inline("2023", b'2023')
                    ],
                    [
                        Button.inline("2022", b'2022')
                    ],
                    [
                        Button.inline("2021", b'2021')
                    ],
                    [
                        Button.inline("2020", b'2020')
                    ],
                    [
                        Button.inline("2019", b'2019')
                    ],
                    [
                        Button.inline("2018", b'2018')
                    ],
                    [
                        Button.inline(bot_text["cancel"], b'cancel')
                    ]
                ]
                ask_year = await conv.send_message(bot_text["select_year"], buttons=year_keys)
                try:
                    year_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                    await bot.delete_messages(user_id, ask_year.id)
                except TimeoutError:
                    await conv.send_message(bot_text["timeout_error"])
                    await bot.delete_messages(user_id, ask_year.id)
                    return
                year_data = year_res.data
                if year_data == b'cancel':
                    await conv.send_message(bot_text["canceled"])
                    await bot.delete_messages(user_id, ask_year.id)
                    await conv.cancel_all()
                else: 
                    year = int(year_data)
                    response = manager.get_event(year=year)["Country"]
                    gp_keys = []
                    for gp in response:
                        if lang == 1:
                            gp_text = gp["t"]
                        else:
                            gp_text = country_tr[gp["tr"]]
                        gp_data = str.encode(gp["t"] + ":" + str(gp["round_num"]))
                        key = Button.inline(gp_text, data=gp_data)
                        gp_keys.append(key)
                    result = []
                    for i in range(0, len(gp_keys), 2):
                        if i + 1 < len(gp_keys):
                            result.append([gp_keys[i], gp_keys[i + 1]])
                        else:
                            result.append([gp_keys[i]])
                    result.append([Button.inline(bot_text["cancel"], b'cancel')])
                    ask_gp = await conv.send_message(bot_text["select_gp"], buttons=result)
                    try:
                        gp_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                        await bot.delete_messages(user_id, ask_gp.id)
                    except TimeoutError:
                        await conv.send_message(bot_text["timeout_error"])
                        await bot.delete_messages(user_id, ask_gp.id)
                        return
                    gp_data = gp_res.data
                    if gp_data == b'cancel':
                        await conv.send_message(bot_text["canceled"])
                        await conv.cancel_all()
                    else:
                        gp_country = gp_data.decode().split(":")[0]
                        gp_round = int(gp_data.decode().split(":")[1])
                        sessions = manager.get_session(year=year, country=gp_round)["sessions"]
                        type_tr = {
                            "Practice_1": "تمرین اول",
                            "Practice_2": "تمرین دوم",
                            "Practice_3": "تمرین سوم",
                            "Sprint": "اسپرینت",
                            "Sprint_Shootout": "اسپرینت شوت آوت",
                            "Sprint_Qualifying": "تعیین خط اسپرینت",
                            "Qualifying": "تعیین خط",
                            "Race": "مسابقه"
                        }
                        sessions_keys = []
                        for session in sessions:
                            if lang == 1:
                                session_text = session
                            else:
                                session_text = type_tr[session]
                            session_key = [
                                Button.inline(session_text, session.encode()),
                            ]
                            sessions_keys.append(session_key)
                        ask_event = await event.reply(bot_text["select_session"], buttons=sessions_keys)
                        try:
                            session_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                            await bot.delete_messages(user_id, ask_event.id)
                        except TimeoutError:
                            await conv.send_message(bot_text["timeout_error"])
                            await bot.delete_messages(user_id, ask_event.id)
                            return
                        event_data = session_res.data
                        if event_data == b'cancel':
                            await conv.send_message(bot_text["canceled"])
                            await conv.cancel_all()
                        else:
                            session = event_data.decode()
                            if year == 2024:
                                # دریافت تاریخ مسابقه از API
                                check_date = f"https://ergast.com/api/f1/{year}.json"
                                check_date = requests.get(check_date).json()["MRData"]["RaceTable"]["Races"]

                                for grand in check_date:
                                    if grand["raceName"] == gp:
                                        now = datetime.now()
                                        now_date_str = f"{now.year}-{now.month:02d}-{now.day:02d}"
                                        now_time_str = now.strftime("%H:%M:%S")
                                        
                                        # ترکیب تاریخ و ساعت فعلی
                                        now_datetime_str = f"{now_date_str} {now_time_str}"
                                        now_datetime = datetime.strptime(now_datetime_str, "%Y-%m-%d %H:%M:%S")
                                        
                                        if session == "Race":
                                            race_date = grand["date"]
                                        elif session == "Sprint":
                                            race_date = grand["Sprint"]["date"]
                                        elif session == "Practice_1":
                                            race_date = grand["FirstPractice"]["date"]
                                        elif session == "Practice_2":
                                            race_date = grand["SecondPractice"]["date"]
                                        elif session == "Practice_3":
                                            race_date = grand["ThirdPractice"]["date"]
                                        elif session == "Qualifying":
                                            race_date = grand["Qualifying"]["date"]
                                        else:
                                            await conv.send_message(bot_text["action_not_found"])
                                            return
                                        if check_date_passed(race_date) is False:
                                            race_hour = cur.execute(f"SELECT time FROM grand_time WHERE grand = '{gp}' AND session_type = '{session}';").fetchone()
                                            if race_hour is None:
                                                await conv.send_message(bot_text["problem"])
                                                return
                                            race_hour = race_hour[0]
                                            # ترکیب تاریخ و ساعت مسابقه
                                            race_datetime_str = f"{race_date} {race_hour}"
                                            race_datetime = datetime.strptime(race_datetime_str, "%Y-%m-%d %H:%M:%S")
                                            
                                            if now_datetime < race_datetime:
                                                await conv.send_message(bot_text["dont_time"])
                                                return
                            url = f"http://ergast.com/api/f1/{year}/{gp_round}/drivers.json"
                            if config.ergast:
                                drivers = requests.get(url).json()["MRData"]["DriverTable"]["Drivers"]
                            else:
                                drivers = ergast_data["MRData"]["DriverTable"]["Drivers"]
                            drivers_keys = []
                            if config.ergast:
                                for driver in drivers:
                                    if lang == 1:
                                        driver_name = driver["givenName"] + driver["familyName"]
                                    else:
                                        driver_name = drivers_translate[driver["givenName"] + "_" + driver["familyName"]]
                                    driver_code = driver["code"]
                                    key = Button.inline(driver_name, data=driver_code.encode())
                                    drivers_keys.append(key)
                            else:
                                for driver in drivers:
                                    if lang == 1:
                                        driver_name = driver["givenName"] + driver["familyName"]
                                    else:
                                        driver_name = drivers_translate[driver["givenName"] + "_" + driver["familyName"]]
                                        driver_code = driver["code"]
                                        key = Button.inline(driver_name, data=driver_code.encode())
                                        drivers_keys.append(key)
                            result = []
                            for dv in range(0, len(drivers_keys), 2):
                                if dv + 1 < len(drivers_keys):
                                    result.append([drivers_keys[dv], drivers_keys[dv + 1]])
                                else:
                                    result.append([drivers_keys[dv]])
                            cancel_btn = [Button.inline(bot_text["cancel"], b'cancel')]
                            result.append(cancel_btn)
                            ask_driver = await conv.send_message(bot_text["ask_driver"], buttons=result)
                            try:
                                dr_event = await conv.wait_event(events.CallbackQuery(), timeout=60)
                                await bot.delete_messages(user_id, ask_driver.id)
                            except TimeoutError:
                                await conv.send_message(bot_text["timeout_error"])
                                await bot.delete_messages(user_id, ask_driver.id)
                                return
                            driver_data = dr_event.data
                            if driver_data == b'cancel':
                                await conv.send_message(bot_text["canceled"])
                                await conv.cancel_all()
                            else:
                                driver_code = driver_data.decode()
                                session = event_data.decode()
                                if lang == 1:
                                    loading = await conv.send_message(bot_text["loading_one"].format(year=year, gp=gp_country, event=session, driver_one=driver_buy_code_en[driver_code]))
                                else:
                                    loading = await conv.send_message(bot_text["loading_one"].format(year=year, gp=country_tr[gp_country.replace(" ", "_")], event=type_tr[session.replace(" ", "_")], driver_one=driver_buy_code_fa[driver_code]))
                                BASE_DIR = Path(__file__).resolve().parent
                                if session == "Practice_1" or session == "Practice_2" or session == "Practice_3":
                                    session = sessions_convert[session]
                                image_viz = f"{year}-{gp_round}-{session}-{driver_code}-map_viz.png"
                                image_base_viz = fr"{BASE_DIR}/{image_viz}"
                                if os.path.exists(image_base_viz) is False:
                                    # print(year, gp_round, session, driver_code)
                                    image_viz_path = map_viz(year, gp_round, session, driver_code)
                                await bot.delete_messages(user_id, loading.id)
                                await bot.send_file(user_id, caption="map viz", file=image_base_viz)
                                await bot.send_file(user_id, caption="map viz", file=image_base_viz, force_document=True)
                                config.all_statistics(event.message.message, user_id)
                                config.small_statistics(event.message.message, user_id)
                                user_find = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
                                user_level = user_find[10]
                                level_dict = {
                                    "1": bot_text["level_one"],
                                    "2": bot_text["level_two"],
                                    "3": bot_text["level_three"],
                                }
                                user_level_fa = level_dict[f"{user_level}"]
                                if user_level == "1":
                                    user_score = user_find[5]
                                    user_score -= 2
                                    cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                    con.commit()
                                    await event.reply(bot_text["score_data"].format(coin=2, level=user_level_fa))
                                elif user_level == "2":
                                    user_score = user_find[5]
                                    user_score -= 1
                                    cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                    con.commit()
                                    await event.reply(bot_text["score_data"].format(coin=1, level=user_level_fa))
                                elif user_level == "3":
                                    user_score = user_find[5]
                                    user_score -= 1
                                    cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                    con.commit()
                                    await event.reply(bot_text["score_data"].format(coin=1, level=user_level_fa))
                                await conv.cancel_all()
        elif text == bot_text["map_break"]:
            find_status = cur.execute(f"SELECT status FROM data_status WHERE data = '{event.message.message}'").fetchone()
            if find_status[0] == 'off' or find_status[0] is None:
                await event.reply(bot_text["data_is_off"])
                return
            user_find = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
            user_scores = user_find[5]
            user_level = user_find[10]
            score_dict = {
                "1": 1,
                "2": 0,
                "3": 0,
            }
            score_get = score_dict[f"{user_level}"]
            if user_scores - score_get < 0:
                key = [
                    Button.inline(bot_text["account"], data=b'user_account')
                ]
                await event.reply(bot_text["coin_not_enough"].format(score=user_scores), buttons=key)
                return
            async with bot.conversation(user_id) as conv:
                year_keys = [
                    [
                        Button.inline("2024", b'2024')
                    ],
                    [
                        Button.inline("2023", b'2023')
                    ],
                    [
                        Button.inline("2022", b'2022')
                    ],
                    [
                        Button.inline("2021", b'2021')
                    ],
                    [
                        Button.inline("2020", b'2020')
                    ],
                    [
                        Button.inline("2019", b'2019')
                    ],
                    [
                        Button.inline("2018", b'2018')
                    ],
                    [
                        Button.inline(bot_text["cancel"], b'cancel')
                    ]
                ]
                ask_year = await conv.send_message(bot_text["select_year"], buttons=year_keys)
                try:
                    year_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                    await bot.delete_messages(user_id, ask_year.id)
                except TimeoutError:
                    await conv.send_message(bot_text["timeout_error"])
                    await bot.delete_messages(user_id, ask_year.id)
                    return
                year_data = year_res.data
                if year_data == b'cancel':
                    await conv.send_message(bot_text["canceled"])
                    await bot.delete_messages(user_id, ask_year.id)
                    await conv.cancel_all()
                else: 
                    year = int(year_data)
                    response = manager.get_event(year=year)["Country"]
                    gp_keys = []
                    for gp in response:
                        if lang == 1:
                            gp_text = gp["t"]
                        else:
                            gp_text = country_tr[gp["tr"]]
                        gp_data = str.encode(gp["t"] + ":" + str(gp["round_num"]))
                        key = Button.inline(gp_text, data=gp_data)
                        gp_keys.append(key)
                    result = []
                    for i in range(0, len(gp_keys), 2):
                        if i + 1 < len(gp_keys):
                            result.append([gp_keys[i], gp_keys[i + 1]])
                        else:
                            result.append([gp_keys[i]])
                    result.append([Button.inline(bot_text["cancel"], b'cancel')])
                    ask_gp = await conv.send_message(bot_text["select_gp"], buttons=result)
                    try:
                        gp_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                        await bot.delete_messages(user_id, ask_gp.id)
                    except TimeoutError:
                        await conv.send_message(bot_text["timeout_error"])
                        await bot.delete_messages(user_id, ask_gp.id)
                        return
                    gp_data = gp_res.data
                    if gp_data == b'cancel':
                        await conv.send_message(bot_text["canceled"])
                        await conv.cancel_all()
                    else:
                        gp_country = gp_data.decode().split(":")[0]
                        gp_round = int(gp_data.decode().split(":")[1])
                        sessions = manager.get_session(year=year, country=gp_round)["sessions"]
                        type_tr = {
                            "Practice_1": "تمرین اول",
                            "Practice_2": "تمرین دوم",
                            "Practice_3": "تمرین سوم",
                            "Sprint": "اسپرینت",
                            "Sprint_Shootout": "اسپرینت شوت آوت",
                            "Sprint_Qualifying": "تعیین خط اسپرینت",
                            "Qualifying": "تعیین خط",
                            "Race": "مسابقه"
                        }
                        sessions_keys = []
                        for session in sessions:
                            if lang == 1:
                                session_text = session
                            else:
                                session_text = type_tr[session]
                            session_key = [
                                Button.inline(session_text, session.encode()),
                            ]
                            sessions_keys.append(session_key)
                        ask_event = await event.reply(bot_text["select_session"], buttons=sessions_keys)
                        try:
                            session_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                            await bot.delete_messages(user_id, ask_event.id)
                        except TimeoutError:
                            await conv.send_message(bot_text["timeout_error"])
                            await bot.delete_messages(user_id, ask_event.id)
                            return
                        event_data = session_res.data
                        if event_data == b'cancel':
                            await conv.send_message(bot_text["canceled"])
                            await conv.cancel_all()
                        else:
                            session = event_data.decode()
                            if year == 2024:
                                # دریافت تاریخ مسابقه از API
                                check_date = f"https://ergast.com/api/f1/{year}.json"
                                check_date = requests.get(check_date).json()["MRData"]["RaceTable"]["Races"]

                                for grand in check_date:
                                    if grand["raceName"] == gp:
                                        now = datetime.now()
                                        now_date_str = f"{now.year}-{now.month:02d}-{now.day:02d}"
                                        now_time_str = now.strftime("%H:%M:%S")
                                        
                                        # ترکیب تاریخ و ساعت فعلی
                                        now_datetime_str = f"{now_date_str} {now_time_str}"
                                        now_datetime = datetime.strptime(now_datetime_str, "%Y-%m-%d %H:%M:%S")
                                        
                                        if session == "Race":
                                            race_date = grand["date"]
                                        elif session == "Sprint":
                                            race_date = grand["Sprint"]["date"]
                                        elif session == "Practice_1":
                                            race_date = grand["FirstPractice"]["date"]
                                        elif session == "Practice_2":
                                            race_date = grand["SecondPractice"]["date"]
                                        elif session == "Practice_3":
                                            race_date = grand["ThirdPractice"]["date"]
                                        elif session == "Qualifying":
                                            race_date = grand["Qualifying"]["date"]
                                        else:
                                            await conv.send_message(bot_text["action_not_found"])
                                            return
                                        if check_date_passed(race_date) is False:
                                            race_hour = cur.execute(f"SELECT time FROM grand_time WHERE grand = '{gp}' AND session_type = '{session}';").fetchone()
                                            if race_hour is None:
                                                await conv.send_message(bot_text["problem"])
                                                return
                                            race_hour = race_hour[0]
                                            # ترکیب تاریخ و ساعت مسابقه
                                            race_datetime_str = f"{race_date} {race_hour}"
                                            race_datetime = datetime.strptime(race_datetime_str, "%Y-%m-%d %H:%M:%S")
                                            
                                            if now_datetime < race_datetime:
                                                await conv.send_message(bot_text["dont_time"])
                                                return
                            url = f"http://ergast.com/api/f1/{year}/{gp_round}/drivers.json"
                            if config.ergast:
                                drivers = requests.get(url).json()["MRData"]["DriverTable"]["Drivers"]
                            else:
                                drivers = ergast_data["MRData"]["DriverTable"]["Drivers"]
                            drivers_keys = []
                            if config.ergast:
                                for driver in drivers:
                                    if lang == 1:
                                        driver_name = driver["givenName"] + driver["familyName"]
                                    else:
                                        driver_name = drivers_translate[driver["givenName"] + "_" + driver["familyName"]]
                                    driver_code = driver["code"]
                                    key = Button.inline(driver_name, data=driver_code.encode())
                                    drivers_keys.append(key)
                            else:
                                for driver in drivers:
                                    if lang == 1:
                                        driver_name = driver["givenName"] + driver["familyName"]
                                    else:
                                        driver_name = drivers_translate[driver["givenName"] + "_" + driver["familyName"]]
                                        driver_code = driver["code"]
                                        key = Button.inline(driver_name, data=driver_code.encode())
                                        drivers_keys.append(key)
                            result = []
                            for dv in range(0, len(drivers_keys), 2):
                                if dv + 1 < len(drivers_keys):
                                    result.append([drivers_keys[dv], drivers_keys[dv + 1]])
                                else:
                                    result.append([drivers_keys[dv]])
                            cancel_btn = [Button.inline(bot_text["cancel"], b'cancel')]
                            result.append(cancel_btn)
                            ask_driver = await conv.send_message(bot_text["ask_driver"], buttons=result)
                            try:
                                dr_event = await conv.wait_event(events.CallbackQuery(), timeout=60)
                                await bot.delete_messages(user_id, ask_driver.id)
                            except TimeoutError:
                                await conv.send_message(bot_text["timeout_error"])
                                await bot.delete_messages(user_id, ask_driver.id)
                                return
                            driver_data = dr_event.data
                            if driver_data == b'cancel':
                                await conv.send_message(bot_text["canceled"])
                                await conv.cancel_all()
                            else:
                                driver_code = driver_data.decode()
                                session = event_data.decode()
                                if lang == 1:
                                    loading = await conv.send_message(bot_text["loading_one"].format(year=year, gp=gp_country, event=session, driver_one=driver_buy_code_en[driver_code]))
                                else:
                                    loading = await conv.send_message(bot_text["loading_one"].format(year=year, gp=country_tr[gp_country.replace(" ", "_")], event=type_tr[session.replace(" ", "_")], driver_one=driver_buy_code_fa[driver_code]))
                                BASE_DIR = Path(__file__).resolve().parent
                                if session == "Practice_1" or session == "Practice_2" or session == "Practice_3":
                                    session = sessions_convert[session]
                                image_map = f"{year}-{gp_round}-{session}-{driver_code}-map_brake.png"
                                image_base_map = fr"{BASE_DIR}/{image_map}"
                                if os.path.exists(image_base_map) is False:
                                    # print(year, gp_round, session, driver_code)
                                    image_map_path = map_brake(year, gp_round, session, driver_code)
                                await bot.delete_messages(user_id, loading.id)
                                await bot.send_file(user_id, caption="map brake", file=image_base_map)
                                await bot.send_file(user_id, caption="map brake", file=image_base_map, force_document=True)
                                config.all_statistics(event.message.message, user_id)
                                config.small_statistics(event.message.message, user_id)
                                user_find = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
                                user_level = user_find[10]
                                level_dict = {
                                    "1": bot_text["level_one"],
                                    "2": bot_text["level_two"],
                                    "3": bot_text["level_three"],
                                }
                                user_level_fa = level_dict[f"{user_level}"]
                                if user_level == "1":
                                    user_score = user_find[5]
                                    user_score -= 1
                                    cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                    con.commit()
                                    await event.reply(bot_text["score_data"].format(coin=1, level=user_level_fa))
                                await conv.cancel_all()
        elif text == bot_text["down_force"]:
            find_status = cur.execute(f"SELECT status FROM data_status WHERE data = '{event.message.message}'").fetchone()
            if find_status[0] == 'off' or find_status[0] is None:
                await event.reply(bot_text["data_is_off"])
                return
            user_find = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
            user_scores = user_find[5]
            user_level = user_find[10]
            score_dict = {
                "1": 2,
                "2": 1,
                "3": 1,
            }
            score_get = score_dict[f"{user_level}"]
            if user_scores - score_get < 0:
                key = [
                    Button.inline(bot_text["account"], data=b'user_account')
                ]
                await event.reply(bot_text["coin_not_enough"].format(score=user_scores), buttons=key)
                return
            async with bot.conversation(user_id) as conv:
                year_keys = [
                    [
                        Button.inline("2024", b'2024')
                    ],
                    [
                        Button.inline("2023", b'2023')
                    ],
                    [
                        Button.inline("2022", b'2022')
                    ],
                    [
                        Button.inline("2021", b'2021')
                    ],
                    [
                        Button.inline("2020", b'2020')
                    ],
                    [
                        Button.inline("2019", b'2019')
                    ],
                    [
                        Button.inline("2018", b'2018')
                    ],
                    [
                        Button.inline(bot_text["cancel"], b'cancel')
                    ]
                ]
                ask_year = await conv.send_message(bot_text["select_year"], buttons=year_keys)
                try:
                    year_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                    await bot.delete_messages(user_id, ask_year.id)
                except TimeoutError:
                    await conv.send_message(bot_text["timeout_error"])
                    await bot.delete_messages(user_id, ask_year.id)
                    return
                year_data = year_res.data
                if year_data == b'cancel':
                    await conv.send_message(bot_text["canceled"])
                    await bot.delete_messages(user_id, ask_year.id)
                    await conv.cancel_all()
                else: 
                    year = int(year_data)
                    response = manager.get_event(year=year)["Country"]
                    gp_keys = []
                    for gp in response:
                        if lang == 1:
                            gp_text = gp["t"]
                        else:
                            gp_text = country_tr[gp["tr"]]
                        gp_data = gp["t"].encode()
                        key = Button.inline(gp_text, data=gp_data)
                        gp_keys.append(key)
                    result = []
                    for i in range(0, len(gp_keys), 2):
                        if i + 1 < len(gp_keys):
                            result.append([gp_keys[i], gp_keys[i + 1]])
                        else:
                            result.append([gp_keys[i]])
                    result.append([Button.inline(bot_text["cancel"], b'cancel')])
                    ask_gp = await conv.send_message(bot_text["select_gp"], buttons=result)
                    try:
                        gp_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                        await bot.delete_messages(user_id, ask_gp.id)
                    except TimeoutError:
                        await conv.send_message(bot_text["timeout_error"])
                        await bot.delete_messages(user_id, ask_gp.id)
                        return
                    gp_data = gp_res.data
                    if gp_data == b'cancel':
                        await conv.send_message(bot_text["canceled"])
                        await conv.cancel_all()
                    else:
                        gp = gp_data.decode()        
                        # url = f"https://f1datas.com/api/v1/fastf1/session?year={year}&country={gp}"
                        sessions = manager.get_session(year=year, country=gp)["sessions"]
                        # sessions = requests.get(url).json()["sessions"]
                        type_tr = {
                            "Practice_1": "تمرین اول",
                            "Practice_2": "تمرین دوم",
                            "Practice_3": "تمرین سوم",
                            "Sprint": "اسپرینت",
                            "Sprint_Shootout": "اسپرینت شوت آوت",
                            "Sprint_Qualifying": "تعیین خط اسپرینت",
                            "Qualifying": "تعیین خط",
                            "Race": "مسابقه"
                        }
                        sessions_keys = []
                        for session in sessions:
                            if lang == 1:
                                session_text = session
                            else:
                                session_text = type_tr[session]
                            session_key = [
                                Button.inline(session_text, session.encode()),
                            ]
                            sessions_keys.append(session_key)
                        ask_event = await event.reply(bot_text["select_session"], buttons=sessions_keys)
                        try:
                            session_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                            await bot.delete_messages(user_id, ask_event.id)
                        except TimeoutError:
                            await conv.send_message(bot_text["timeout_error"])
                            await bot.delete_messages(user_id, ask_event.id)
                            return
                        event_data = session_res.data
                        if event_data == b'cancel':
                            await conv.send_message(bot_text["canceled"])
                            await conv.cancel_all()
                        else:
                            session = event_data.decode()
                            if year == 2024:
                                # دریافت تاریخ مسابقه از API
                                check_date = f"https://ergast.com/api/f1/{year}.json"
                                check_date = requests.get(check_date).json()["MRData"]["RaceTable"]["Races"]

                                for grand in check_date:
                                    if grand["raceName"] == gp:
                                        now = datetime.now()
                                        now_date_str = f"{now.year}-{now.month:02d}-{now.day:02d}"
                                        now_time_str = now.strftime("%H:%M:%S")
                                        
                                        # ترکیب تاریخ و ساعت فعلی
                                        now_datetime_str = f"{now_date_str} {now_time_str}"
                                        now_datetime = datetime.strptime(now_datetime_str, "%Y-%m-%d %H:%M:%S")
                                        
                                        if session == "Race":
                                            race_date = grand["date"]
                                        elif session == "Sprint":
                                            race_date = grand["Sprint"]["date"]
                                        elif session == "Practice_1":
                                            race_date = grand["FirstPractice"]["date"]
                                        elif session == "Practice_2":
                                            race_date = grand["SecondPractice"]["date"]
                                        elif session == "Practice_3":
                                            race_date = grand["ThirdPractice"]["date"]
                                        elif session == "Qualifying":
                                            race_date = grand["Qualifying"]["date"]
                                        else:
                                            await conv.send_message(bot_text["action_not_found"])
                                            return
                                        if check_date_passed(race_date) is False:
                                            race_hour = cur.execute(f"SELECT time FROM grand_time WHERE grand = '{gp}' AND session_type = '{session}';").fetchone()
                                            if race_hour is None:
                                                await conv.send_message(bot_text["problem"])
                                                return
                                            race_hour = race_hour[0]
                                            # ترکیب تاریخ و ساعت مسابقه
                                            race_datetime_str = f"{race_date} {race_hour}"
                                            race_datetime = datetime.strptime(race_datetime_str, "%Y-%m-%d %H:%M:%S")
                                            
                                            if now_datetime < race_datetime:
                                                await conv.send_message(bot_text["dont_time"])
                                                return
                            if lang == 1:
                                loading = await conv.send_message(bot_text["loading"].format(year=year, gp=gp, event=session))
                            else:
                                loading = await conv.send_message(bot_text["loading"].format(year=year, gp=country_tr[gp.replace(" ", "_")], event=type_tr[session.replace(" ", "_")]))
                            BASE_DIR = Path(__file__).resolve().parent
                            if session == "Practice_1" or session == "Practice_2" or session == "Practice_3":
                                session = sessions_convert[session]
                            image_force = f"{year}-{gp}-{session}-down_force.png"
                            image_base_force = fr"{BASE_DIR}/{image_force}"
                            if os.path.exists(image_base_force) is False:
                                down_force_path = down_force(year, gp, session)
                            await bot.delete_messages(user_id, loading.id)
                            await bot.send_file(user_id, caption="Down Force", file=image_base_force)
                            await bot.send_file(user_id, caption="Down Force", file=image_base_force, force_document=True)
                            config.all_statistics(event.message.message, user_id)
                            config.small_statistics(event.message.message, user_id)
                            user_find = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
                            user_level = user_find[10]
                            level_dict = {
                                "1": bot_text["level_one"],
                                "2": bot_text["level_two"],
                                "3": bot_text["level_three"],
                            }
                            user_level_fa = level_dict[f"{user_level}"]
                            if user_level == "1":
                                user_score = user_find[5]
                                user_score -= 2
                                cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                con.commit()
                                await event.reply(bot_text["score_data"].format(coin=2, level=user_level_fa))
                            elif user_level == "2":
                                user_score = user_find[5]
                                user_score -= 1
                                cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                con.commit()
                                await event.reply(bot_text["score_data"].format(coin=1, level=user_level_fa))
                            elif user_level == "3":
                                user_score = user_find[5]
                                user_score -= 1
                                cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                con.commit()
                                await event.reply(bot_text["score_data"].format(coin=1, level=user_level_fa))
                            await conv.cancel_all()
        elif text == bot_text["start_reaction"]:
            find_status = cur.execute(f"SELECT status FROM data_status WHERE data = '{event.message.message}'").fetchone()
            if find_status[0] == 'off' or find_status[0] is None:
                await event.reply(bot_text["data_is_off"])
                return
            user_find = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
            user_scores = user_find[5]
            user_level = user_find[10]
            score_dict = {
                "1": 2,
                "2": 1,
                "3": 1,
            }
            score_get = score_dict[f"{user_level}"]
            if user_scores - score_get < 0:
                key = [
                    Button.inline(bot_text["account"], data=b'user_account')
                ]
                await event.reply(bot_text["coin_not_enough"].format(score=user_scores), buttons=key)
                return
            async with bot.conversation(user_id) as conv:
                year_keys = [
                    [
                        Button.inline("2024", b'2024')
                    ],
                    [
                        Button.inline("2023", b'2023')
                    ],
                    [
                        Button.inline("2022", b'2022')
                    ],
                    [
                        Button.inline("2021", b'2021')
                    ],
                    [
                        Button.inline("2020", b'2020')
                    ],
                    [
                        Button.inline("2019", b'2019')
                    ],
                    [
                        Button.inline("2018", b'2018')
                    ],
                    [
                        Button.inline(bot_text["cancel"], b'cancel')
                    ]
                ]
                ask_year = await conv.send_message(bot_text["select_year"], buttons=year_keys)
                try:
                    year_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                    await bot.delete_messages(user_id, ask_year.id)
                except TimeoutError:
                    await conv.send_message(bot_text["timeout_error"])
                    await bot.delete_messages(user_id, ask_year.id)
                    return
                year_data = year_res.data
                if year_data == b'cancel':
                    await conv.send_message(bot_text["canceled"])
                    await bot.delete_messages(user_id, ask_year.id)
                    await conv.cancel_all()
                else: 
                    year = int(year_data)
                    response = manager.get_event(year=year)["Country"]
                    gp_keys = []
                    for gp in response:
                        if lang == 1:
                            gp_text = gp["t"]
                        else:
                            gp_text = country_tr[gp["tr"]]
                        gp_data = gp["t"].encode()
                        key = Button.inline(gp_text, data=gp_data)
                        gp_keys.append(key)
                    result = []
                    for i in range(0, len(gp_keys), 2):
                        if i + 1 < len(gp_keys):
                            result.append([gp_keys[i], gp_keys[i + 1]])
                        else:
                            result.append([gp_keys[i]])
                    result.append([Button.inline(bot_text["cancel"], b'cancel')])
                    ask_gp = await conv.send_message(bot_text["select_gp"], buttons=result)
                    try:
                        gp_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                        await bot.delete_messages(user_id, ask_gp.id)
                    except TimeoutError:
                        await conv.send_message(bot_text["timeout_error"])
                        await bot.delete_messages(user_id, ask_gp.id)
                        return
                    gp_data = gp_res.data
                    if gp_data == b'cancel':
                        await conv.send_message(bot_text["canceled"])
                        await conv.cancel_all()
                    else:
                        gp = gp_data.decode()
                        session = "Race"
                        type_tr = {
                            "Practice_1": "تمرین اول",
                            "Practice_2": "تمرین دوم",
                            "Practice_3": "تمرین سوم",
                            "Sprint": "اسپرینت",
                            "Sprint_Shootout": "اسپرینت شوت آوت",
                            "Sprint_Qualifying": "تعیین خط اسپرینت",
                            "Qualifying": "تعیین خط",
                            "Race": "مسابقه"
                        }
                        if year == 2024:
                            # دریافت تاریخ مسابقه از API
                            check_date = f"https://ergast.com/api/f1/{year}.json"
                            check_date = requests.get(check_date).json()["MRData"]["RaceTable"]["Races"]

                            for grand in check_date:
                                if grand["raceName"] == gp:
                                    now = datetime.now()
                                    now_date_str = f"{now.year}-{now.month:02d}-{now.day:02d}"
                                    now_time_str = now.strftime("%H:%M:%S")
                                    
                                    # ترکیب تاریخ و ساعت فعلی
                                    now_datetime_str = f"{now_date_str} {now_time_str}"
                                    now_datetime = datetime.strptime(now_datetime_str, "%Y-%m-%d %H:%M:%S")
                                    
                                    if session == "Race":
                                        race_date = grand["date"]
                                    elif session == "Sprint":
                                        race_date = grand["Sprint"]["date"]
                                    elif session == "Practice_1":
                                        race_date = grand["FirstPractice"]["date"]
                                    elif session == "Practice_2":
                                        race_date = grand["SecondPractice"]["date"]
                                    elif session == "Practice_3":
                                        race_date = grand["ThirdPractice"]["date"]
                                    elif session == "Qualifying":
                                        race_date = grand["Qualifying"]["date"]
                                    else:
                                        await conv.send_message(bot_text["action_not_found"])
                                        return
                                    if check_date_passed(race_date) is False:
                                        race_hour = cur.execute(f"SELECT time FROM grand_time WHERE grand = '{gp}' AND session_type = '{session}';").fetchone()
                                        if race_hour is None:
                                            await conv.send_message(bot_text["problem"])
                                            return
                                        race_hour = race_hour[0]
                                        # ترکیب تاریخ و ساعت مسابقه
                                        race_datetime_str = f"{race_date} {race_hour}"
                                        race_datetime = datetime.strptime(race_datetime_str, "%Y-%m-%d %H:%M:%S")
                                        
                                        if now_datetime < race_datetime:
                                            await conv.send_message(bot_text["dont_time"])
                                            return
                        if lang == 1:
                            loading = await conv.send_message(bot_text["loading"].format(year=year, gp=gp, event=session))
                        else:
                            loading = await conv.send_message(bot_text["loading"].format(year=year, gp=country_tr[gp.replace(" ", "_")], event=type_tr[session.replace(" ", "_")]))
                        BASE_DIR = Path(__file__).resolve().parent
                        if session == "Practice_1" or session == "Practice_2" or session == "Practice_3":
                            session = sessions_convert[session]
                        image_reaction = f"{year}-{gp}-{session}-reaction.png"
                        image_base_reaction = fr"{BASE_DIR}/{image_reaction}"
                        if os.path.exists(image_base_reaction) is False:
                            start_reaction_path = start_reaction(year, gp, session)
                        await bot.delete_messages(user_id, loading.id)
                        await bot.send_file(user_id, caption="Reaction", file=image_base_reaction)
                        await bot.send_file(user_id, caption="Reaction", file=image_base_reaction, force_document=True)
                        config.all_statistics(event.message.message, user_id)
                        config.small_statistics(event.message.message, user_id)
                        user_find = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
                        user_level = user_find[10]
                        level_dict = {
                            "1": bot_text["level_one"],
                            "2": bot_text["level_two"],
                            "3": bot_text["level_three"],
                        }
                        user_level_fa = level_dict[f"{user_level}"]
                        if user_level == "1":
                            user_score = user_find[5]
                            user_score -= 2
                            cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                            con.commit()
                            await event.reply(bot_text["score_data"].format(coin=2, level=user_level_fa))
                        elif user_level == "2":
                            user_score = user_find[5]
                            user_score -= 1
                            cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                            con.commit()
                            await event.reply(bot_text["score_data"].format(coin=1, level=user_level_fa))
                        elif user_level == "3":
                            user_score = user_find[5]
                            user_score -= 1
                            cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                            con.commit()
                            await event.reply(bot_text["score_data"].format(coin=1, level=user_level_fa))
                        await conv.cancel_all()
        elif text == bot_text["all"]:
            find_status = cur.execute(f"SELECT status FROM data_status WHERE data = '{event.message.message}'").fetchone()
            if find_status[0] == 'off' or find_status[0] is None:
                await event.reply(bot_text["data_is_off"])
                return
            user_find = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
            user_scores = user_find[5]
            user_level = user_find[10]
            score_dict = {
                "1": 5,
                "2": 3,
                "3": 3,
            }
            score_get = score_dict[f"{user_level}"]
            if user_scores - score_get < 0:
                key = [
                    Button.inline(bot_text["account"], data=b'user_account')
                ]
                await event.reply(bot_text["coin_not_enough"].format(score=user_scores), buttons=key)
                return
            async with bot.conversation(user_id) as conv:
                year_keys = [
                    [
                        Button.inline("2024", b'2024')
                    ],
                    [
                        Button.inline("2023", b'2023')
                    ],
                    [
                        Button.inline("2022", b'2022')
                    ],
                    [
                        Button.inline("2021", b'2021')
                    ],
                    [
                        Button.inline("2020", b'2020')
                    ],
                    [
                        Button.inline("2019", b'2019')
                    ],
                    [
                        Button.inline("2018", b'2018')
                    ],
                    [
                        Button.inline(bot_text["cancel"], b'cancel')
                    ]
                ]
                ask_year = await conv.send_message(bot_text["select_year"], buttons=year_keys)
                try:
                    year_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                    await bot.delete_messages(user_id, ask_year.id)
                except TimeoutError:
                    await conv.send_message(bot_text["timeout_error"])
                    await bot.delete_messages(user_id, ask_year.id)
                    return
                year_data = year_res.data
                if year_data == b'cancel':
                    await conv.send_message(bot_text["canceled"])
                    await bot.delete_messages(user_id, ask_year.id)
                    await conv.cancel_all()
                else: 
                    year = int(year_data)
                    response = manager.get_event(year=year)["Country"]
                    gp_keys = []
                    for gp in response:
                        if lang == 1:
                            gp_text = gp["t"]
                        else:
                            gp_text = country_tr[gp["tr"]]
                        gp_data = str.encode(gp["t"] + ":" + str(gp["round_num"]))
                        key = Button.inline(gp_text, data=gp_data)
                        gp_keys.append(key)
                    result = []
                    for i in range(0, len(gp_keys), 2):
                        if i + 1 < len(gp_keys):
                            result.append([gp_keys[i], gp_keys[i + 1]])
                        else:
                            result.append([gp_keys[i]])
                    result.append([Button.inline(bot_text["cancel"], b'cancel')])
                    ask_gp = await conv.send_message(bot_text["select_gp"], buttons=result)
                    try:
                        gp_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                        await bot.delete_messages(user_id, ask_gp.id)
                    except TimeoutError:
                        await conv.send_message(bot_text["timeout_error"])
                        await bot.delete_messages(user_id, ask_gp.id)
                        return
                    gp_data = gp_res.data
                    if gp_data == b'cancel':
                        await conv.send_message(bot_text["canceled"])
                        await conv.cancel_all()
                    else:
                        gp_country = gp_data.decode().split(":")[0]
                        gp_round = int(gp_data.decode().split(":")[1])
                        sessions = manager.get_session(year=year, country=gp_round)["sessions"]
                        type_tr = {
                            "Practice_1": "تمرین اول",
                            "Practice_2": "تمرین دوم",
                            "Practice_3": "تمرین سوم",
                            "Sprint": "اسپرینت",
                            "Sprint_Shootout": "اسپرینت شوت آوت",
                            "Sprint_Qualifying": "تعیین خط اسپرینت",
                            "Qualifying": "تعیین خط",
                            "Race": "مسابقه"
                        }
                        sessions_keys = []
                        for session in sessions:
                            if lang == 1:
                                session_text = session
                            else:
                                session_text = type_tr[session]
                            session_key = [
                                Button.inline(session_text, session.encode()),
                            ]
                            sessions_keys.append(session_key)
                        ask_event = await event.reply(bot_text["select_session"], buttons=sessions_keys)
                        try:
                            session_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                            await bot.delete_messages(user_id, ask_event.id)
                        except TimeoutError:
                            await conv.send_message(bot_text["timeout_error"])
                            await bot.delete_messages(user_id, ask_event.id)
                            return
                        event_data = session_res.data
                        if event_data == b'cancel':
                            await conv.send_message(bot_text["canceled"])
                            await conv.cancel_all()
                        else:
                            session = event_data.decode()
                            if year == 2024:
                                # دریافت تاریخ مسابقه از API
                                check_date = f"https://ergast.com/api/f1/{year}.json"
                                check_date = requests.get(check_date).json()["MRData"]["RaceTable"]["Races"]

                                for grand in check_date:
                                    if grand["raceName"] == gp:
                                        now = datetime.now()
                                        now_date_str = f"{now.year}-{now.month:02d}-{now.day:02d}"
                                        now_time_str = now.strftime("%H:%M:%S")
                                        
                                        # ترکیب تاریخ و ساعت فعلی
                                        now_datetime_str = f"{now_date_str} {now_time_str}"
                                        now_datetime = datetime.strptime(now_datetime_str, "%Y-%m-%d %H:%M:%S")
                                        
                                        if session == "Race":
                                            race_date = grand["date"]
                                        elif session == "Sprint":
                                            race_date = grand["Sprint"]["date"]
                                        elif session == "Practice_1":
                                            race_date = grand["FirstPractice"]["date"]
                                        elif session == "Practice_2":
                                            race_date = grand["SecondPractice"]["date"]
                                        elif session == "Practice_3":
                                            race_date = grand["ThirdPractice"]["date"]
                                        elif session == "Qualifying":
                                            race_date = grand["Qualifying"]["date"]
                                        else:
                                            await conv.send_message(bot_text["action_not_found"])
                                            return
                                        if check_date_passed(race_date) is False:
                                            race_hour = cur.execute(f"SELECT time FROM grand_time WHERE grand = '{gp}' AND session_type = '{session}';").fetchone()
                                            if race_hour is None:
                                                await conv.send_message(bot_text["problem"])
                                                return
                                            race_hour = race_hour[0]
                                            # ترکیب تاریخ و ساعت مسابقه
                                            race_datetime_str = f"{race_date} {race_hour}"
                                            race_datetime = datetime.strptime(race_datetime_str, "%Y-%m-%d %H:%M:%S")
                                            
                                            if now_datetime < race_datetime:
                                                await conv.send_message(bot_text["dont_time"])
                                                return
                            url = f"http://ergast.com/api/f1/{year}/{gp_round}/drivers.json"
                            if config.ergast:
                                drivers = requests.get(url).json()["MRData"]["DriverTable"]["Drivers"]
                            else:
                                drivers = ergast_data["MRData"]["DriverTable"]["Drivers"]
                            drivers_keys = []
                            if config.ergast:
                                for driver in drivers:
                                    if lang == 1:
                                        driver_name = driver["givenName"] + driver["familyName"]
                                    else:
                                        driver_name = drivers_translate[driver["givenName"] + "_" + driver["familyName"]]
                                    driver_code = driver["code"]
                                    key = Button.inline(driver_name, data=driver_code.encode())
                                    drivers_keys.append(key)
                            else:
                                for driver in drivers:
                                    if lang == 1:
                                        driver_name = driver["givenName"] + driver["familyName"]
                                    else:
                                        driver_name = drivers_translate[driver["givenName"] + "_" + driver["familyName"]]
                                        driver_code = driver["code"]
                                        key = Button.inline(driver_name, data=driver_code.encode())
                                        drivers_keys.append(key)
                            result = []
                            for dv in range(0, len(drivers_keys), 2):
                                if dv + 1 < len(drivers_keys):
                                    result.append([drivers_keys[dv], drivers_keys[dv + 1]])
                                else:
                                    result.append([drivers_keys[dv]])
                            cancel_btn = [Button.inline(bot_text["cancel"], b'cancel')]
                            result.append(cancel_btn)
                            ask_driver = await conv.send_message(bot_text["ask_driver_one"], buttons=result)
                            try:
                                dr_event = await conv.wait_event(events.CallbackQuery(), timeout=60)
                                await bot.delete_messages(user_id, ask_driver.id)
                            except TimeoutError:
                                await conv.send_message(bot_text["timeout_error"])
                                await bot.delete_messages(user_id, ask_driver.id)
                                return
                            driver_data = dr_event.data
                            if driver_data == b'cancel':
                                await conv.send_message(bot_text["canceled"])
                                await conv.cancel_all()
                            else:
                                gp_round = int(gp_data.decode().split(":")[1])
                                url = f"http://ergast.com/api/f1/{year}/{gp_round}/drivers.json"
                                if config.ergast:
                                    drivers = requests.get(url).json()["MRData"]["DriverTable"]["Drivers"]
                                else:
                                    drivers = ergast_data["MRData"]["DriverTable"]["Drivers"]
                                drivers_keys = []
                                if config.ergast:
                                    for driver in drivers:
                                        if lang == 1:
                                            driver_name = driver["givenName"] + driver["familyName"]
                                        else:
                                            driver_name = drivers_translate[driver["givenName"] + "_" + driver["familyName"]]
                                        driver_code = driver["code"]
                                        key = Button.inline(driver_name, data=driver_code.encode())
                                        drivers_keys.append(key)
                                else:
                                    for driver in drivers:
                                        if lang == 1:
                                            driver_name = driver["givenName"] + driver["familyName"]
                                        else:
                                            driver_name = drivers_translate[driver["givenName"] + "_" + driver["familyName"]]
                                            driver_code = driver["code"]
                                            key = Button.inline(driver_name, data=driver_code.encode())
                                            drivers_keys.append(key)
                                result = []
                                for dv in range(0, len(drivers_keys), 2):
                                    if dv + 1 < len(drivers_keys):
                                        result.append([drivers_keys[dv], drivers_keys[dv + 1]])
                                    else:
                                        result.append([drivers_keys[dv]])
                                cancel_btn = [Button.inline(bot_text["cancel"], b'cancel')]
                                result.append(cancel_btn)
                                ask_driver = await conv.send_message(bot_text["ask_driver_two"], buttons=result)
                                try:
                                    dr_event = await conv.wait_event(events.CallbackQuery(), timeout=60)
                                    await bot.delete_messages(user_id, ask_driver.id)
                                except TimeoutError:
                                    await conv.send_message(bot_text["timeout_error"])
                                    await bot.delete_messages(user_id, ask_driver.id)
                                    return
                                driver_data_two = dr_event.data
                                if driver_data == b"cancel":
                                    await conv.send_message(bot_text["canceled"])
                                    await conv.cancel_all()
                                else:
                                    driver_one_code = driver_data.decode()
                                    driver_two_code = driver_data_two.decode()
                                    session = event_data.decode()
                                    if lang == 1:
                                        loading = await conv.send_message(bot_text["loading_two"].format(year=year, gp=gp_country, event=session, driver_one=driver_buy_code_en[driver_one_code], driver_two=driver_buy_code_en[driver_two_code]))
                                    else:
                                        loading = await conv.send_message(bot_text["loading_two"].format(year=year, gp=country_tr[gp_country.replace(" ", "_")], event=type_tr[session.replace(" ", "_")], driver_one=driver_buy_code_fa[driver_one_code], driver_two=driver_buy_code_fa[driver_two_code]))
                                    BASE_DIR = Path(__file__).resolve().parent
                                    if session == "Practice_1" or session == "Practice_2" or session == "Practice_3":
                                        session = sessions_convert[session]
                                    image_speed_comparison = f"{year}-{gp_round}-{session}-{driver_one_code}-{driver_two_code}_speed_comparison.png"
                                    image_base_speed = fr"{BASE_DIR}/{image_speed_comparison}"
                                    image_gear_comparison = f"{year}-{gp_round}-{session}-{driver_one_code}-{driver_two_code}_gear_comparison.png"
                                    image_base_gear = fr"{BASE_DIR}/{image_gear_comparison}"
                                    image_brake_comparison = f"{year}-{gp_round}-{session}-{driver_one_code}-{driver_two_code}_brake_comparison.png"
                                    image_base_brake = fr"{BASE_DIR}/{image_brake_comparison}"
                                    image_throttle_comparison = f"{year}-{gp_round}-{session}-{driver_one_code}-{driver_two_code}_throttle_comparison.png"
                                    image_base_throttle = fr"{BASE_DIR}/{image_throttle_comparison}"
                                    if os.path.exists(image_base_speed) is False or \
                                    os.path.exists(image_base_gear) is False or os.path.exists(image_base_brake) is False or \
                                    os.path.exists(image_base_throttle) is False:
                                        image_all_path = all_data(year, gp_round, session, driver_one_code, driver_two_code)
                                    await bot.delete_messages(user_id, loading.id)
                                    await bot.send_file(user_id, caption="All", file=[image_base_throttle, image_base_gear, image_base_brake, image_base_speed])
                                    await bot.send_file(user_id, caption="All", file=[image_base_throttle, image_base_gear, image_base_brake, image_base_speed], force_document=True)
                                    config.all_statistics(event.message.message, user_id)
                                    config.small_statistics(event.message.message, user_id)
                                    user_find = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
                                    user_level = user_find[10]
                                    level_dict = {
                                        "1": bot_text["level_one"],
                                        "2": bot_text["level_two"],
                                        "3": bot_text["level_three"],
                                    }
                                    user_level_fa = level_dict[f"{user_level}"]
                                    if user_level == "1":
                                        user_score = user_find[5]
                                        user_score -= 5
                                        cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                        con.commit()
                                        await event.reply(bot_text["score_data"].format(coin=5, level=user_level_fa))
                                    elif user_level == "2":
                                        user_score = user_find[5]
                                        user_score -= 3
                                        cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                        con.commit()
                                        await event.reply(bot_text["score_data"].format(coin=3, level=user_level_fa))
                                    elif user_level == "3":
                                        user_score = user_find[5]
                                        user_score -= 3
                                        cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                        con.commit()
                                        await event.reply(bot_text["score_data"].format(coin=3, level=user_level_fa))
        elif text == bot_text["strategy"]:
            find_status = cur.execute(f"SELECT status FROM data_status WHERE data = '{event.message.message}'").fetchone()
            if find_status[0] == 'off' or find_status[0] is None:
                await event.reply(bot_text["data_is_off"])
                return
            user_find = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
            user_scores = user_find[5]
            user_level = user_find[10]
            score_dict = {
                "1": 1,
                "2": 1,
                "3": 0,
            }
            score_get = score_dict[f"{user_level}"]
            if user_scores - score_get < 0:
                key = [
                    Button.inline(bot_text["account"], data=b'user_account')
                ]
                await event.reply(bot_text["coin_not_enough"].format(score=user_scores), buttons=key)
                return
            async with bot.conversation(user_id) as conv:
                year_keys = [
                    [
                        Button.inline("2024", b'2024')
                    ],
                    [
                        Button.inline("2023", b'2023')
                    ],
                    [
                        Button.inline("2022", b'2022')
                    ],
                    [
                        Button.inline("2021", b'2021')
                    ],
                    [
                        Button.inline("2020", b'2020')
                    ],
                    [
                        Button.inline("2019", b'2019')
                    ],
                    [
                        Button.inline("2018", b'2018')
                    ],
                    [
                        Button.inline(bot_text["cancel"], b'cancel')
                    ]
                ]
                ask_year = await conv.send_message(bot_text["select_year"], buttons=year_keys)
                try:
                    year_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                    await bot.delete_messages(user_id, ask_year.id)
                except TimeoutError:
                    await conv.send_message(bot_text["timeout_error"])
                    await bot.delete_messages(user_id, ask_year.id)
                    return
                year_data = year_res.data
                if year_data == b'cancel':
                    await conv.send_message(bot_text["canceled"])
                    await bot.delete_messages(user_id, ask_year.id)
                    await conv.cancel_all()
                else: 
                    year = int(year_data)
                    response = manager.get_event(year=year)["Country"]
                    gp_keys = []
                    for gp in response:
                        if lang == 1:
                            gp_text = gp["t"]
                        else:
                            gp_text = country_tr[gp["tr"]]
                        gp_data = gp["t"].encode()
                        key = Button.inline(gp_text, data=gp_data)
                        gp_keys.append(key)
                    result = []
                    for i in range(0, len(gp_keys), 2):
                        if i + 1 < len(gp_keys):
                            result.append([gp_keys[i], gp_keys[i + 1]])
                        else:
                            result.append([gp_keys[i]])
                    result.append([Button.inline(bot_text["cancel"], b'cancel')])
                    ask_gp = await conv.send_message(bot_text["select_gp"], buttons=result)
                    try:
                        gp_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                        await bot.delete_messages(user_id, ask_gp.id)
                    except TimeoutError:
                        await conv.send_message(bot_text["timeout_error"])
                        await bot.delete_messages(user_id, ask_gp.id)
                        return
                    gp_data = gp_res.data
                    if gp_data == b'cancel':
                        await conv.send_message(bot_text["canceled"])
                        await conv.cancel_all()
                    else:
                        gp = gp_data.decode()
                        sessions = manager.get_session(year=year, country=gp)["sessions"]
                        type_tr = {
                            "Sprint": "اسپرینت",
                            "Race": "مسابقه"
                        }
                        sessions_keys = []
                        for session in sessions:
                            if session != "Race" and session != "Sprint":
                                continue
                            else:
                                if lang == 1:
                                    session_text = session
                                else:
                                    session_text = type_tr[session]
                                session_key = [
                                    Button.inline(session_text, session.encode()),
                                ]
                                sessions_keys.append(session_key)
                        ask_event = await event.reply(bot_text["select_session"], buttons=sessions_keys)
                        try:
                            session_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                            await bot.delete_messages(user_id, ask_event.id)
                        except TimeoutError:
                            await conv.send_message(bot_text["timeout_error"])
                            await bot.delete_messages(user_id, ask_event.id)
                            return
                        event_data = session_res.data
                        if event_data == b'cancel':
                            await conv.send_message(bot_text["canceled"])
                            await conv.cancel_all()
                        else:
                            session = event_data.decode()
                            if year == 2024:
                                # ساعت مسابقه به عنوان یک رشته

                                # دریافت تاریخ مسابقه از API
                                check_date = f"https://ergast.com/api/f1/{year}.json"
                                check_date = requests.get(check_date).json()["MRData"]["RaceTable"]["Races"]

                                for grand in check_date:
                                    if grand["raceName"] == gp:
                                        now = datetime.now()
                                        now_date_str = f"{now.year}-{now.month:02d}-{now.day:02d}"
                                        now_time_str = now.strftime("%H:%M:%S")
                                        
                                        # ترکیب تاریخ و ساعت فعلی
                                        now_datetime_str = f"{now_date_str} {now_time_str}"
                                        now_datetime = datetime.strptime(now_datetime_str, "%Y-%m-%d %H:%M:%S")
                                        
                                        if session == "Race":
                                            race_date = grand["date"]
                                        elif session == "Sprint":
                                            race_date = grand["Sprint"]["date"]
                                        else:
                                            await conv.send_message(bot_text["action_not_found"])
                                            return
                                        if check_date_passed(race_date) is False:
                                            race_hour = cur.execute(f"SELECT time FROM grand_time WHERE grand = '{gp}' AND session_type = '{session}';").fetchone()
                                            if race_hour is None:
                                                await conv.send_message(bot_text["problem"])
                                                return
                                            race_hour = race_hour[0]
                                            # ترکیب تاریخ و ساعت مسابقه
                                            race_datetime_str = f"{race_date} {race_hour}"
                                            race_datetime = datetime.strptime(race_datetime_str, "%Y-%m-%d %H:%M:%S")
                                            
                                            if now_datetime < race_datetime:
                                                await conv.send_message(bot_text["dont_time"])
                                                return
                            if lang == 1:
                                loading = await conv.send_message(bot_text["loading"].format(year=year, gp=gp, event=session))
                            else:
                                loading = await conv.send_message(bot_text["loading"].format(year=year, gp=country_tr[gp.replace(" ", "_")], event=type_tr[session]))
                            BASE_DIR = Path(__file__).resolve().parent
                            image_strategy = f"{year}-{gp}-{session}_strategy.png"
                            image_base_strategy = fr"{BASE_DIR}/{image_strategy}"
                            if os.path.exists(image_base_strategy) is False:
                                try:
                                    strategy_path = strategy(year, gp, session)
                                except Exception as e:
                                    print(e)
                            await bot.delete_messages(user_id, loading.id)
                            await bot.send_file(user_id, caption="Strategy", file=image_base_strategy)
                            await bot.send_file(user_id, caption="Strategy", file=image_base_strategy, force_document=True)
                            config.all_statistics(event.message.message, user_id)
                            config.small_statistics(event.message.message, user_id)
                            user_find = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
                            user_level = user_find[10]
                            level_dict = {
                                "1": bot_text["level_one"],
                                "2": bot_text["level_two"],
                                "3": bot_text["level_three"],
                            }
                            user_level_fa = level_dict[f"{user_level}"]
                            if user_level == "1":
                                user_score = user_find[5]
                                user_score -= 1
                                cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                con.commit()
                                await event.reply(bot_text["score_data"].format(coin=1, level=user_level_fa))
                            if user_level == "2":
                                user_score = user_find[5]
                                user_score -= 1
                                cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                con.commit()
                                await event.reply(bot_text["score_data"].format(coin=1, level=user_level_fa))

                            await conv.cancel_all()
        elif text == bot_text["g_force"]:
            find_status = cur.execute(f"SELECT status FROM data_status WHERE data = '{event.message.message}'").fetchone()
            if find_status[0] == 'off' or find_status[0] is None:
                await event.reply(bot_text["data_is_off"])
                return
            keys = [
                [
                    Button.text(bot_text["driver"]),
                    Button.text(bot_text["all_info"])
                ],
                [
                    Button.text(bot_text["back"], resize=True)
                ]
            ]
            await event.reply(bot_text["select"], buttons=keys)
        elif text == bot_text["all_info"]:
            find_status = cur.execute(f"SELECT status FROM data_status WHERE data = '{event.message.message}'").fetchone()
            if find_status[0] == 'off' or find_status[0] is None:
                await event.reply(bot_text["data_is_off"])
                return
            user_find = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
            user_scores = user_find[5]
            user_level = user_find[10]
            score_dict = {
                "1": 0,
                "2": 0,
                "3": 0,
            }
            score_get = score_dict[f"{user_level}"]
            if user_scores - score_get < 0:
                key = [
                    Button.inline(bot_text["account"], data=b'user_account')
                ]
                await event.reply(bot_text["coin_not_enough"].format(score=user_scores), buttons=key)
                return
            async with bot.conversation(user_id) as conv:
                year_keys = [
                    [
                        Button.inline("2024", b'2024')
                    ],
                    [
                        Button.inline("2023", b'2023')
                    ],
                    [
                        Button.inline("2022", b'2022')
                    ],
                    [
                        Button.inline("2021", b'2021')
                    ],
                    [
                        Button.inline("2020", b'2020')
                    ],
                    [
                        Button.inline("2019", b'2019')
                    ],
                    [
                        Button.inline("2018", b'2018')
                    ],
                    [
                        Button.inline(bot_text["cancel"], b'cancel')
                    ]
                ]
                ask_year = await conv.send_message(bot_text["select_year"], buttons=year_keys)
                try:
                    year_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                    await bot.delete_messages(user_id, ask_year.id)
                except TimeoutError:
                    await conv.send_message(bot_text["timeout_error"])
                    await bot.delete_messages(user_id, ask_year.id)
                    return
                year_data = year_res.data
                if year_data == b'cancel':
                    await conv.send_message(bot_text["canceled"])
                    await bot.delete_messages(user_id, ask_year.id)
                    await conv.cancel_all()
                else: 
                    year = int(year_data)
                    response = manager.get_event(year=year)["Country"]
                    gp_keys = []
                    for gp in response:
                        if lang == 1:
                            gp_text = gp["t"]
                        else:
                            gp_text = country_tr[gp["tr"]]
                        gp_data = gp["t"].encode()
                        key = Button.inline(gp_text, data=gp_data)
                        gp_keys.append(key)
                    result = []
                    for i in range(0, len(gp_keys), 2):
                        if i + 1 < len(gp_keys):
                            result.append([gp_keys[i], gp_keys[i + 1]])
                        else:
                            result.append([gp_keys[i]])
                    result.append([Button.inline(bot_text["cancel"], b'cancel')])
                    ask_gp = await conv.send_message(bot_text["select_gp"], buttons=result)
                    try:
                        gp_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                        await bot.delete_messages(user_id, ask_gp.id)
                    except TimeoutError:
                        await conv.send_message(bot_text["timeout_error"])
                        await bot.delete_messages(user_id, ask_gp.id)
                        return
                    gp_data = gp_res.data
                    if gp_data == b'cancel':
                        await conv.send_message(bot_text["canceled"])
                        await conv.cancel_all()
                    else:
                        gp = gp_data.decode()
                        sessions = manager.get_session(year=year, country=gp)["sessions"]
                        type_tr = {
                            "Practice_1": "تمرین اول",
                            "Practice_2": "تمرین دوم",
                            "Practice_3": "تمرین سوم",
                            "Sprint": "اسپرینت",
                            "Sprint_Shootout": "اسپرینت شوت آوت",
                            "Sprint_Qualifying": "تعیین خط اسپرینت",
                            "Qualifying": "تعیین خط",
                            "Race": "مسابقه"
                        }
                        sessions_keys = []
                        for session in sessions:
                            if lang == 1:
                                session_text = session
                            else:
                                session_text = type_tr[session]
                            session_key = [
                                Button.inline(session_text, session.encode()),
                            ]
                            sessions_keys.append(session_key)
                        ask_event = await event.reply(bot_text["select_session"], buttons=sessions_keys)
                        try:
                            session_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                            await bot.delete_messages(user_id, ask_event.id)
                        except TimeoutError:
                            await conv.send_message(bot_text["timeout_error"])
                            await bot.delete_messages(user_id, ask_event.id)
                            return
                        event_data = session_res.data
                        if event_data == b'cancel':
                            await conv.send_message(bot_text["canceled"])
                            await conv.cancel_all()
                        else:
                            session = event_data.decode()
                            if year == 2024:
                                # ساعت مسابقه به عنوان یک رشته

                                # دریافت تاریخ مسابقه از API
                                check_date = f"https://ergast.com/api/f1/{year}.json"
                                check_date = requests.get(check_date).json()["MRData"]["RaceTable"]["Races"]

                                for grand in check_date:
                                    if grand["raceName"] == gp:
                                        now = datetime.now()
                                        now_date_str = f"{now.year}-{now.month:02d}-{now.day:02d}"
                                        now_time_str = now.strftime("%H:%M:%S")
                                        
                                        # ترکیب تاریخ و ساعت فعلی
                                        now_datetime_str = f"{now_date_str} {now_time_str}"
                                        now_datetime = datetime.strptime(now_datetime_str, "%Y-%m-%d %H:%M:%S")
                                        
                                        if session == "Race":
                                            race_date = grand["date"]
                                        elif session == "Sprint":
                                            race_date = grand["Sprint"]["date"]
                                        elif session == "Practice_1":
                                            race_date = grand["FirstPractice"]["date"]
                                        elif session == "Practice_2":
                                            race_date = grand["SecondPractice"]["date"]
                                        elif session == "Practice_3":
                                            race_date = grand["ThirdPractice"]["date"]
                                        elif session == "Qualifying":
                                            race_date = grand["Qualifying"]["date"]
                                        else:
                                            await conv.send_message(bot_text["action_not_found"])
                                            return
                                        if check_date_passed(race_date) is False:
                                            race_hour = cur.execute(f"SELECT time FROM grand_time WHERE grand = '{gp}' AND session_type = '{session}';").fetchone()
                                            if race_hour is None:
                                                await conv.send_message(bot_text["problem"])
                                                return
                                            race_hour = race_hour[0]
                                            # ترکیب تاریخ و ساعت مسابقه
                                            race_datetime_str = f"{race_date} {race_hour}"
                                            race_datetime = datetime.strptime(race_datetime_str, "%Y-%m-%d %H:%M:%S")
                                            
                                            if now_datetime < race_datetime:
                                                await conv.send_message(bot_text["dont_time"])
                                                return
                            if lang == 1:
                                loading = await conv.send_message(bot_text["loading"].format(year=year, gp=gp, event=session))
                            else:
                                loading = await conv.send_message(bot_text["loading"].format(year=year, gp=country_tr[gp.replace(" ", "_")], event=type_tr[session]))
                            BASE_DIR = Path(__file__).resolve().parent
                            image_all_info = f"{year}-{gp}-{session}_all_info.png"
                            image_base_info = fr"{BASE_DIR}/{image_all_info}"
                            if os.path.exists(image_base_info) is False:
                                try:
                                    info_path = all_info(year, gp, session)
                                except Exception as e:
                                    print(e)
                            await bot.delete_messages(user_id, loading.id)
                            await bot.send_file(user_id, caption="All Info", file=image_base_info)
                            await bot.send_file(user_id, caption="All Info", file=image_base_info, force_document=True)
                            config.all_statistics(event.message.message, user_id)
                            config.small_statistics(event.message.message, user_id)
                            user_find = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
                            user_level = user_find[10]
                            level_dict = {
                                "1": bot_text["level_one"],
                                "2": bot_text["level_two"],
                                "3": bot_text["level_three"],
                            }
                            user_level_fa = level_dict[f"{user_level}"]
                            if user_level == "1":
                                user_score = user_find[5]
                                user_score -= 1
                                cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                con.commit()
                                await event.reply(bot_text["score_data"].format(coin=1, level=user_level_fa))
                            await conv.cancel_all()
        elif text == bot_text["driver"]:
            find_status = cur.execute(f"SELECT status FROM data_status WHERE data = '{event.message.message}'").fetchone()
            if find_status[0] == 'off' or find_status[0] is None:
                await event.reply(bot_text["data_is_off"])
                return
            user_find = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
            user_scores = user_find[5]
            user_level = user_find[10]
            score_dict = {
                "1": 0,
                "2": 0,
                "3": 0,
            }
            score_get = score_dict[f"{user_level}"]
            if user_scores - score_get < 0:
                key = [
                    Button.inline(bot_text["account"], data=b'user_account')
                ]
                await event.reply(bot_text["coin_not_enough"].format(score=user_scores), buttons=key)
                return
            async with bot.conversation(user_id) as conv:
                year_keys = [
                    [
                        Button.inline("2024", b'2024')
                    ],
                    [
                        Button.inline("2023", b'2023')
                    ],
                    [
                        Button.inline("2022", b'2022')
                    ],
                    [
                        Button.inline("2021", b'2021')
                    ],
                    [
                        Button.inline("2020", b'2020')
                    ],
                    [
                        Button.inline("2019", b'2019')
                    ],
                    [
                        Button.inline("2018", b'2018')
                    ],
                    [
                        Button.inline(bot_text["cancel"], b'cancel')
                    ]
                ]
                ask_year = await conv.send_message(bot_text["select_year"], buttons=year_keys)
                try:
                    year_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                    await bot.delete_messages(user_id, ask_year.id)
                except TimeoutError:
                    await conv.send_message(bot_text["timeout_error"])
                    await bot.delete_messages(user_id, ask_year.id)
                    return
                year_data = year_res.data
                if year_data == b'cancel':
                    await conv.send_message(bot_text["canceled"])
                    await bot.delete_messages(user_id, ask_year.id)
                    await conv.cancel_all()
                else: 
                    year = int(year_data)
                    response = manager.get_event(year=year)["Country"]
                    gp_keys = []
                    for gp in response:
                        if lang == 1:
                            gp_text = gp["t"]
                        else:
                            gp_text = country_tr[gp["tr"]]
                        gp_data = str.encode(gp["t"] + ":" + str(gp["round_num"]))
                        key = Button.inline(gp_text, data=gp_data)
                        gp_keys.append(key)
                    result = []
                    for i in range(0, len(gp_keys), 2):
                        if i + 1 < len(gp_keys):
                            result.append([gp_keys[i], gp_keys[i + 1]])
                        else:
                            result.append([gp_keys[i]])
                    result.append([Button.inline(bot_text["cancel"], b'cancel')])
                    ask_gp = await conv.send_message(bot_text["select_gp"], buttons=result)
                    try:
                        gp_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                        await bot.delete_messages(user_id, ask_gp.id)
                    except TimeoutError:
                        await conv.send_message(bot_text["timeout_error"])
                        await bot.delete_messages(user_id, ask_gp.id)
                        return
                    gp_data = gp_res.data
                    if gp_data == b'cancel':
                        await conv.send_message(bot_text["canceled"])
                        await conv.cancel_all()
                    else:
                        gp_country = gp_data.decode().split(":")[0]
                        gp_round = int(gp_data.decode().split(":")[1])
                        sessions = manager.get_session(year=year, country=gp_round)["sessions"]
                        type_tr = {
                            "Sprint": "اسپرینت",
                            "Race": "مسابقه"
                        }
                        sessions_keys = []
                        for session in sessions:
                            if lang == 1:
                                session_text = session
                            else:
                                try:
                                    session_text = type_tr[session]
                                except KeyError:
                                    continue
                            session_key = [
                                Button.inline(session_text, session.encode()),
                            ]
                            sessions_keys.append(session_key)
                        ask_event = await event.reply(bot_text["select_session"], buttons=sessions_keys)
                        try:
                            session_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                            await bot.delete_messages(user_id, ask_event.id)
                        except TimeoutError:
                            await conv.send_message(bot_text["timeout_error"])
                            await bot.delete_messages(user_id, ask_event.id)
                            return
                        event_data = session_res.data
                        if event_data == b'cancel':
                            await conv.send_message(bot_text["canceled"])
                            await conv.cancel_all()
                        else:
                            session = event_data.decode()
                            if year == 2024:
                                # دریافت تاریخ مسابقه از API
                                check_date = f"https://ergast.com/api/f1/{year}.json"
                                check_date = requests.get(check_date).json()["MRData"]["RaceTable"]["Races"]

                                for grand in check_date:
                                    if grand["raceName"] == gp:
                                        now = datetime.now()
                                        now_date_str = f"{now.year}-{now.month:02d}-{now.day:02d}"
                                        now_time_str = now.strftime("%H:%M:%S")
                                        
                                        # ترکیب تاریخ و ساعت فعلی
                                        now_datetime_str = f"{now_date_str} {now_time_str}"
                                        now_datetime = datetime.strptime(now_datetime_str, "%Y-%m-%d %H:%M:%S")
                                        
                                        if session == "Race":
                                            race_date = grand["date"]
                                        elif session == "Sprint":
                                            race_date = grand["Sprint"]["date"]
                                        else:
                                            await conv.send_message(bot_text["action_not_found"])
                                            return
                                        if check_date_passed(race_date) is False:
                                            race_hour = cur.execute(f"SELECT time FROM grand_time WHERE grand = '{gp}' AND session_type = '{session}';").fetchone()
                                            if race_hour is None:
                                                await conv.send_message(bot_text["problem"])
                                                return
                                            race_hour = race_hour[0]
                                            # ترکیب تاریخ و ساعت مسابقه
                                            race_datetime_str = f"{race_date} {race_hour}"
                                            race_datetime = datetime.strptime(race_datetime_str, "%Y-%m-%d %H:%M:%S")
                                            
                                            if now_datetime < race_datetime:
                                                await conv.send_message(bot_text["dont_time"])
                                                return
                            url = f"http://ergast.com/api/f1/{year}/{gp_round}/drivers.json"
                            if config.ergast:
                                drivers = requests.get(url).json()["MRData"]["DriverTable"]["Drivers"]
                            else:
                                drivers = ergast_data["MRData"]["DriverTable"]["Drivers"]
                            drivers_keys = []
                            if config.ergast:
                                for driver in drivers:
                                    if lang == 1:
                                        driver_name = driver["givenName"] + driver["familyName"]
                                    else:
                                        driver_name = drivers_translate[driver["givenName"] + "_" + driver["familyName"]]
                                    driver_code = driver["code"]
                                    key = Button.inline(driver_name, data=driver_code.encode())
                                    drivers_keys.append(key)
                            else:
                                for driver in drivers:
                                    if lang == 1:
                                        driver_name = driver["givenName"] + driver["familyName"]
                                    else:
                                        driver_name = drivers_translate[driver["givenName"] + "_" + driver["familyName"]]
                                        driver_code = driver["code"]
                                        key = Button.inline(driver_name, data=driver_code.encode())
                                        drivers_keys.append(key)
                            result = []
                            for dv in range(0, len(drivers_keys), 2):
                                if dv + 1 < len(drivers_keys):
                                    result.append([drivers_keys[dv], drivers_keys[dv + 1]])
                                else:
                                    result.append([drivers_keys[dv]])
                            cancel_btn = [Button.inline(bot_text["cancel"], b'cancel')]
                            result.append(cancel_btn)
                            ask_driver = await conv.send_message(bot_text["ask_driver_one"], buttons=result)
                            try:
                                dr_event = await conv.wait_event(events.CallbackQuery(), timeout=60)
                                await bot.delete_messages(user_id, ask_driver.id)
                            except TimeoutError:
                                await conv.send_message(bot_text["timeout_error"])
                                await bot.delete_messages(user_id, ask_driver.id)
                                return
                            driver_data = dr_event.data
                            if driver_data == b'cancel':
                                await conv.send_message(bot_text["canceled"])
                                await conv.cancel_all()
                            else:
                                gp_round = int(gp_data.decode().split(":")[1])
                                url = f"http://ergast.com/api/f1/{year}/{gp_round}/drivers.json"
                                if config.ergast:
                                    drivers = requests.get(url).json()["MRData"]["DriverTable"]["Drivers"]
                                else:
                                    drivers = ergast_data["MRData"]["DriverTable"]["Drivers"]
                                drivers_keys = []
                                if config.ergast:
                                    for driver in drivers:
                                        if lang == 1:
                                            driver_name = driver["givenName"] + driver["familyName"]
                                        else:
                                            driver_name = drivers_translate[driver["givenName"] + "_" + driver["familyName"]]
                                        driver_code = driver["code"]
                                        key = Button.inline(driver_name, data=driver_code.encode())
                                        drivers_keys.append(key)
                                else:
                                    for driver in drivers:
                                        if lang == 1:
                                            driver_name = driver["givenName"] + driver["familyName"]
                                        else:
                                            driver_name = drivers_translate[driver["givenName"] + "_" + driver["familyName"]]
                                            driver_code = driver["code"]
                                            key = Button.inline(driver_name, data=driver_code.encode())
                                            drivers_keys.append(key)
                                result = []
                                for dv in range(0, len(drivers_keys), 2):
                                    if dv + 1 < len(drivers_keys):
                                        result.append([drivers_keys[dv], drivers_keys[dv + 1]])
                                    else:
                                        result.append([drivers_keys[dv]])
                                cancel_btn = [Button.inline(bot_text["cancel"], b'cancel')]
                                result.append(cancel_btn)
                                ask_driver = await conv.send_message(bot_text["ask_driver_two"], buttons=result)
                                try:
                                    dr_event = await conv.wait_event(events.CallbackQuery(), timeout=60)
                                    await bot.delete_messages(user_id, ask_driver.id)
                                except TimeoutError:
                                    await conv.send_message(bot_text["timeout_error"])
                                    await bot.delete_messages(user_id, ask_driver.id)
                                    return
                                driver_data_two = dr_event.data
                                if driver_data == b"cancel":
                                    await conv.send_message(bot_text["canceled"])
                                    await conv.cancel_all()
                                else:
                                    driver_one_code = driver_data.decode()
                                    driver_two_code = driver_data_two.decode()
                                    session = event_data.decode()
                                    if lang == 1:
                                        loading = await conv.send_message(bot_text["loading_two"].format(year=year, gp=gp_country, event=session, driver_one=driver_buy_code_en[driver_one_code], driver_two=driver_buy_code_en[driver_two_code]))
                                    else:
                                        loading = await conv.send_message(bot_text["loading_two"].format(year=year, gp=country_tr[gp_country.replace(" ", "_")], event=type_tr[session.replace(" ", "_")], driver_one=driver_buy_code_fa[driver_one_code], driver_two=driver_buy_code_fa[driver_two_code]))
                                    BASE_DIR = Path(__file__).resolve().parent
                                    if session == "Practice_1" or session == "Practice_2" or session == "Practice_3":
                                        session = sessions_convert[session]
                                    image_driver = f"{year}-{gp_round}-{session}-{driver_one_code}-{driver_two_code}_driver.png"
                                    image_base_driver = fr"{BASE_DIR}/{image_driver}"
                                    if os.path.exists(image_base_driver) is False:
                                        image_driver_path = driver_func_data(year, gp_round, session, driver_one_code, driver_two_code)
                                    await bot.delete_messages(user_id, loading.id)
                                    await bot.send_file(user_id, caption="Driver", file=image_base_driver)
                                    await bot.send_file(user_id, caption="Driver", file=image_base_driver, force_document=True)
                                    config.all_statistics(event.message.message, user_id)
                                    config.small_statistics(event.message.message, user_id)
                                    await conv.cancel_all()
        elif text == bot_text["data_to_pole"]:
            find_status = cur.execute(f"SELECT status FROM data_status WHERE data = '{event.message.message}'").fetchone()
            if find_status[0] == 'off' or find_status[0] is None:
                await event.reply(bot_text["data_is_off"])
                return
            user_find = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
            user_scores = user_find[5]
            user_level = user_find[10]
            score_dict = {
                "1": 1,
                "2": 0,
                "3": 0,
            }
            score_get = score_dict[f"{user_level}"]
            if user_scores - score_get < 0:
                key = [
                    Button.inline(bot_text["account"], data=b'user_account')
                ]
                await event.reply(bot_text["coin_not_enough"].format(score=user_scores), buttons=key)
                return
            async with bot.conversation(user_id) as conv:
                year_keys = [
                    [
                        Button.inline("2024", b'2024')
                    ],
                    [
                        Button.inline("2023", b'2023')
                    ],
                    [
                        Button.inline("2022", b'2022')
                    ],
                    [
                        Button.inline("2021", b'2021')
                    ],
                    [
                        Button.inline("2020", b'2020')
                    ],
                    [
                        Button.inline("2019", b'2019')
                    ],
                    [
                        Button.inline("2018", b'2018')
                    ],
                    [
                        Button.inline(bot_text["cancel"], b'cancel')
                    ]
                ]
                ask_year = await conv.send_message(bot_text["select_year"], buttons=year_keys)
                try:
                    year_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                    await bot.delete_messages(user_id, ask_year.id)
                except TimeoutError:
                    await conv.send_message(bot_text["timeout_error"])
                    await bot.delete_messages(user_id, ask_year.id)
                    return
                year_data = year_res.data
                if year_data == b'cancel':
                    await conv.send_message(bot_text["canceled"])
                    await bot.delete_messages(user_id, ask_year.id)
                    await conv.cancel_all()
                else: 
                    year = int(year_data)
                    response = manager.get_event(year=year)["Country"]
                    gp_keys = []
                    for gp in response:
                        if lang == 1:
                            gp_text = gp["t"]
                        else:
                            gp_text = country_tr[gp["tr"]]
                        gp_data = gp["t"].encode()
                        key = Button.inline(gp_text, data=gp_data)
                        gp_keys.append(key)
                    result = []
                    for i in range(0, len(gp_keys), 2):
                        if i + 1 < len(gp_keys):
                            result.append([gp_keys[i], gp_keys[i + 1]])
                        else:
                            result.append([gp_keys[i]])
                    result.append([Button.inline(bot_text["cancel"], b'cancel')])
                    ask_gp = await conv.send_message(bot_text["select_gp"], buttons=result)
                    try:
                        gp_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                        await bot.delete_messages(user_id, ask_gp.id)
                    except TimeoutError:
                        await conv.send_message(bot_text["timeout_error"])
                        await bot.delete_messages(user_id, ask_gp.id)
                        return
                    gp_data = gp_res.data
                    if gp_data == b'cancel':
                        await conv.send_message(bot_text["canceled"])
                        await conv.cancel_all()
                    else:
                        gp = gp_data.decode()        
                        session = "Q"
                        if year == 2024:
                            # دریافت تاریخ مسابقه از API
                            check_date = f"https://ergast.com/api/f1/{year}.json"
                            check_date = requests.get(check_date).json()["MRData"]["RaceTable"]["Races"]

                            for grand in check_date:
                                if grand["raceName"] == gp:
                                    now = datetime.now()
                                    now_date_str = f"{now.year}-{now.month:02d}-{now.day:02d}"
                                    now_time_str = now.strftime("%H:%M:%S")
                                    
                                    # ترکیب تاریخ و ساعت فعلی
                                    now_datetime_str = f"{now_date_str} {now_time_str}"
                                    now_datetime = datetime.strptime(now_datetime_str, "%Y-%m-%d %H:%M:%S")
                                    
                                    if session == "Race":
                                        race_date = grand["date"]
                                    elif session == "Sprint":
                                        race_date = grand["Sprint"]["date"]
                                    elif session == "Practice_1":
                                        race_date = grand["FirstPractice"]["date"]
                                    elif session == "Practice_2":
                                        race_date = grand["SecondPractice"]["date"]
                                    elif session == "Practice_3":
                                        race_date = grand["ThirdPractice"]["date"]
                                    elif session == "Q":
                                        race_date = grand["Qualifying"]["date"]
                                    else:
                                        await conv.send_message(bot_text["action_not_found"])
                                        return
                                    if check_date_passed(race_date) is False:
                                        race_hour = cur.execute(f"SELECT time FROM grand_time WHERE grand = '{gp}' AND session_type = '{session}';").fetchone()
                                        if race_hour is None:
                                            await conv.send_message(bot_text["problem"])
                                            return
                                        race_hour = race_hour[0]
                                        # ترکیب تاریخ و ساعت مسابقه
                                        race_datetime_str = f"{race_date} {race_hour}"
                                        race_datetime = datetime.strptime(race_datetime_str, "%Y-%m-%d %H:%M:%S")
                                        
                                        if now_datetime < race_datetime:
                                            await conv.send_message(bot_text["dont_time"])
                                            return
                        if lang == 1:
                            loading = await conv.send_message(bot_text["loading"].format(year=year, gp=gp, event=session))
                        else:
                            loading = await conv.send_message(bot_text["loading"].format(year=year, gp=country_tr[gp.replace(" ", "_")], event="تعیین خط"))
                        BASE_DIR = Path(__file__).resolve().parent
                        if session == "Practice_1" or session == "Practice_2" or session == "Practice_3":
                            session = sessions_convert[session]
                        image_pole = f"{year}-{gp}-Q-delta_to_pole.png"
                        image_base_pole = fr"{BASE_DIR}/{image_pole}"
                        if os.path.exists(image_base_pole) is False:
                            pole_path = create_image(year, gp)
                        await bot.delete_messages(user_id, loading.id)
                        await bot.send_file(user_id, caption="Delta To Pole", file=image_base_pole)
                        await bot.send_file(user_id, caption="Delta To Pole", file=image_base_pole, force_document=True)
                        user_level_fa = {
                            "1": "برنزی",
                            "2": "نقره ای",
                            "3": "طلایی"
                        }
                        if user_level == "1":
                            user_score = user_find[5]
                            user_score -= 1
                            cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                            con.commit()
                            await event.reply(bot_text["score_data"].format(coin=1, level=user_level_fa))
                        config.all_statistics(event.message.message, user_id)
                        config.small_statistics(event.message.message, user_id)
                        await conv.cancel_all()
        elif text == bot_text["lap_times_table"]:
            find_status = cur.execute(f"SELECT status FROM data_status WHERE data = '{event.message.message}'").fetchone()
            if find_status[0] == 'off' or find_status[0] is None:
                await event.reply(bot_text["data_is_off"])
                return
            user_find = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
            user_scores = user_find[5]
            user_level = user_find[10]
            score_dict = {
                "1": 3,
                "2": 2,
                "3": 1,
            }
            score_get = score_dict[f"{user_level}"]
            if user_scores - score_get < 0:
                key = [
                    Button.inline(bot_text["account"], data=b'user_account')
                ]
                await event.reply(bot_text["coin_not_enough"].format(score=user_scores), buttons=key)
                return
            async with bot.conversation(user_id) as conv:
                year_keys = [
                    [
                        Button.inline("2024", b'2024')
                    ],
                    [
                        Button.inline("2023", b'2023')
                    ],
                    [
                        Button.inline("2022", b'2022')
                    ],
                    [
                        Button.inline("2021", b'2021')
                    ],
                    [
                        Button.inline("2020", b'2020')
                    ],
                    [
                        Button.inline("2019", b'2019')
                    ],
                    [
                        Button.inline("2018", b'2018')
                    ],
                    [
                        Button.inline(bot_text["cancel"], b'cancel')
                    ]
                ]
                ask_year = await conv.send_message(bot_text["select_year"], buttons=year_keys)
                try:
                    year_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                    await bot.delete_messages(user_id, ask_year.id)
                except TimeoutError:
                    await conv.send_message(bot_text["timeout_error"])
                    await bot.delete_messages(user_id, ask_year.id)
                    return
                year_data = year_res.data
                if year_data == b'cancel':
                    await conv.send_message(bot_text["canceled"])
                    await bot.delete_messages(user_id, ask_year.id)
                    await conv.cancel_all()
                else: 
                    year = int(year_data)
                    response = manager.get_event(year=year)["Country"]
                    gp_keys = []
                    for gp in response:
                        if lang == 1:
                            gp_text = gp["t"]
                        else:
                            gp_text = country_tr[gp["tr"]]
                        gp_data = str.encode(gp["t"] + ":" + str(gp["round_num"]))
                        key = Button.inline(gp_text, data=gp_data)
                        gp_keys.append(key)
                    result = []
                    for i in range(0, len(gp_keys), 2):
                        if i + 1 < len(gp_keys):
                            result.append([gp_keys[i], gp_keys[i + 1]])
                        else:
                            result.append([gp_keys[i]])
                    result.append([Button.inline(bot_text["cancel"], b'cancel')])
                    ask_gp = await conv.send_message(bot_text["select_gp"], buttons=result)
                    try:
                        gp_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                        await bot.delete_messages(user_id, ask_gp.id)
                    except TimeoutError:
                        await conv.send_message(bot_text["timeout_error"])
                        await bot.delete_messages(user_id, ask_gp.id)
                        return
                    gp_data = gp_res.data
                    if gp_data == b'cancel':
                        await conv.send_message(bot_text["canceled"])
                        await conv.cancel_all()
                    else:
                        gp_country = gp_data.decode().split(":")[0]
                        gp_round = int(gp_data.decode().split(":")[1])
                        sessions = manager.get_session(year=year, country=gp_round)["sessions"]
                        type_tr = {
                            "Practice_1": "تمرین اول",
                            "Practice_2": "تمرین دوم",
                            "Practice_3": "تمرین سوم",
                            "Sprint": "اسپرینت",
                            "Sprint_Shootout": "اسپرینت شوت آوت",
                            "Sprint_Qualifying": "تعیین خط اسپرینت",
                            "Race": "مسابقه"
                        }
                        sessions_keys = []
                        for session in sessions:
                            if session == "Qualifying":
                                continue
                            if lang == 1:
                                session_text = session
                            else:
                                session_text = type_tr[session]
                            session_key = [
                                Button.inline(session_text, session.encode()),
                            ]
                            sessions_keys.append(session_key)
                        ask_event = await event.reply(bot_text["select_session"], buttons=sessions_keys)
                        try:
                            session_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                            await bot.delete_messages(user_id, ask_event.id)
                        except TimeoutError:
                            await conv.send_message(bot_text["timeout_error"])
                            await bot.delete_messages(user_id, ask_event.id)
                            return
                        event_data = session_res.data
                        if event_data == b'cancel':
                            await conv.send_message(bot_text["canceled"])
                            await conv.cancel_all()
                        else:
                            session = event_data.decode()
                            if year == 2024:
                                # دریافت تاریخ مسابقه از API
                                check_date = f"https://ergast.com/api/f1/{year}.json"
                                check_date = requests.get(check_date).json()["MRData"]["RaceTable"]["Races"]

                                for grand in check_date:
                                    if grand["raceName"] == gp:
                                        now = datetime.now()
                                        now_date_str = f"{now.year}-{now.month:02d}-{now.day:02d}"
                                        now_time_str = now.strftime("%H:%M:%S")
                                        
                                        # ترکیب تاریخ و ساعت فعلی
                                        now_datetime_str = f"{now_date_str} {now_time_str}"
                                        now_datetime = datetime.strptime(now_datetime_str, "%Y-%m-%d %H:%M:%S")
                                        
                                        if session == "Race":
                                            race_date = grand["date"]
                                        elif session == "Sprint":
                                            race_date = grand["Sprint"]["date"]
                                        elif session == "Practice_1":
                                            race_date = grand["FirstPractice"]["date"]
                                        elif session == "Practice_2":
                                            race_date = grand["SecondPractice"]["date"]
                                        elif session == "Practice_3":
                                            race_date = grand["ThirdPractice"]["date"]
                                        elif session == "Qualifying":
                                            race_date = grand["Qualifying"]["date"]
                                        else:
                                            await conv.send_message(bot_text["action_not_found"])
                                            return
                                        if check_date_passed(race_date) is False:
                                            race_hour = cur.execute(f"SELECT time FROM grand_time WHERE grand = '{gp}' AND session_type = '{session}';").fetchone()
                                            if race_hour is None:
                                                await conv.send_message(bot_text["problem"])
                                                return
                                            race_hour = race_hour[0]
                                            # ترکیب تاریخ و ساعت مسابقه
                                            race_datetime_str = f"{race_date} {race_hour}"
                                            race_datetime = datetime.strptime(race_datetime_str, "%Y-%m-%d %H:%M:%S")
                                            
                                            if now_datetime < race_datetime:
                                                await conv.send_message(bot_text["dont_time"])
                                                return
                            url = f"http://ergast.com/api/f1/{year}/{gp_round}/drivers.json"
                            if config.ergast:
                                drivers = requests.get(url).json()["MRData"]["DriverTable"]["Drivers"]
                            else:
                                drivers = ergast_data["MRData"]["DriverTable"]["Drivers"]
                            drivers_keys = []
                            if config.ergast:
                                for driver in drivers:
                                    if lang == 1:
                                        driver_name = driver["givenName"] + driver["familyName"]
                                    else:
                                        driver_name = drivers_translate[driver["givenName"] + "_" + driver["familyName"]]
                                    driver_code = driver["code"]
                                    key = Button.inline(driver_name, data=driver_code.encode())
                                    drivers_keys.append(key)
                            else:
                                for driver in drivers:
                                    if lang == 1:
                                        driver_name = driver["givenName"] + driver["familyName"]
                                    else:
                                        driver_name = drivers_translate[driver["givenName"] + "_" + driver["familyName"]]
                                        driver_code = driver["code"]
                                        key = Button.inline(driver_name, data=driver_code.encode())
                                        drivers_keys.append(key)
                            result = []
                            for dv in range(0, len(drivers_keys), 2):
                                if dv + 1 < len(drivers_keys):
                                    result.append([drivers_keys[dv], drivers_keys[dv + 1]])
                                else:
                                    result.append([drivers_keys[dv]])
                            cancel_btn = [Button.inline(bot_text["cancel"], b'cancel')]
                            result.append(cancel_btn)
                            ask_driver = await conv.send_message(bot_text["ask_driver"], buttons=result)
                            try:
                                dr_event = await conv.wait_event(events.CallbackQuery(), timeout=60)
                                await bot.delete_messages(user_id, ask_driver.id)
                            except TimeoutError:
                                await conv.send_message(bot_text["timeout_error"])
                                await bot.delete_messages(user_id, ask_driver.id)
                                return
                            driver_data = dr_event.data
                            if driver_data == b'cancel':
                                await conv.send_message(bot_text["canceled"])
                                await conv.cancel_all()
                            else:
                                driver_code = driver_data.decode()
                                session = event_data.decode()
                                if lang == 1:
                                    loading = await conv.send_message(bot_text["loading_one"].format(year=year, gp=gp_country, event=session, driver_one=driver_buy_code_en[driver_code]))
                                else:
                                    loading = await conv.send_message(bot_text["loading_one"].format(year=year, gp=country_tr[gp_country.replace(" ", "_")], event=type_tr[session.replace(" ", "_")], driver_one=driver_buy_code_fa[driver_code]))
                                if session == "Practice_1" or session == "Practice_2" or session == "Practice_3":
                                    session = sessions_convert[session]
                                images = show_driver_lap_times([driver_code], year, gp_country, session)
                                await bot.delete_messages(user_id, loading.id)
                                await bot.send_file(user_id, caption="Lap Times Table", file=images)
                                await bot.send_file(user_id, caption="Lap Times Table", file=images, force_document=True)
                                config.all_statistics(event.message.message, user_id)
                                config.small_statistics(event.message.message, user_id)
                                user_find = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
                                user_level = user_find[10]
                                level_dict = {
                                    "1": bot_text["level_one"],
                                    "2": bot_text["level_two"],
                                    "3": bot_text["level_three"],
                                }
                                user_level_fa = level_dict[f"{user_level}"]
                                if user_level == "1":
                                    user_score = user_find[5]
                                    user_score -= 3
                                    cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                    con.commit()
                                    await event.reply(bot_text["score_data"].format(coin=3, level=user_level_fa))
                                elif user_level == "2":
                                    user_score = user_find[5]
                                    user_score -= 2
                                    cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                    con.commit()
                                    await event.reply(bot_text["score_data"].format(coin=2, level=user_level_fa))
                                elif user_level == "3":
                                    user_score = user_find[5]
                                    user_score -= 1
                                    cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                    con.commit()
                                    await event.reply(bot_text["score_data"].format(coin=1, level=user_level_fa))
                                await conv.cancel_all()
        elif text == bot_text["brake_configurations"]:
            find_status = cur.execute(f"SELECT status FROM data_status WHERE data = '{event.message.message}'").fetchone()
            if find_status[0] == 'off' or find_status[0] is None:
                await event.reply(bot_text["data_is_off"])
                return
            user_find = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
            user_scores = user_find[5]
            user_level = user_find[10]
            score_dict = {
                "1": 3,
                "2": 2,
                "3": 1,
            }
            score_get = score_dict[f"{user_level}"]
            if user_scores - score_get < 0:
                key = [
                    Button.inline(bot_text["account"], data=b'user_account')
                ]
                await event.reply(bot_text["coin_not_enough"].format(score=user_scores), buttons=key)
                return
            async with bot.conversation(user_id) as conv:
                year_keys = [
                    [
                        Button.inline("2024", b'2024')
                    ],
                    [
                        Button.inline("2023", b'2023')
                    ],
                    [
                        Button.inline("2022", b'2022')
                    ],
                    [
                        Button.inline("2021", b'2021')
                    ],
                    [
                        Button.inline("2020", b'2020')
                    ],
                    [
                        Button.inline("2019", b'2019')
                    ],
                    [
                        Button.inline("2018", b'2018')
                    ],
                    [
                        Button.inline(bot_text["cancel"], b'cancel')
                    ]
                ]
                ask_year = await conv.send_message(bot_text["select_year"], buttons=year_keys)
                try:
                    year_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                    await bot.delete_messages(user_id, ask_year.id)
                except TimeoutError:
                    await conv.send_message(bot_text["timeout_error"])
                    await bot.delete_messages(user_id, ask_year.id)
                    return
                year_data = year_res.data
                if year_data == b'cancel':
                    await conv.send_message(bot_text["canceled"])
                    await bot.delete_messages(user_id, ask_year.id)
                    await conv.cancel_all()
                else: 
                    year = int(year_data)
                    response = manager.get_event(year=year)["Country"]
                    gp_keys = []
                    for gp in response:
                        if lang == 1:
                            gp_text = gp["t"]
                        else:
                            gp_text = country_tr[gp["tr"]]
                        gp_data = gp["t"].encode()
                        key = Button.inline(gp_text, data=gp_data)
                        gp_keys.append(key)
                    result = []
                    for i in range(0, len(gp_keys), 2):
                        if i + 1 < len(gp_keys):
                            result.append([gp_keys[i], gp_keys[i + 1]])
                        else:
                            result.append([gp_keys[i]])
                    result.append([Button.inline(bot_text["cancel"], b'cancel')])
                    ask_gp = await conv.send_message(bot_text["select_gp"], buttons=result)
                    try:
                        gp_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                        await bot.delete_messages(user_id, ask_gp.id)
                    except TimeoutError:
                        await conv.send_message(bot_text["timeout_error"])
                        await bot.delete_messages(user_id, ask_gp.id)
                        return
                    gp_data = gp_res.data
                    if gp_data == b'cancel':
                        await conv.send_message(bot_text["canceled"])
                        await conv.cancel_all()
                    else:
                        gp = gp_data.decode()        
                        # url = f"https://f1datas.com/api/v1/fastf1/session?year={year}&country={gp}"
                        sessions = manager.get_session(year=year, country=gp)["sessions"]
                        # sessions = requests.get(url).json()["sessions"]
                        type_tr = {
                            "Practice_1": "تمرین اول",
                            "Practice_2": "تمرین دوم",
                            "Practice_3": "تمرین سوم",
                            "Sprint": "اسپرینت",
                            "Sprint_Shootout": "اسپرینت شوت آوت",
                            "Sprint_Qualifying": "تعیین خط اسپرینت",
                            "Qualifying": "تعیین خط",
                            "Race": "مسابقه"
                        }
                        sessions_keys = []
                        for session in sessions:
                            if lang == 1:
                                session_text = session
                            else:
                                session_text = type_tr[session]
                            session_key = [
                                Button.inline(session_text, session.encode()),
                            ]
                            sessions_keys.append(session_key)
                        ask_event = await event.reply(bot_text["select_session"], buttons=sessions_keys)
                        try:
                            session_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                            await bot.delete_messages(user_id, ask_event.id)
                        except TimeoutError:
                            await conv.send_message(bot_text["timeout_error"])
                            await bot.delete_messages(user_id, ask_event.id)
                            return
                        event_data = session_res.data
                        if event_data == b'cancel':
                            await conv.send_message(bot_text["canceled"])
                            await conv.cancel_all()
                        else:
                            session = event_data.decode()
                            if year == 2024:
                                # دریافت تاریخ مسابقه از API
                                check_date = f"https://ergast.com/api/f1/{year}.json"
                                check_date = requests.get(check_date).json()["MRData"]["RaceTable"]["Races"]

                                for grand in check_date:
                                    if grand["raceName"] == gp:
                                        now = datetime.now()
                                        now_date_str = f"{now.year}-{now.month:02d}-{now.day:02d}"
                                        now_time_str = now.strftime("%H:%M:%S")
                                        
                                        # ترکیب تاریخ و ساعت فعلی
                                        now_datetime_str = f"{now_date_str} {now_time_str}"
                                        now_datetime = datetime.strptime(now_datetime_str, "%Y-%m-%d %H:%M:%S")
                                        
                                        if session == "Race":
                                            race_date = grand["date"]
                                        elif session == "Sprint":
                                            race_date = grand["Sprint"]["date"]
                                        elif session == "Practice_1":
                                            race_date = grand["FirstPractice"]["date"]
                                        elif session == "Practice_2":
                                            race_date = grand["SecondPractice"]["date"]
                                        elif session == "Practice_3":
                                            race_date = grand["ThirdPractice"]["date"]
                                        elif session == "Qualifying":
                                            race_date = grand["Qualifying"]["date"]
                                        else:
                                            await conv.send_message(bot_text["action_not_found"])
                                            return
                                        if check_date_passed(race_date) is False:
                                            race_hour = cur.execute(f"SELECT time FROM grand_time WHERE grand = '{gp}' AND session_type = '{session}';").fetchone()
                                            if race_hour is None:
                                                print("race hour", race_hour)
                                                print("session and grand", gp, session)
                                                print("check date", check_date_passed(race_date))
                                                await conv.send_message(bot_text["problem"])
                                                return
                                            race_hour = race_hour[0]
                                            # ترکیب تاریخ و ساعت مسابقه
                                            race_datetime_str = f"{race_date} {race_hour}"
                                            race_datetime = datetime.strptime(race_datetime_str, "%Y-%m-%d %H:%M:%S")
                                            
                                            if now_datetime < race_datetime:
                                                await conv.send_message(bot_text["dont_time"])
                                                return
                            if lang == 1:
                                loading = await conv.send_message(bot_text["loading"].format(year=year, gp=gp, event=session))
                            else:
                                loading = await conv.send_message(bot_text["loading"].format(year=year, gp=country_tr[gp.replace(" ", "_")], event=type_tr[session.replace(" ", "_")]))
                            BASE_DIR = Path(__file__).resolve().parent
                            if session == "Practice_1" or session == "Practice_2" or session == "Practice_3":
                                session = sessions_convert[session]
                            image_brake = f"{year}-{gp}-{session}-brake_configurations.png"
                            image_brake_base = fr"{BASE_DIR}/{image_brake}"
                            if os.path.exists(image_brake_base) is False:
                                lap_times_path = brake_configurations(year, gp, session)
                            await bot.delete_messages(user_id, loading.id)
                            await bot.send_file(user_id, caption="Brake Configurations", file=image_brake_base)
                            await bot.send_file(user_id, caption="Brake Configurations", file=image_brake_base, force_document=True)
                            config.all_statistics(event.message.message, user_id)
                            config.small_statistics(event.message.message, user_id)
                            user_find = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
                            user_level = user_find[10]
                            level_dict = {
                                "1": bot_text["level_one"],
                                "2": bot_text["level_two"],
                                "3": bot_text["level_three"],
                            }
                            user_level_fa = level_dict[f"{user_level}"]
                            if user_level == "1":
                                user_score = user_find[5]
                                user_score -= 3
                                cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                con.commit()
                                await event.reply(bot_text["score_data"].format(coin=3, level=user_level_fa))
                            elif user_level == "2":
                                user_score = user_find[5]
                                user_score -= 2
                                cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                con.commit()
                                await event.reply(bot_text["score_data"].format(coin=2, level=user_level_fa))
                            elif user_level == "3":
                                user_score = user_find[5]
                                user_score -= 1
                                cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                con.commit()
                                await event.reply(bot_text["score_data"].format(coin=1, level=user_level_fa))

                            await conv.cancel_all()
        elif text == bot_text["composite_perfomance"]:
            find_status = cur.execute(f"SELECT status FROM data_status WHERE data = '{event.message.message}'").fetchone()
            if find_status[0] == 'off' or find_status[0] is None:
                await event.reply(bot_text["data_is_off"])
                return
            user_find = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
            user_scores = user_find[5]
            user_level = user_find[10]
            score_dict = {
                "1": 2,
                "2": 1,
                "3": 1,
            }
            score_get = score_dict[f"{user_level}"]
            if user_scores - score_get < 0:
                key = [
                    Button.inline(bot_text["account"], data=b'user_account')
                ]
                await event.reply(bot_text["coin_not_enough"].format(score=user_scores), buttons=key)
                return
            async with bot.conversation(user_id) as conv:
                year_keys = [
                    [
                        Button.inline("2024", b'2024')
                    ],
                    [
                        Button.inline("2023", b'2023')
                    ],
                    [
                        Button.inline("2022", b'2022')
                    ],
                    [
                        Button.inline("2021", b'2021')
                    ],
                    [
                        Button.inline("2020", b'2020')
                    ],
                    [
                        Button.inline("2019", b'2019')
                    ],
                    [
                        Button.inline("2018", b'2018')
                    ],
                    [
                        Button.inline(bot_text["cancel"], b'cancel')
                    ]
                ]
                ask_year = await conv.send_message(bot_text["select_year"], buttons=year_keys)
                try:
                    year_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                    await bot.delete_messages(user_id, ask_year.id)
                except TimeoutError:
                    await conv.send_message(bot_text["timeout_error"])
                    await bot.delete_messages(user_id, ask_year.id)
                    return
                year_data = year_res.data
                if year_data == b'cancel':
                    await conv.send_message(bot_text["canceled"])
                    await bot.delete_messages(user_id, ask_year.id)
                    await conv.cancel_all()
                else: 
                    year = int(year_data)
                    response = manager.get_event(year=year)["Country"]
                    gp_keys = []
                    for gp in response:
                        if lang == 1:
                            gp_text = gp["t"]
                        else:
                            gp_text = country_tr[gp["tr"]]
                        gp_data = gp["t"].encode()
                        key = Button.inline(gp_text, data=gp_data)
                        gp_keys.append(key)
                    result = []
                    for i in range(0, len(gp_keys), 2):
                        if i + 1 < len(gp_keys):
                            result.append([gp_keys[i], gp_keys[i + 1]])
                        else:
                            result.append([gp_keys[i]])
                    result.append([Button.inline(bot_text["cancel"], b'cancel')])
                    ask_gp = await conv.send_message(bot_text["select_gp"], buttons=result)
                    try:
                        gp_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                        await bot.delete_messages(user_id, ask_gp.id)
                    except TimeoutError:
                        await conv.send_message(bot_text["timeout_error"])
                        await bot.delete_messages(user_id, ask_gp.id)
                        return
                    gp_data = gp_res.data
                    if gp_data == b'cancel':
                        await conv.send_message(bot_text["canceled"])
                        await conv.cancel_all()
                    else:
                        gp = gp_data.decode()        
                        # url = f"https://f1datas.com/api/v1/fastf1/session?year={year}&country={gp}"
                        sessions = manager.get_session(year=year, country=gp)["sessions"]
                        # sessions = requests.get(url).json()["sessions"]
                        type_tr = {
                            "Practice_1": "تمرین اول",
                            "Practice_2": "تمرین دوم",
                            "Practice_3": "تمرین سوم",
                            "Sprint": "اسپرینت",
                            "Sprint_Shootout": "اسپرینت شوت آوت",
                            "Sprint_Qualifying": "تعیین خط اسپرینت",
                            "Qualifying": "تعیین خط",
                            "Race": "مسابقه"
                        }
                        sessions_keys = []
                        for session in sessions:
                            if lang == 1:
                                session_text = session
                            else:
                                session_text = type_tr[session]
                            session_key = [
                                Button.inline(session_text, session.encode()),
                            ]
                            sessions_keys.append(session_key)
                        ask_event = await event.reply(bot_text["select_session"], buttons=sessions_keys)
                        try:
                            session_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                            await bot.delete_messages(user_id, ask_event.id)
                        except TimeoutError:
                            await conv.send_message(bot_text["timeout_error"])
                            await bot.delete_messages(user_id, ask_event.id)
                            return
                        event_data = session_res.data
                        if event_data == b'cancel':
                            await conv.send_message(bot_text["canceled"])
                            await conv.cancel_all()
                        else:
                            session = event_data.decode()
                            if year == 2024:
                                # دریافت تاریخ مسابقه از API
                                check_date = f"https://ergast.com/api/f1/{year}.json"
                                check_date = requests.get(check_date).json()["MRData"]["RaceTable"]["Races"]

                                for grand in check_date:
                                    if grand["raceName"] == gp:
                                        now = datetime.now()
                                        now_date_str = f"{now.year}-{now.month:02d}-{now.day:02d}"
                                        now_time_str = now.strftime("%H:%M:%S")
                                        
                                        # ترکیب تاریخ و ساعت فعلی
                                        now_datetime_str = f"{now_date_str} {now_time_str}"
                                        now_datetime = datetime.strptime(now_datetime_str, "%Y-%m-%d %H:%M:%S")
                                        
                                        if session == "Race":
                                            race_date = grand["date"]
                                        elif session == "Sprint":
                                            race_date = grand["Sprint"]["date"]
                                        elif session == "Practice_1":
                                            race_date = grand["FirstPractice"]["date"]
                                        elif session == "Practice_2":
                                            race_date = grand["SecondPractice"]["date"]
                                        elif session == "Practice_3":
                                            race_date = grand["ThirdPractice"]["date"]
                                        elif session == "Qualifying":
                                            race_date = grand["Qualifying"]["date"]
                                        else:
                                            await conv.send_message(bot_text["action_not_found"])
                                            return
                                        if check_date_passed(race_date) is False:
                                            race_hour = cur.execute(f"SELECT time FROM grand_time WHERE grand = '{gp}' AND session_type = '{session}';").fetchone()
                                            if race_hour is None:
                                                print("race hour", race_hour)
                                                print("session and grand", gp, session)
                                                print("check date", check_date_passed(race_date))
                                                await conv.send_message(bot_text["problem"])
                                                return
                                            race_hour = race_hour[0]
                                            # ترکیب تاریخ و ساعت مسابقه
                                            race_datetime_str = f"{race_date} {race_hour}"
                                            race_datetime = datetime.strptime(race_datetime_str, "%Y-%m-%d %H:%M:%S")
                                            
                                            if now_datetime < race_datetime:
                                                await conv.send_message(bot_text["dont_time"])
                                                return
                            if lang == 1:
                                loading = await conv.send_message(bot_text["loading"].format(year=year, gp=gp, event=session))
                            else:
                                loading = await conv.send_message(bot_text["loading"].format(year=year, gp=country_tr[gp.replace(" ", "_")], event=type_tr[session.replace(" ", "_")]))
                            BASE_DIR = Path(__file__).resolve().parent
                            if session == "Practice_1" or session == "Practice_2" or session == "Practice_3":
                                session = sessions_convert[session]
                            image_performance = f"{year}-{gp}-{session}-composite_perfomance.png"
                            image_base_performance = fr"{BASE_DIR}/{image_performance}"
                            if os.path.exists(image_base_performance) is False:
                                lap_times_path = composite_perfomance(year, gp, session)
                            await bot.delete_messages(user_id, loading.id)
                            await bot.send_file(user_id, caption="Composite Perfomance", file=image_base_performance)
                            await bot.send_file(user_id, caption="Composite Perfomance", file=image_base_performance, force_document=True)
                            config.all_statistics(event.message.message, user_id)
                            config.small_statistics(event.message.message, user_id)
                            user_find = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
                            user_level = user_find[10]
                            level_dict = {
                                "1": bot_text["level_one"],
                                "2": bot_text["level_two"],
                                "3": bot_text["level_three"],
                            }
                            user_level_fa = level_dict[f"{user_level}"]
                            if user_level == "1":
                                user_score = user_find[5]
                                user_score -= 2
                                cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                con.commit()
                                await event.reply(bot_text["score_data"].format(coin=2, level=user_level_fa))
                            elif user_level == "2":
                                user_score = user_find[5]
                                user_score -= 1
                                cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                con.commit()
                                await event.reply(bot_text["score_data"].format(coin=1, level=user_level_fa))
                            elif user_level == "3":
                                user_score = user_find[5]
                                user_score -= 1
                                cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                con.commit()
                                await event.reply(bot_text["score_data"].format(coin=1, level=user_level_fa))

                            await conv.cancel_all()
        elif text == bot_text["degradation_tyre"]:
            find_status = cur.execute(
                f"SELECT status FROM data_status WHERE data = '{event.message.message}'").fetchone()
            if find_status[0] == 'off' or find_status[0] is None:
                await event.reply(bot_text["data_is_off"])
                return
            user_find = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
            user_scores = user_find[5]
            user_level = user_find[10]
            score_dict = {
                "1": 3,
                "2": 3,
                "3": 2,
            }
            score_get = score_dict[f"{user_level}"]
            if user_scores - score_get < 0:
                key = [
                    Button.inline(bot_text["account"], data=b'user_account')
                ]
                await event.reply(bot_text["coin_not_enough"].format(score=user_scores), buttons=key)
                return
            async with bot.conversation(user_id) as conv:
                year_keys = [
                    [
                        Button.inline("2024", b'2024')
                    ],
                    [
                        Button.inline("2023", b'2023')
                    ],
                    [
                        Button.inline("2022", b'2022')
                    ],
                    [
                        Button.inline("2021", b'2021')
                    ],
                    [
                        Button.inline("2020", b'2020')
                    ],
                    [
                        Button.inline("2019", b'2019')
                    ],
                    [
                        Button.inline("2018", b'2018')
                    ],
                    [
                        Button.inline(bot_text["cancel"], b'cancel')
                    ]
                ]
                ask_year = await conv.send_message(bot_text["select_year"], buttons=year_keys)
                try:
                    year_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                    await bot.delete_messages(user_id, ask_year.id)
                except TimeoutError:
                    await conv.send_message(bot_text["timeout_error"])
                    await bot.delete_messages(user_id, ask_year.id)
                    return
                year_data = year_res.data
                if year_data == b'cancel':
                    await conv.send_message(bot_text["canceled"])
                    await bot.delete_messages(user_id, ask_year.id)
                    await conv.cancel_all()
                else:
                    year = int(year_data)
                    response = manager.get_event(year=year)["Country"]
                    gp_keys = []
                    for gp in response:
                        if lang == 1:
                            gp_text = gp["t"]
                        else:
                            gp_text = country_tr[gp["tr"]]
                        gp_data = gp["t"].encode()
                        key = Button.inline(gp_text, data=gp_data)
                        gp_keys.append(key)
                    result = []
                    for i in range(0, len(gp_keys), 2):
                        if i + 1 < len(gp_keys):
                            result.append([gp_keys[i], gp_keys[i + 1]])
                        else:
                            result.append([gp_keys[i]])
                    result.append([Button.inline(bot_text["cancel"], b'cancel')])
                    ask_gp = await conv.send_message(bot_text["select_gp"], buttons=result)
                    try:
                        gp_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                        await bot.delete_messages(user_id, ask_gp.id)
                    except TimeoutError:
                        await conv.send_message(bot_text["timeout_error"])
                        await bot.delete_messages(user_id, ask_gp.id)
                        return
                    gp_data = gp_res.data
                    if gp_data == b'cancel':
                        await conv.send_message(bot_text["canceled"])
                        await conv.cancel_all()
                    else:
                        gp = gp_data.decode()
                        # url = f"https://f1datas.com/api/v1/fastf1/session?year={year}&country={gp}"
                        sessions = manager.get_session(year=year, country=gp)["sessions"]
                        # sessions = requests.get(url).json()["sessions"]
                        type_tr = {
                            "Practice_1": "تمرین اول",
                            "Practice_2": "تمرین دوم",
                            "Practice_3": "تمرین سوم",
                            "Sprint": "اسپرینت",
                            "Sprint_Shootout": "اسپرینت شوت آوت",
                            "Sprint_Qualifying": "تعیین خط اسپرینت",
                            "Qualifying": "تعیین خط",
                            "Race": "مسابقه"
                        }
                        sessions_keys = []
                        for session in sessions:
                            if lang == 1:
                                session_text = session
                            else:
                                session_text = type_tr[session]
                            session_key = [
                                Button.inline(session_text, session.encode()),
                            ]
                            sessions_keys.append(session_key)
                        ask_event = await event.reply(bot_text["select_session"], buttons=sessions_keys)
                        try:
                            session_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                            await bot.delete_messages(user_id, ask_event.id)
                        except TimeoutError:
                            await conv.send_message(bot_text["timeout_error"])
                            await bot.delete_messages(user_id, ask_event.id)
                            return
                        event_data = session_res.data
                        if event_data == b'cancel':
                            await conv.send_message(bot_text["canceled"])
                            await conv.cancel_all()
                        else:
                            session = event_data.decode()
                            if year == 2024:
                                # دریافت تاریخ مسابقه از API
                                check_date = f"https://ergast.com/api/f1/{year}.json"
                                check_date = requests.get(check_date).json()["MRData"]["RaceTable"]["Races"]

                                for grand in check_date:
                                    if grand["raceName"] == gp:
                                        now = datetime.now()
                                        now_date_str = f"{now.year}-{now.month:02d}-{now.day:02d}"
                                        now_time_str = now.strftime("%H:%M:%S")

                                        # ترکیب تاریخ و ساعت فعلی
                                        now_datetime_str = f"{now_date_str} {now_time_str}"
                                        now_datetime = datetime.strptime(now_datetime_str, "%Y-%m-%d %H:%M:%S")

                                        if session == "Race":
                                            race_date = grand["date"]
                                        elif session == "Sprint":
                                            race_date = grand["Sprint"]["date"]
                                        elif session == "Practice_1":
                                            race_date = grand["FirstPractice"]["date"]
                                        elif session == "Practice_2":
                                            race_date = grand["SecondPractice"]["date"]
                                        elif session == "Practice_3":
                                            race_date = grand["ThirdPractice"]["date"]
                                        elif session == "Qualifying":
                                            race_date = grand["Qualifying"]["date"]
                                        else:
                                            await conv.send_message(bot_text["action_not_found"])
                                            return
                                        if check_date_passed(race_date) is False:
                                            race_hour = cur.execute(
                                                f"SELECT time FROM grand_time WHERE grand = '{gp}' AND session_type = '{session}';").fetchone()
                                            if race_hour is None:
                                                print("race hour", race_hour)
                                                print("session and grand", gp, session)
                                                print("check date", check_date_passed(race_date))
                                                await conv.send_message(bot_text["problem"])
                                                return
                                            race_hour = race_hour[0]
                                            # ترکیب تاریخ و ساعت مسابقه
                                            race_datetime_str = f"{race_date} {race_hour}"
                                            race_datetime = datetime.strptime(race_datetime_str, "%Y-%m-%d %H:%M:%S")

                                            if now_datetime < race_datetime:
                                                await conv.send_message(bot_text["dont_time"])
                                                return
                            if lang == 1:
                                loading = await conv.send_message(
                                    bot_text["loading"].format(year=year, gp=gp, event=session))
                            else:
                                loading = await conv.send_message(
                                    bot_text["loading"].format(year=year, gp=country_tr[gp.replace(" ", "_")],
                                                               event=type_tr[session.replace(" ", "_")]))
                            BASE_DIR = Path(__file__).resolve().parent
                            if session == "Practice_1" or session == "Practice_2" or session == "Practice_3":
                                session = sessions_convert[session]
                            image_dyre = f"{year}-{gp}-{session}-deg_tyre.png"
                            image_base_dyre = fr"{BASE_DIR}/{image_dyre}"
                            if os.path.exists(image_base_dyre) is False:
                                deg_tyre_path = await deg_tyre(year, gp, session)
                            await bot.delete_messages(user_id, loading.id)
                            await bot.send_file(user_id, caption="Degradation Tyre", file=image_base_dyre)
                            await bot.send_file(user_id, caption="Degradation Tyre", file=image_base_dyre, force_document=True)
                            config.all_statistics(event.message.message, user_id)
                            config.small_statistics(event.message.message, user_id)
                            user_find = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
                            user_level = user_find[10]
                            level_dict = {
                                "1": bot_text["level_one"],
                                "2": bot_text["level_two"],
                                "3": bot_text["level_three"],
                            }
                            user_level_fa = level_dict[f"{user_level}"]
                            if user_level == "1":
                                user_score = user_find[5]
                                user_score -= 3
                                cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                con.commit()
                                await event.reply(bot_text["score_data"].format(coin=3, level=user_level_fa))
                            elif user_level == "2":
                                user_score = user_find[5]
                                user_score -= 3
                                cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                con.commit()
                                await event.reply(bot_text["score_data"].format(coin=3, level=user_level_fa))
                            elif user_level == "3":
                                user_score = user_find[5]
                                user_score -= 2
                                cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                con.commit()
                                await event.reply(bot_text["score_data"].format(coin=2, level=user_level_fa))

                            await conv.cancel_all()
        elif text == bot_text["weather_data"]:
            find_status = cur.execute(
                f"SELECT status FROM data_status WHERE data = '{event.message.message}'").fetchone()
            print(find_status)
            if find_status[0] == 'off' or find_status[0] is None:
                await event.reply(bot_text["data_is_off"])
                return
            user_find = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
            user_scores = user_find[5]
            user_level = user_find[10]
            score_dict = {
                "1": 1,
                "2": 0,
                "3": 0,
            }
            score_get = score_dict[f"{user_level}"]
            if user_scores - score_get < 0:
                key = [
                    Button.inline(bot_text["account"], data=b'user_account')
                ]
                await event.reply(bot_text["coin_not_enough"].format(score=user_scores), buttons=key)
                return
            async with bot.conversation(user_id) as conv:
                year_keys = [
                    [
                        Button.inline("2024", b'2024')
                    ],
                    [
                        Button.inline("2023", b'2023')
                    ],
                    [
                        Button.inline("2022", b'2022')
                    ],
                    [
                        Button.inline("2021", b'2021')
                    ],
                    [
                        Button.inline("2020", b'2020')
                    ],
                    [
                        Button.inline("2019", b'2019')
                    ],
                    [
                        Button.inline("2018", b'2018')
                    ],
                    [
                        Button.inline(bot_text["cancel"], b'cancel')
                    ]
                ]
                ask_year = await conv.send_message(bot_text["select_year"], buttons=year_keys)
                try:
                    year_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                    await bot.delete_messages(user_id, ask_year.id)
                except TimeoutError:
                    await conv.send_message(bot_text["timeout_error"])
                    await bot.delete_messages(user_id, ask_year.id)
                    return
                year_data = year_res.data
                if year_data == b'cancel':
                    await conv.send_message(bot_text["canceled"])
                    await bot.delete_messages(user_id, ask_year.id)
                    await conv.cancel_all()
                else:
                    year = int(year_data)
                    response = manager.get_event(year=year)["Country"]
                    gp_keys = []
                    for gp in response:
                        if lang == 1:
                            gp_text = gp["t"]
                        else:
                            gp_text = country_tr[gp["tr"]]
                        gp_data = gp["t"].encode()
                        key = Button.inline(gp_text, data=gp_data)
                        gp_keys.append(key)
                    result = []
                    for i in range(0, len(gp_keys), 2):
                        if i + 1 < len(gp_keys):
                            result.append([gp_keys[i], gp_keys[i + 1]])
                        else:
                            result.append([gp_keys[i]])
                    result.append([Button.inline(bot_text["cancel"], b'cancel')])
                    ask_gp = await conv.send_message(bot_text["select_gp"], buttons=result)
                    try:
                        gp_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                        await bot.delete_messages(user_id, ask_gp.id)
                    except TimeoutError:
                        await conv.send_message(bot_text["timeout_error"])
                        await bot.delete_messages(user_id, ask_gp.id)
                        return
                    gp_data = gp_res.data
                    if gp_data == b'cancel':
                        await conv.send_message(bot_text["canceled"])
                        await conv.cancel_all()
                    else:
                        gp = gp_data.decode()
                        # url = f"https://f1datas.com/api/v1/fastf1/session?year={year}&country={gp}"
                        sessions = manager.get_session(year=year, country=gp)["sessions"]
                        # sessions = requests.get(url).json()["sessions"]
                        type_tr = {
                            "Practice_1": "تمرین اول",
                            "Practice_2": "تمرین دوم",
                            "Practice_3": "تمرین سوم",
                            "Sprint": "اسپرینت",
                            "Sprint_Shootout": "اسپرینت شوت آوت",
                            "Sprint_Qualifying": "تعیین خط اسپرینت",
                            "Qualifying": "تعیین خط",
                            "Race": "مسابقه"
                        }
                        sessions_keys = []
                        for session in sessions:
                            if lang == 1:
                                session_text = session
                            else:
                                session_text = type_tr[session]
                            session_key = [
                                Button.inline(session_text, session.encode()),
                            ]
                            sessions_keys.append(session_key)
                        ask_event = await event.reply(bot_text["select_session"], buttons=sessions_keys)
                        try:
                            session_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                            await bot.delete_messages(user_id, ask_event.id)
                        except TimeoutError:
                            await conv.send_message(bot_text["timeout_error"])
                            await bot.delete_messages(user_id, ask_event.id)
                            return
                        event_data = session_res.data
                        if event_data == b'cancel':
                            await conv.send_message(bot_text["canceled"])
                            await conv.cancel_all()
                        else:
                            session = event_data.decode()
                            if year == 2024:
                                # دریافت تاریخ مسابقه از API
                                check_date = f"https://ergast.com/api/f1/{year}.json"
                                check_date = requests.get(check_date).json()["MRData"]["RaceTable"]["Races"]

                                for grand in check_date:
                                    if grand["raceName"] == gp:
                                        now = datetime.now()
                                        now_date_str = f"{now.year}-{now.month:02d}-{now.day:02d}"
                                        now_time_str = now.strftime("%H:%M:%S")

                                        # ترکیب تاریخ و ساعت فعلی
                                        now_datetime_str = f"{now_date_str} {now_time_str}"
                                        now_datetime = datetime.strptime(now_datetime_str, "%Y-%m-%d %H:%M:%S")

                                        if session == "Race":
                                            race_date = grand["date"]
                                        elif session == "Sprint":
                                            race_date = grand["Sprint"]["date"]
                                        elif session == "Practice_1":
                                            race_date = grand["FirstPractice"]["date"]
                                        elif session == "Practice_2":
                                            race_date = grand["SecondPractice"]["date"]
                                        elif session == "Practice_3":
                                            race_date = grand["ThirdPractice"]["date"]
                                        elif session == "Qualifying":
                                            race_date = grand["Qualifying"]["date"]
                                        else:
                                            await conv.send_message(bot_text["action_not_found"])
                                            return
                                        if check_date_passed(race_date) is False:
                                            race_hour = cur.execute(
                                                f"SELECT time FROM grand_time WHERE grand = '{gp}' AND session_type = '{session}';").fetchone()
                                            if race_hour is None:
                                                print("race hour", race_hour)
                                                print("session and grand", gp, session)
                                                print("check date", check_date_passed(race_date))
                                                await conv.send_message(bot_text["problem"])
                                                return
                                            race_hour = race_hour[0]
                                            # ترکیب تاریخ و ساعت مسابقه
                                            race_datetime_str = f"{race_date} {race_hour}"
                                            race_datetime = datetime.strptime(race_datetime_str, "%Y-%m-%d %H:%M:%S")

                                            if now_datetime < race_datetime:
                                                await conv.send_message(bot_text["dont_time"])
                                                return
                            if lang == 1:
                                loading = await conv.send_message(
                                    bot_text["loading"].format(year=year, gp=gp, event=session))
                            else:
                                loading = await conv.send_message(
                                    bot_text["loading"].format(year=year, gp=country_tr[gp.replace(" ", "_")],
                                                               event=type_tr[session.replace(" ", "_")]))
                            BASE_DIR = Path(__file__).resolve().parent
                            if session == "Practice_1" or session == "Practice_2" or session == "Practice_3":
                                session = sessions_convert[session]
                            image_weather = f"{year}-{gp}-{session}-weather_data.png"
                            image_base_weather = fr"{BASE_DIR}/{image_weather}"
                            if os.path.exists(image_base_weather) is False:
                                weather_data_path = await weather_data(year, gp, session)
                            await bot.delete_messages(user_id, loading.id)
                            await bot.send_file(user_id, caption="Weather Data", file=image_base_weather)
                            await bot.send_file(user_id, caption="Weather Data", file=image_base_weather, force_document=True)
                            config.all_statistics(event.message.message, user_id)
                            config.small_statistics(event.message.message, user_id)
                            user_find = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
                            user_level = user_find[10]
                            level_dict = {
                                "1": bot_text["level_one"],
                                "2": bot_text["level_two"],
                                "3": bot_text["level_three"],
                            }
                            user_level_fa = level_dict[f"{user_level}"]
                            if user_level == "1":
                                user_score = user_find[5]
                                user_score -= 1
                                cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                con.commit()
                                await event.reply(bot_text["score_data"].format(coin=1, level=user_level_fa))
                            await conv.cancel_all()
        elif text == bot_text["tyre_performance"]:
            find_status = cur.execute(
                f"SELECT status FROM data_status WHERE data = '{event.message.message}'").fetchone()
            print(find_status)
            if find_status[0] == 'off' or find_status[0] is None:
                await event.reply(bot_text["data_is_off"])
                return
            user_find = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
            user_scores = user_find[5]
            user_level = user_find[10]
            score_dict = {
                "1": 3,
                "2": 2,
                "3": 1,
            }
            score_get = score_dict[f"{user_level}"]
            if user_scores - score_get < 0:
                key = [
                    Button.inline(bot_text["account"], data=b'user_account')
                ]
                await event.reply(bot_text["coin_not_enough"].format(score=user_scores), buttons=key)
                return
            async with bot.conversation(user_id) as conv:
                year_keys = [
                    [
                        Button.inline("2024", b'2024')
                    ],
                    [
                        Button.inline("2023", b'2023')
                    ],
                    [
                        Button.inline("2022", b'2022')
                    ],
                    [
                        Button.inline("2021", b'2021')
                    ],
                    [
                        Button.inline("2020", b'2020')
                    ],
                    [
                        Button.inline("2019", b'2019')
                    ],
                    [
                        Button.inline("2018", b'2018')
                    ],
                    [
                        Button.inline(bot_text["cancel"], b'cancel')
                    ]
                ]
                ask_year = await conv.send_message(bot_text["select_year"], buttons=year_keys)
                try:
                    year_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                    await bot.delete_messages(user_id, ask_year.id)
                except TimeoutError:
                    await conv.send_message(bot_text["timeout_error"])
                    await bot.delete_messages(user_id, ask_year.id)
                    return
                year_data = year_res.data
                if year_data == b'cancel':
                    await conv.send_message(bot_text["canceled"])
                    await bot.delete_messages(user_id, ask_year.id)
                    await conv.cancel_all()
                else:
                    year = int(year_data)
                    response = manager.get_event(year=year)["Country"]
                    gp_keys = []
                    for gp in response:
                        if lang == 1:
                            gp_text = gp["t"]
                        else:
                            gp_text = country_tr[gp["tr"]]
                        gp_data = gp["t"].encode()
                        key = Button.inline(gp_text, data=gp_data)
                        gp_keys.append(key)
                    result = []
                    for i in range(0, len(gp_keys), 2):
                        if i + 1 < len(gp_keys):
                            result.append([gp_keys[i], gp_keys[i + 1]])
                        else:
                            result.append([gp_keys[i]])
                    result.append([Button.inline(bot_text["cancel"], b'cancel')])
                    ask_gp = await conv.send_message(bot_text["select_gp"], buttons=result)
                    try:
                        gp_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                        await bot.delete_messages(user_id, ask_gp.id)
                    except TimeoutError:
                        await conv.send_message(bot_text["timeout_error"])
                        await bot.delete_messages(user_id, ask_gp.id)
                        return
                    gp_data = gp_res.data
                    if gp_data == b'cancel':
                        await conv.send_message(bot_text["canceled"])
                        await conv.cancel_all()
                    else:
                        gp = gp_data.decode()
                        # url = f"https://f1datas.com/api/v1/fastf1/session?year={year}&country={gp}"
                        sessions = manager.get_session(year=year, country=gp)["sessions"]
                        # sessions = requests.get(url).json()["sessions"]
                        type_tr = {
                            "Practice_1": "تمرین اول",
                            "Practice_2": "تمرین دوم",
                            "Practice_3": "تمرین سوم",
                            "Sprint": "اسپرینت",
                            "Sprint_Shootout": "اسپرینت شوت آوت",
                            "Sprint_Qualifying": "تعیین خط اسپرینت",
                            "Qualifying": "تعیین خط",
                            "Race": "مسابقه"
                        }
                        sessions_keys = []
                        for session in sessions:
                            if lang == 1:
                                session_text = session
                            else:
                                session_text = type_tr[session]
                            session_key = [
                                Button.inline(session_text, session.encode()),
                            ]
                            sessions_keys.append(session_key)
                        ask_event = await event.reply(bot_text["select_session"], buttons=sessions_keys)
                        try:
                            session_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                            await bot.delete_messages(user_id, ask_event.id)
                        except TimeoutError:
                            await conv.send_message(bot_text["timeout_error"])
                            await bot.delete_messages(user_id, ask_event.id)
                            return
                        event_data = session_res.data
                        if event_data == b'cancel':
                            await conv.send_message(bot_text["canceled"])
                            await conv.cancel_all()
                        else:
                            session = event_data.decode()
                            if year == 2024:
                                # دریافت تاریخ مسابقه از API
                                check_date = f"https://ergast.com/api/f1/{year}.json"
                                check_date = requests.get(check_date).json()["MRData"]["RaceTable"]["Races"]

                                for grand in check_date:
                                    if grand["raceName"] == gp:
                                        now = datetime.now()
                                        now_date_str = f"{now.year}-{now.month:02d}-{now.day:02d}"
                                        now_time_str = now.strftime("%H:%M:%S")

                                        # ترکیب تاریخ و ساعت فعلی
                                        now_datetime_str = f"{now_date_str} {now_time_str}"
                                        now_datetime = datetime.strptime(now_datetime_str, "%Y-%m-%d %H:%M:%S")

                                        if session == "Race":
                                            race_date = grand["date"]
                                        elif session == "Sprint":
                                            race_date = grand["Sprint"]["date"]
                                        elif session == "Practice_1":
                                            race_date = grand["FirstPractice"]["date"]
                                        elif session == "Practice_2":
                                            race_date = grand["SecondPractice"]["date"]
                                        elif session == "Practice_3":
                                            race_date = grand["ThirdPractice"]["date"]
                                        elif session == "Qualifying":
                                            race_date = grand["Qualifying"]["date"]
                                        else:
                                            await conv.send_message(bot_text["action_not_found"])
                                            return
                                        if check_date_passed(race_date) is False:
                                            race_hour = cur.execute(
                                                f"SELECT time FROM grand_time WHERE grand = '{gp}' AND session_type = '{session}';").fetchone()
                                            if race_hour is None:
                                                print("race hour", race_hour)
                                                print("session and grand", gp, session)
                                                print("check date", check_date_passed(race_date))
                                                await conv.send_message(bot_text["problem"])
                                                return
                                            race_hour = race_hour[0]
                                            # ترکیب تاریخ و ساعت مسابقه
                                            race_datetime_str = f"{race_date} {race_hour}"
                                            race_datetime = datetime.strptime(race_datetime_str, "%Y-%m-%d %H:%M:%S")

                                            if now_datetime < race_datetime:
                                                await conv.send_message(bot_text["dont_time"])
                                                return
                            if lang == 1:
                                loading = await conv.send_message(
                                    bot_text["loading"].format(year=year, gp=gp, event=session))
                            else:
                                loading = await conv.send_message(
                                    bot_text["loading"].format(year=year, gp=country_tr[gp.replace(" ", "_")],
                                                               event=type_tr[session.replace(" ", "_")]))
                            BASE_DIR = Path(__file__).resolve().parent
                            if session == "Practice_1" or session == "Practice_2" or session == "Practice_3":
                                session = sessions_convert[session]
                            image_tyre = f"{year}-{gp}-{session}-tyre_performance.png"
                            image_base_tyre = fr"{BASE_DIR}/{image_tyre}"
                            if os.path.exists(image_base_tyre) is False:
                                weather_data_path = await tyre_performance(year, gp, session)
                            await bot.delete_messages(user_id, loading.id)
                            await bot.send_file(user_id, caption="Tyre Performance", file=image_base_tyre)
                            await bot.send_file(user_id, caption="Tyre Performance", file=image_base_tyre, force_document=True)
                            config.all_statistics(event.message.message, user_id)
                            config.small_statistics(event.message.message, user_id)
                            user_find = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
                            user_level = user_find[10]
                            level_dict = {
                                "1": bot_text["level_one"],
                                "2": bot_text["level_two"],
                                "3": bot_text["level_three"],
                            }
                            user_level_fa = level_dict[f"{user_level}"]
                            if user_level == "1":
                                user_score = user_find[5]
                                user_score -= 3
                                cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                con.commit()
                                await event.reply(bot_text["score_data"].format(coin=3, level=user_level_fa))
                            elif user_level == "2":
                                user_score = user_find[5]
                                user_score -= 2
                                cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                con.commit()
                                await event.reply(bot_text["score_data"].format(coin=2, level=user_level_fa))
                            elif user_level == "3":
                                user_score = user_find[5]
                                user_score -= 1
                                cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                con.commit()
                                await event.reply(bot_text["score_data"].format(coin=1, level=user_level_fa))
                            await conv.cancel_all()
        elif text == bot_text["ers_analysis"]:
            find_status = cur.execute(
                f"SELECT status FROM data_status WHERE data = '{event.message.message}'").fetchone()
            if find_status[0] == 'off' or find_status[0] is None:
                await event.reply(bot_text["data_is_off"])
                return
            user_find = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
            user_scores = user_find[5]
            user_level = user_find[10]
            score_dict = {
                "1": 1,
                "2": 1,
                "3": 0,
            }
            score_get = score_dict[f"{user_level}"]
            if user_scores - score_get < 0:
                key = [
                    Button.inline(bot_text["account"], data=b'user_account')
                ]
                await event.reply(bot_text["coin_not_enough"].format(score=user_scores), buttons=key)
                return
            async with bot.conversation(user_id) as conv:
                year_keys = [
                    [
                        Button.inline("2024", b'2024')
                    ],
                    [
                        Button.inline("2023", b'2023')
                    ],
                    [
                        Button.inline("2022", b'2022')
                    ],
                    [
                        Button.inline("2021", b'2021')
                    ],
                    [
                        Button.inline("2020", b'2020')
                    ],
                    [
                        Button.inline("2019", b'2019')
                    ],
                    [
                        Button.inline("2018", b'2018')
                    ],
                    [
                        Button.inline(bot_text["cancel"], b'cancel')
                    ]
                ]
                ask_year = await conv.send_message(bot_text["select_year"], buttons=year_keys)
                try:
                    year_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                    await bot.delete_messages(user_id, ask_year.id)
                except TimeoutError:
                    await conv.send_message(bot_text["timeout_error"])
                    await bot.delete_messages(user_id, ask_year.id)
                    return
                year_data = year_res.data
                if year_data == b'cancel':
                    await conv.send_message(bot_text["canceled"])
                    await bot.delete_messages(user_id, ask_year.id)
                    await conv.cancel_all()
                else:
                    year = int(year_data)
                    response = manager.get_event(year=year)["Country"]
                    gp_keys = []
                    for gp in response:
                        if lang == 1:
                            gp_text = gp["t"]
                        else:
                            gp_text = country_tr[gp["tr"]]
                        gp_data = str.encode(gp["t"] + ":" + str(gp["round_num"]))
                        key = Button.inline(gp_text, data=gp_data)
                        gp_keys.append(key)
                    result = []
                    for i in range(0, len(gp_keys), 2):
                        if i + 1 < len(gp_keys):
                            result.append([gp_keys[i], gp_keys[i + 1]])
                        else:
                            result.append([gp_keys[i]])
                    result.append([Button.inline(bot_text["cancel"], b'cancel')])
                    ask_gp = await conv.send_message(bot_text["select_gp"], buttons=result)
                    try:
                        gp_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                        await bot.delete_messages(user_id, ask_gp.id)
                    except TimeoutError:
                        await conv.send_message(bot_text["timeout_error"])
                        await bot.delete_messages(user_id, ask_gp.id)
                        return
                    gp_data = gp_res.data
                    if gp_data == b'cancel':
                        await conv.send_message(bot_text["canceled"])
                        await conv.cancel_all()
                    else:
                        gp_country = gp_data.decode().split(":")[0]
                        gp_round = int(gp_data.decode().split(":")[1])
                        sessions = manager.get_session(year=year, country=gp_round)["sessions"]
                        type_tr = {
                            "Practice_1": "تمرین اول",
                            "Practice_2": "تمرین دوم",
                            "Practice_3": "تمرین سوم",
                            "Sprint": "اسپرینت",
                            "Sprint_Shootout": "اسپرینت شوت آوت",
                            "Sprint_Qualifying": "تعیین خط اسپرینت",
                            "Qualifying": "تعیین خط",
                            "Race": "مسابقه"
                        }
                        sessions_keys = []
                        for session in sessions:
                            if lang == 1:
                                session_text = session
                            else:
                                session_text = type_tr[session]
                            session_key = [
                                Button.inline(session_text, session.encode()),
                            ]
                            sessions_keys.append(session_key)
                        ask_event = await event.reply(bot_text["select_session"], buttons=sessions_keys)
                        try:
                            session_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                            await bot.delete_messages(user_id, ask_event.id)
                        except TimeoutError:
                            await conv.send_message(bot_text["timeout_error"])
                            await bot.delete_messages(user_id, ask_event.id)
                            return
                        event_data = session_res.data
                        if event_data == b'cancel':
                            await conv.send_message(bot_text["canceled"])
                            await conv.cancel_all()
                        else:
                            session = event_data.decode()
                            if year == 2024:
                                # دریافت تاریخ مسابقه از API
                                check_date = f"https://ergast.com/api/f1/{year}.json"
                                check_date = requests.get(check_date).json()["MRData"]["RaceTable"]["Races"]

                                for grand in check_date:
                                    if grand["raceName"] == gp:
                                        now = datetime.now()
                                        now_date_str = f"{now.year}-{now.month:02d}-{now.day:02d}"
                                        now_time_str = now.strftime("%H:%M:%S")

                                        # ترکیب تاریخ و ساعت فعلی
                                        now_datetime_str = f"{now_date_str} {now_time_str}"
                                        now_datetime = datetime.strptime(now_datetime_str, "%Y-%m-%d %H:%M:%S")

                                        if session == "Race":
                                            race_date = grand["date"]
                                        elif session == "Sprint":
                                            race_date = grand["Sprint"]["date"]
                                        elif session == "Practice_1":
                                            race_date = grand["FirstPractice"]["date"]
                                        elif session == "Practice_2":
                                            race_date = grand["SecondPractice"]["date"]
                                        elif session == "Practice_3":
                                            race_date = grand["ThirdPractice"]["date"]
                                        elif session == "Qualifying":
                                            race_date = grand["Qualifying"]["date"]
                                        else:
                                            await conv.send_message(bot_text["action_not_found"])
                                            return
                                        if check_date_passed(race_date) is False:
                                            race_hour = cur.execute(
                                                f"SELECT time FROM grand_time WHERE grand = '{gp}' AND session_type = '{session}';").fetchone()
                                            if race_hour is None:
                                                await conv.send_message(bot_text["problem"])
                                                return
                                            race_hour = race_hour[0]
                                            # ترکیب تاریخ و ساعت مسابقه
                                            race_datetime_str = f"{race_date} {race_hour}"
                                            race_datetime = datetime.strptime(race_datetime_str, "%Y-%m-%d %H:%M:%S")

                                            if now_datetime < race_datetime:
                                                await conv.send_message(bot_text["dont_time"])
                                                return
                            url = f"http://ergast.com/api/f1/{year}/{gp_round}/drivers.json"
                            if config.ergast:
                                drivers = requests.get(url).json()["MRData"]["DriverTable"]["Drivers"]
                            else:
                                drivers = ergast_data["MRData"]["DriverTable"]["Drivers"]
                            drivers_keys = []
                            if config.ergast:
                                for driver in drivers:
                                    if lang == 1:
                                        driver_name = driver["givenName"] + driver["familyName"]
                                    else:
                                        driver_name = drivers_translate[
                                            driver["givenName"] + "_" + driver["familyName"]]
                                    driver_code = driver["code"]
                                    key = Button.inline(driver_name, data=driver_code.encode())
                                    drivers_keys.append(key)
                            else:
                                for driver in drivers:
                                    if lang == 1:
                                        driver_name = driver["givenName"] + driver["familyName"]
                                    else:
                                        driver_name = drivers_translate[
                                            driver["givenName"] + "_" + driver["familyName"]]
                                        driver_code = driver["code"]
                                        key = Button.inline(driver_name, data=driver_code.encode())
                                        drivers_keys.append(key)
                            result = []
                            for dv in range(0, len(drivers_keys), 2):
                                if dv + 1 < len(drivers_keys):
                                    result.append([drivers_keys[dv], drivers_keys[dv + 1]])
                                else:
                                    result.append([drivers_keys[dv]])
                            cancel_btn = [Button.inline(bot_text["cancel"], b'cancel')]
                            result.append(cancel_btn)
                            ask_driver = await conv.send_message(bot_text["ask_driver"], buttons=result)
                            try:
                                dr_event = await conv.wait_event(events.CallbackQuery(), timeout=60)
                                await bot.delete_messages(user_id, ask_driver.id)
                            except TimeoutError:
                                await conv.send_message(bot_text["timeout_error"])
                                await bot.delete_messages(user_id, ask_driver.id)
                                return
                            driver_data = dr_event.data
                            if driver_data == b'cancel':
                                await conv.send_message(bot_text["canceled"])
                                await conv.cancel_all()
                            else:
                                driver_code = driver_data.decode()
                                session = event_data.decode()
                                if lang == 1:
                                    loading = await conv.send_message(
                                        bot_text["loading_one"].format(year=year, gp=gp_country, event=session,
                                                                       driver_one=driver_buy_code_en[driver_code]))
                                else:
                                    loading = await conv.send_message(bot_text["loading_one"].format(year=year,
                                                                                                     gp=country_tr[
                                                                                                         gp_country.replace(
                                                                                                             " ", "_")],
                                                                                                     event=type_tr[
                                                                                                         session.replace(
                                                                                                             " ", "_")],
                                                                                                     driver_one=
                                                                                                     driver_buy_code_fa[
                                                                                                         driver_code]))
                                BASE_DIR = Path(__file__).resolve().parent
                                if session == "Practice_1" or session == "Practice_2" or session == "Practice_3":
                                    session = sessions_convert[session]
                                image_ers = f"{year}-{gp_round}-{session}-{driver_code}-ers_analysis.png"
                                image_base_ers = fr"{BASE_DIR}/{image_ers}"
                                if os.path.exists(image_base_ers) is False:
                                    # print(year, gp_round, session, driver_code)
                                    image_ers_path = await ers_analysis(year, gp_round, session, driver_code)
                                await bot.delete_messages(user_id, loading.id)
                                await bot.send_file(user_id, caption="ERS Analysis", file=image_base_ers)
                                await bot.send_file(user_id, caption="ERS Analysis", file=image_base_ers,
                                                    force_document=True)
                                config.all_statistics(event.message.message, user_id)
                                config.small_statistics(event.message.message, user_id)
                                user_find = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
                                user_level = user_find[10]
                                level_dict = {
                                    "1": bot_text["level_one"],
                                    "2": bot_text["level_two"],
                                    "3": bot_text["level_three"],
                                }
                                user_level_fa = level_dict[f"{user_level}"]
                                if user_level == "1":
                                    user_score = user_find[5]
                                    user_score -= 1
                                    cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                    con.commit()
                                    await event.reply(bot_text["score_data"].format(coin=1, level=user_level_fa))
                                elif user_level == "2":
                                    user_score = user_find[5]
                                    user_score -= 1
                                    cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                    con.commit()
                                    await event.reply(bot_text["score_data"].format(coin=1, level=user_level_fa))
                                await conv.cancel_all()
        elif text == bot_text["comparison_fastest_lap"]:
            find_status = cur.execute(
                f"SELECT status FROM data_status WHERE data = '{event.message.message}'").fetchone()
            if find_status[0] == 'off' or find_status[0] is None:
                await event.reply(bot_text["data_is_off"])
                return
            user_find = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
            user_scores = user_find[5]
            user_level = user_find[10]
            score_dict = {
                "1": 1,
                "2": 0,
                "3": 0,
            }
            score_get = score_dict[f"{user_level}"]
            if user_scores - score_get < 0:
                key = [
                    Button.inline(bot_text["account"], data=b'user_account')
                ]
                await event.reply(bot_text["coin_not_enough"].format(score=user_scores), buttons=key)
                return
            async with bot.conversation(user_id) as conv:
                year_keys = [
                    [
                        Button.inline("2024", b'2024')
                    ],
                    [
                        Button.inline("2023", b'2023')
                    ],
                    [
                        Button.inline("2022", b'2022')
                    ],
                    [
                        Button.inline("2021", b'2021')
                    ],
                    [
                        Button.inline("2020", b'2020')
                    ],
                    [
                        Button.inline("2019", b'2019')
                    ],
                    [
                        Button.inline("2018", b'2018')
                    ],
                    [
                        Button.inline(bot_text["cancel"], b'cancel')
                    ]
                ]
                ask_year = await conv.send_message(bot_text["select_year"], buttons=year_keys)
                try:
                    year_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                    await bot.delete_messages(user_id, ask_year.id)
                except TimeoutError:
                    await conv.send_message(bot_text["timeout_error"])
                    await bot.delete_messages(user_id, ask_year.id)
                    return
                year_data = year_res.data
                if year_data == b'cancel':
                    await conv.send_message(bot_text["canceled"])
                    await bot.delete_messages(user_id, ask_year.id)
                    await conv.cancel_all()
                else:
                    year = int(year_data)
                    response = manager.get_event(year=year)["Country"]
                    gp_keys = []
                    for gp in response:
                        if lang == 1:
                            gp_text = gp["t"]
                        else:
                            gp_text = country_tr[gp["tr"]]
                        gp_data = str.encode(gp["t"] + ":" + str(gp["round_num"]))
                        key = Button.inline(gp_text, data=gp_data)
                        gp_keys.append(key)
                    result = []
                    for i in range(0, len(gp_keys), 2):
                        if i + 1 < len(gp_keys):
                            result.append([gp_keys[i], gp_keys[i + 1]])
                        else:
                            result.append([gp_keys[i]])
                    result.append([Button.inline(bot_text["cancel"], b'cancel')])
                    ask_gp = await conv.send_message(bot_text["select_gp"], buttons=result)
                    try:
                        gp_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                        await bot.delete_messages(user_id, ask_gp.id)
                    except TimeoutError:
                        await conv.send_message(bot_text["timeout_error"])
                        await bot.delete_messages(user_id, ask_gp.id)
                        return
                    gp_data = gp_res.data
                    if gp_data == b'cancel':
                        await conv.send_message(bot_text["canceled"])
                        await conv.cancel_all()
                    else:
                        gp_country = gp_data.decode().split(":")[0]
                        gp_round = int(gp_data.decode().split(":")[1])
                        sessions = manager.get_session(year=year, country=gp_round)["sessions"]
                        type_tr = {
                            "Practice_1": "تمرین اول",
                            "Practice_2": "تمرین دوم",
                            "Practice_3": "تمرین سوم",
                            "Sprint": "اسپرینت",
                            "Sprint_Shootout": "اسپرینت شوت آوت",
                            "Sprint_Qualifying": "تعیین خط اسپرینت",
                            "Qualifying": "تعیین خط",
                            "Race": "مسابقه"
                        }
                        sessions_keys = []
                        for session in sessions:
                            if lang == 1:
                                try:
                                    session_text = sessions_convert[session]
                                except KeyError:
                                    session_text = session
                            else:
                                session_text = type_tr[session]
                            session_key = [
                                Button.inline(session_text, session.encode()),
                            ]
                            sessions_keys.append(session_key)
                        ask_event = await event.reply(bot_text["select_session"], buttons=sessions_keys)
                        try:
                            session_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                            await bot.delete_messages(user_id, ask_event.id)
                        except TimeoutError:
                            await conv.send_message(bot_text["timeout_error"])
                            await bot.delete_messages(user_id, ask_event.id)
                            return
                        event_data = session_res.data
                        if event_data == b'cancel':
                            await conv.send_message(bot_text["canceled"])
                            await conv.cancel_all()
                        else:
                            session = event_data.decode()
                            if year == 2024:
                                # دریافت تاریخ مسابقه از API
                                check_date = f"https://ergast.com/api/f1/{year}.json"
                                check_date = requests.get(check_date).json()["MRData"]["RaceTable"]["Races"]

                                for grand in check_date:
                                    if grand["raceName"] == gp:
                                        now = datetime.now()
                                        now_date_str = f"{now.year}-{now.month:02d}-{now.day:02d}"
                                        now_time_str = now.strftime("%H:%M:%S")

                                        # ترکیب تاریخ و ساعت فعلی
                                        now_datetime_str = f"{now_date_str} {now_time_str}"
                                        now_datetime = datetime.strptime(now_datetime_str, "%Y-%m-%d %H:%M:%S")

                                        if session == "Race":
                                            race_date = grand["date"]
                                        elif session == "Sprint":
                                            race_date = grand["Sprint"]["date"]
                                        elif session == "Practice_1":
                                            race_date = grand["FirstPractice"]["date"]
                                        elif session == "Practice_2":
                                            race_date = grand["SecondPractice"]["date"]
                                        elif session == "Practice_3":
                                            race_date = grand["ThirdPractice"]["date"]
                                        elif session == "Qualifying":
                                            race_date = grand["Qualifying"]["date"]
                                        else:
                                            await conv.send_message(bot_text["action_not_found"])
                                            return
                                        print("rpm session", session)
                                        if check_date_passed(race_date) is False:
                                            race_hour = cur.execute(
                                                f"SELECT time FROM grand_time WHERE grand = '{gp}' AND session_type = '{session}';").fetchone()
                                            if race_hour is None:
                                                print("race hour", race_hour)
                                                print("session and grand", gp, session)
                                                print("check date", check_date_passed(race_date))
                                                await conv.send_message(bot_text["problem"])
                                                return
                                            race_hour = race_hour[0]
                                            # ترکیب تاریخ و ساعت مسابقه
                                            race_datetime_str = f"{race_date} {race_hour}"
                                            race_datetime = datetime.strptime(race_datetime_str, "%Y-%m-%d %H:%M:%S")

                                            if now_datetime < race_datetime:
                                                await conv.send_message(bot_text["dont_time"])
                                                return
                            url = f"http://ergast.com/api/f1/{year}/{gp_round}/drivers.json"
                            if config.ergast:
                                drivers = requests.get(url).json()["MRData"]["DriverTable"]["Drivers"]
                            else:
                                drivers = ergast_data["MRData"]["DriverTable"]["Drivers"]
                            drivers_keys = []
                            if config.ergast:
                                for driver in drivers:
                                    if lang == 1:
                                        driver_name = driver["givenName"] + driver["familyName"]
                                    else:
                                        driver_name = drivers_translate[
                                            driver["givenName"] + "_" + driver["familyName"]]
                                    driver_code = driver["code"]
                                    key = Button.inline(driver_name, data=driver_code.encode())
                                    drivers_keys.append(key)
                            else:
                                for driver in drivers:
                                    if lang == 1:
                                        driver_name = driver["givenName"] + driver["familyName"]
                                    else:
                                        driver_name = drivers_translate[
                                            driver["givenName"] + "_" + driver["familyName"]]
                                        driver_code = driver["code"]
                                        key = Button.inline(driver_name, data=driver_code.encode())
                                        drivers_keys.append(key)
                            result = []
                            for dv in range(0, len(drivers_keys), 2):
                                if dv + 1 < len(drivers_keys):
                                    result.append([drivers_keys[dv], drivers_keys[dv + 1]])
                                else:
                                    result.append([drivers_keys[dv]])
                            cancel_btn = [Button.inline(bot_text["cancel"], b'cancel')]
                            result.append(cancel_btn)
                            ask_driver = await conv.send_message(bot_text["ask_driver_one"], buttons=result)
                            try:
                                dr_event = await conv.wait_event(events.CallbackQuery(), timeout=60)
                                print(dr_event)
                                await bot.delete_messages(user_id, ask_driver.id)
                            except TimeoutError:
                                await conv.send_message(bot_text["timeout_error"])
                                await bot.delete_messages(user_id, ask_driver.id)
                                return
                            driver_data = dr_event.data
                            if driver_data == b'cancel':
                                await conv.send_message(bot_text["canceled"])
                                await conv.cancel_all()
                            else:
                                driver_one_name = driver_data.decode()
                                gp_round = int(gp_data.decode().split(":")[1])
                                url = f"http://ergast.com/api/f1/{year}/{gp_round}/drivers.json"
                                if config.ergast:
                                    drivers = requests.get(url).json()["MRData"]["DriverTable"]["Drivers"]
                                else:
                                    drivers = ergast_data["MRData"]["DriverTable"]["Drivers"]
                                drivers_keys = []
                                if config.ergast:
                                    for driver in drivers:
                                        if lang == 1:
                                            driver_name = driver["givenName"] + driver["familyName"]
                                        else:
                                            driver_name = drivers_translate[
                                                driver["givenName"] + "_" + driver["familyName"]]
                                        driver_code = driver["code"]
                                        key = Button.inline(driver_name, data=driver_code.encode())
                                        drivers_keys.append(key)
                                else:
                                    for driver in drivers:
                                        if lang == 1:
                                            driver_name = driver["givenName"] + driver["familyName"]
                                        else:
                                            driver_name = drivers_translate[
                                                driver["givenName"] + "_" + driver["familyName"]]
                                            driver_code = driver["code"]
                                            key = Button.inline(driver_name, data=driver_code.encode())
                                            drivers_keys.append(key)
                                result = []
                                for dv in range(0, len(drivers_keys), 2):
                                    if dv + 1 < len(drivers_keys):
                                        result.append([drivers_keys[dv], drivers_keys[dv + 1]])
                                    else:
                                        result.append([drivers_keys[dv]])
                                cancel_btn = [Button.inline(bot_text["cancel"], b'cancel')]
                                result.append(cancel_btn)
                                ask_driver = await conv.send_message(bot_text["ask_driver_two"], buttons=result)
                                try:
                                    dr_event = await conv.wait_event(events.CallbackQuery(), timeout=60)
                                    await bot.delete_messages(user_id, ask_driver.id)
                                except TimeoutError:
                                    await conv.send_message(bot_text["timeout_error"])
                                    await bot.delete_messages(user_id, ask_driver.id)
                                    return
                                driver_data_two = dr_event.data
                                if driver_data == b"cancel":
                                    await conv.send_message(bot_text["canceled"])
                                    await conv.cancel_all()
                                else:
                                    driver_one_code = driver_data.decode()
                                    driver_two_code = driver_data_two.decode()
                                    session = event_data.decode()
                                    if lang == 1:
                                        loading = await conv.send_message(
                                            bot_text["loading_two"].format(year=year, gp=gp_country, event=session,
                                                                           driver_one=driver_buy_code_en[
                                                                               driver_one_code],
                                                                           driver_two=driver_buy_code_en[
                                                                               driver_two_code]))
                                    else:
                                        loading = await conv.send_message(bot_text["loading_two"].format(year=year,
                                                                                                         gp=country_tr[
                                                                                                             gp_country.replace(
                                                                                                                 " ",
                                                                                                                 "_")],
                                                                                                         event=type_tr[
                                                                                                             session.replace(
                                                                                                                 " ",
                                                                                                                 "_")],
                                                                                                         driver_one=
                                                                                                         driver_buy_code_fa[
                                                                                                             driver_one_code],
                                                                                                         driver_two=
                                                                                                         driver_buy_code_fa[
                                                                                                             driver_two_code]))
                                    BASE_DIR = Path(__file__).resolve().parent
                                    if session == "Practice_1" or session == "Practice_2" or session == "Practice_3" or session == "Sprint_Qualifying":
                                        session = sessions_convert[session]
                                    image_com = f"{year}-{gp_round}-{session}-{driver_one_code}-{driver_two_code}-comparison_fastest_lap.png"
                                    image_base_com = fr"{BASE_DIR}/{image_com}"
                                    if os.path.exists(image_base_com) is False:
                                        image_com_path = await comparison_fastest_lap(year, gp_round, session, driver_one_code,
                                                                         driver_two_code)
                                    await bot.delete_messages(user_id, loading.id)
                                    await bot.send_file(user_id, caption="Comparison Fastest Lap", file=image_base_com)
                                    await bot.send_file(user_id, caption="Comparison Fastest Lap", file=image_base_com,
                                                        force_document=True)
                                    config.all_statistics(event.message.message, user_id)
                                    config.small_statistics(event.message.message, user_id)
                                    user_find = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
                                    user_level = user_find[10]
                                    level_dict = {
                                        "1": bot_text["level_one"],
                                        "2": bot_text["level_two"],
                                        "3": bot_text["level_three"],
                                    }
                                    user_level_fa = level_dict[f"{user_level}"]
                                    if user_level == "1":
                                        user_score = user_find[5]
                                        user_score -= 1
                                        cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                        con.commit()
                                        await event.reply(bot_text["score_data"].format(coin=1, level=user_level_fa))
                                    await conv.cancel_all()
        elif text == bot_text["efficiency_breakdown"]:
            find_status = cur.execute(
                f"SELECT status FROM data_status WHERE data = '{event.message.message}'").fetchone()
            print(find_status)
            if find_status[0] == 'off' or find_status[0] is None:
                await event.reply(bot_text["data_is_off"])
                return
            user_find = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
            user_scores = user_find[5]
            user_level = user_find[10]
            score_dict = {
                "1": 2,
                "2": 1,
                "3": 1,
            }
            score_get = score_dict[f"{user_level}"]
            if user_scores - score_get < 0:
                key = [
                    Button.inline(bot_text["account"], data=b'user_account')
                ]
                await event.reply(bot_text["coin_not_enough"].format(score=user_scores), buttons=key)
                return
            async with bot.conversation(user_id) as conv:
                year_keys = [
                    [
                        Button.inline("2024", b'2024')
                    ],
                    [
                        Button.inline("2023", b'2023')
                    ],
                    [
                        Button.inline("2022", b'2022')
                    ],
                    [
                        Button.inline("2021", b'2021')
                    ],
                    [
                        Button.inline("2020", b'2020')
                    ],
                    [
                        Button.inline("2019", b'2019')
                    ],
                    [
                        Button.inline("2018", b'2018')
                    ],
                    [
                        Button.inline(bot_text["cancel"], b'cancel')
                    ]
                ]
                ask_year = await conv.send_message(bot_text["select_year"], buttons=year_keys)
                try:
                    year_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                    await bot.delete_messages(user_id, ask_year.id)
                except TimeoutError:
                    await conv.send_message(bot_text["timeout_error"])
                    await bot.delete_messages(user_id, ask_year.id)
                    return
                year_data = year_res.data
                if year_data == b'cancel':
                    await conv.send_message(bot_text["canceled"])
                    await bot.delete_messages(user_id, ask_year.id)
                    await conv.cancel_all()
                else:
                    year = int(year_data)
                    response = manager.get_event(year=year)["Country"]
                    gp_keys = []
                    for gp in response:
                        if lang == 1:
                            gp_text = gp["t"]
                        else:
                            gp_text = country_tr[gp["tr"]]
                        gp_data = gp["t"].encode()
                        key = Button.inline(gp_text, data=gp_data)
                        gp_keys.append(key)
                    result = []
                    for i in range(0, len(gp_keys), 2):
                        if i + 1 < len(gp_keys):
                            result.append([gp_keys[i], gp_keys[i + 1]])
                        else:
                            result.append([gp_keys[i]])
                    result.append([Button.inline(bot_text["cancel"], b'cancel')])
                    ask_gp = await conv.send_message(bot_text["select_gp"], buttons=result)
                    try:
                        gp_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                        await bot.delete_messages(user_id, ask_gp.id)
                    except TimeoutError:
                        await conv.send_message(bot_text["timeout_error"])
                        await bot.delete_messages(user_id, ask_gp.id)
                        return
                    gp_data = gp_res.data
                    if gp_data == b'cancel':
                        await conv.send_message(bot_text["canceled"])
                        await conv.cancel_all()
                    else:
                        gp = gp_data.decode()
                        # url = f"https://f1datas.com/api/v1/fastf1/session?year={year}&country={gp}"
                        sessions = manager.get_session(year=year, country=gp)["sessions"]
                        # sessions = requests.get(url).json()["sessions"]
                        type_tr = {
                            "Practice_1": "تمرین اول",
                            "Practice_2": "تمرین دوم",
                            "Practice_3": "تمرین سوم",
                            "Sprint": "اسپرینت",
                            "Sprint_Shootout": "اسپرینت شوت آوت",
                            "Sprint_Qualifying": "تعیین خط اسپرینت",
                            "Qualifying": "تعیین خط",
                            "Race": "مسابقه"
                        }
                        sessions_keys = []
                        for session in sessions:
                            if lang == 1:
                                session_text = session
                            else:
                                session_text = type_tr[session]
                            session_key = [
                                Button.inline(session_text, session.encode()),
                            ]
                            sessions_keys.append(session_key)
                        ask_event = await event.reply(bot_text["select_session"], buttons=sessions_keys)
                        try:
                            session_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                            await bot.delete_messages(user_id, ask_event.id)
                        except TimeoutError:
                            await conv.send_message(bot_text["timeout_error"])
                            await bot.delete_messages(user_id, ask_event.id)
                            return
                        event_data = session_res.data
                        if event_data == b'cancel':
                            await conv.send_message(bot_text["canceled"])
                            await conv.cancel_all()
                        else:
                            session = event_data.decode()
                            if year == 2024:
                                # دریافت تاریخ مسابقه از API
                                check_date = f"https://ergast.com/api/f1/{year}.json"
                                check_date = requests.get(check_date).json()["MRData"]["RaceTable"]["Races"]

                                for grand in check_date:
                                    if grand["raceName"] == gp:
                                        now = datetime.now()
                                        now_date_str = f"{now.year}-{now.month:02d}-{now.day:02d}"
                                        now_time_str = now.strftime("%H:%M:%S")

                                        # ترکیب تاریخ و ساعت فعلی
                                        now_datetime_str = f"{now_date_str} {now_time_str}"
                                        now_datetime = datetime.strptime(now_datetime_str, "%Y-%m-%d %H:%M:%S")

                                        if session == "Race":
                                            race_date = grand["date"]
                                        elif session == "Sprint":
                                            race_date = grand["Sprint"]["date"]
                                        elif session == "Practice_1":
                                            race_date = grand["FirstPractice"]["date"]
                                        elif session == "Practice_2":
                                            race_date = grand["SecondPractice"]["date"]
                                        elif session == "Practice_3":
                                            race_date = grand["ThirdPractice"]["date"]
                                        elif session == "Qualifying":
                                            race_date = grand["Qualifying"]["date"]
                                        else:
                                            await conv.send_message(bot_text["action_not_found"])
                                            return
                                        if check_date_passed(race_date) is False:
                                            race_hour = cur.execute(
                                                f"SELECT time FROM grand_time WHERE grand = '{gp}' AND session_type = '{session}';").fetchone()
                                            if race_hour is None:
                                                print("race hour", race_hour)
                                                print("session and grand", gp, session)
                                                print("check date", check_date_passed(race_date))
                                                await conv.send_message(bot_text["problem"])
                                                return
                                            race_hour = race_hour[0]
                                            # ترکیب تاریخ و ساعت مسابقه
                                            race_datetime_str = f"{race_date} {race_hour}"
                                            race_datetime = datetime.strptime(race_datetime_str, "%Y-%m-%d %H:%M:%S")

                                            if now_datetime < race_datetime:
                                                await conv.send_message(bot_text["dont_time"])
                                                return
                            if lang == 1:
                                loading = await conv.send_message(
                                    bot_text["loading"].format(year=year, gp=gp, event=session))
                            else:
                                loading = await conv.send_message(
                                    bot_text["loading"].format(year=year, gp=country_tr[gp.replace(" ", "_")],
                                                               event=type_tr[session.replace(" ", "_")]))
                            BASE_DIR = Path(__file__).resolve().parent
                            if session == "Practice_1" or session == "Practice_2" or session == "Practice_3":
                                session = sessions_convert[session]
                            image_eff = f"{year}-{gp}-{session}-Efficiency_Breakdown.png"
                            image_base_eff = fr"{BASE_DIR}/{image_eff}"
                            if os.path.exists(image_base_eff) is False:
                                eff_path = await efficiency_breakdown(year, gp, session)
                            await bot.delete_messages(user_id, loading.id)
                            await bot.send_file(user_id, caption="Efficiency Breakdown", file=image_base_eff)
                            await bot.send_file(user_id, caption="Efficiency Breakdown", file=image_base_eff, force_document=True)
                            config.all_statistics(event.message.message, user_id)
                            config.small_statistics(event.message.message, user_id)
                            user_find = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
                            user_level = user_find[10]
                            level_dict = {
                                "1": bot_text["level_one"],
                                "2": bot_text["level_two"],
                                "3": bot_text["level_three"],
                            }
                            user_level_fa = level_dict[f"{user_level}"]
                            if user_level == "1":
                                user_score = user_find[5]
                                user_score -= 2
                                cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                con.commit()
                                await event.reply(bot_text["score_data"].format(coin=2, level=user_level_fa))
                            elif user_level == "2":
                                user_score = user_find[5]
                                user_score -= 1
                                cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                con.commit()
                                await event.reply(bot_text["score_data"].format(coin=1, level=user_level_fa))
                            elif user_level == "3":
                                user_score = user_find[5]
                                user_score -= 1
                                cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                con.commit()
                                await event.reply(bot_text["score_data"].format(coin=1, level=user_level_fa))
                            await conv.cancel_all()
        elif text == bot_text["stress_index"]:
            find_status = cur.execute(
                f"SELECT status FROM data_status WHERE data = '{event.message.message}'").fetchone()
            print(find_status)
            if find_status[0] == 'off' or find_status[0] is None:
                await event.reply(bot_text["data_is_off"])
                return
            user_find = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
            user_scores = user_find[5]
            user_level = user_find[10]
            score_dict = {
                "1": 2,
                "2": 2,
                "3": 1,
            }
            score_get = score_dict[f"{user_level}"]
            if user_scores - score_get < 0:
                key = [
                    Button.inline(bot_text["account"], data=b'user_account')
                ]
                await event.reply(bot_text["coin_not_enough"].format(score=user_scores), buttons=key)
                return
            async with bot.conversation(user_id) as conv:
                year_keys = [
                    [
                        Button.inline("2024", b'2024')
                    ],
                    [
                        Button.inline("2023", b'2023')
                    ],
                    [
                        Button.inline("2022", b'2022')
                    ],
                    [
                        Button.inline("2021", b'2021')
                    ],
                    [
                        Button.inline("2020", b'2020')
                    ],
                    [
                        Button.inline("2019", b'2019')
                    ],
                    [
                        Button.inline("2018", b'2018')
                    ],
                    [
                        Button.inline(bot_text["cancel"], b'cancel')
                    ]
                ]
                ask_year = await conv.send_message(bot_text["select_year"], buttons=year_keys)
                try:
                    year_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                    await bot.delete_messages(user_id, ask_year.id)
                except TimeoutError:
                    await conv.send_message(bot_text["timeout_error"])
                    await bot.delete_messages(user_id, ask_year.id)
                    return
                year_data = year_res.data
                if year_data == b'cancel':
                    await conv.send_message(bot_text["canceled"])
                    await bot.delete_messages(user_id, ask_year.id)
                    await conv.cancel_all()
                else:
                    year = int(year_data)
                    response = manager.get_event(year=year)["Country"]
                    gp_keys = []
                    for gp in response:
                        if lang == 1:
                            gp_text = gp["t"]
                        else:
                            gp_text = country_tr[gp["tr"]]
                        gp_data = gp["t"].encode()
                        key = Button.inline(gp_text, data=gp_data)
                        gp_keys.append(key)
                    result = []
                    for i in range(0, len(gp_keys), 2):
                        if i + 1 < len(gp_keys):
                            result.append([gp_keys[i], gp_keys[i + 1]])
                        else:
                            result.append([gp_keys[i]])
                    result.append([Button.inline(bot_text["cancel"], b'cancel')])
                    ask_gp = await conv.send_message(bot_text["select_gp"], buttons=result)
                    try:
                        gp_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                        await bot.delete_messages(user_id, ask_gp.id)
                    except TimeoutError:
                        await conv.send_message(bot_text["timeout_error"])
                        await bot.delete_messages(user_id, ask_gp.id)
                        return
                    gp_data = gp_res.data
                    if gp_data == b'cancel':
                        await conv.send_message(bot_text["canceled"])
                        await conv.cancel_all()
                    else:
                        gp = gp_data.decode()
                        # url = f"https://f1datas.com/api/v1/fastf1/session?year={year}&country={gp}"
                        sessions = manager.get_session(year=year, country=gp)["sessions"]
                        # sessions = requests.get(url).json()["sessions"]
                        type_tr = {
                            "Practice_1": "تمرین اول",
                            "Practice_2": "تمرین دوم",
                            "Practice_3": "تمرین سوم",
                            "Sprint": "اسپرینت",
                            "Sprint_Shootout": "اسپرینت شوت آوت",
                            "Sprint_Qualifying": "تعیین خط اسپرینت",
                            "Qualifying": "تعیین خط",
                            "Race": "مسابقه"
                        }
                        sessions_keys = []
                        for session in sessions:
                            if lang == 1:
                                session_text = session
                            else:
                                session_text = type_tr[session]
                            session_key = [
                                Button.inline(session_text, session.encode()),
                            ]
                            sessions_keys.append(session_key)
                        ask_event = await event.reply(bot_text["select_session"], buttons=sessions_keys)
                        try:
                            session_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                            await bot.delete_messages(user_id, ask_event.id)
                        except TimeoutError:
                            await conv.send_message(bot_text["timeout_error"])
                            await bot.delete_messages(user_id, ask_event.id)
                            return
                        event_data = session_res.data
                        if event_data == b'cancel':
                            await conv.send_message(bot_text["canceled"])
                            await conv.cancel_all()
                        else:
                            session = event_data.decode()
                            if year == 2024:
                                # دریافت تاریخ مسابقه از API
                                check_date = f"https://ergast.com/api/f1/{year}.json"
                                check_date = requests.get(check_date).json()["MRData"]["RaceTable"]["Races"]

                                for grand in check_date:
                                    if grand["raceName"] == gp:
                                        now = datetime.now()
                                        now_date_str = f"{now.year}-{now.month:02d}-{now.day:02d}"
                                        now_time_str = now.strftime("%H:%M:%S")

                                        # ترکیب تاریخ و ساعت فعلی
                                        now_datetime_str = f"{now_date_str} {now_time_str}"
                                        now_datetime = datetime.strptime(now_datetime_str, "%Y-%m-%d %H:%M:%S")

                                        if session == "Race":
                                            race_date = grand["date"]
                                        elif session == "Sprint":
                                            race_date = grand["Sprint"]["date"]
                                        elif session == "Practice_1":
                                            race_date = grand["FirstPractice"]["date"]
                                        elif session == "Practice_2":
                                            race_date = grand["SecondPractice"]["date"]
                                        elif session == "Practice_3":
                                            race_date = grand["ThirdPractice"]["date"]
                                        elif session == "Qualifying":
                                            race_date = grand["Qualifying"]["date"]
                                        else:
                                            await conv.send_message(bot_text["action_not_found"])
                                            return
                                        if check_date_passed(race_date) is False:
                                            race_hour = cur.execute(
                                                f"SELECT time FROM grand_time WHERE grand = '{gp}' AND session_type = '{session}';").fetchone()
                                            if race_hour is None:
                                                print("race hour", race_hour)
                                                print("session and grand", gp, session)
                                                print("check date", check_date_passed(race_date))
                                                await conv.send_message(bot_text["problem"])
                                                return
                                            race_hour = race_hour[0]
                                            # ترکیب تاریخ و ساعت مسابقه
                                            race_datetime_str = f"{race_date} {race_hour}"
                                            race_datetime = datetime.strptime(race_datetime_str, "%Y-%m-%d %H:%M:%S")

                                            if now_datetime < race_datetime:
                                                await conv.send_message(bot_text["dont_time"])
                                                return
                            if lang == 1:
                                loading = await conv.send_message(
                                    bot_text["loading"].format(year=year, gp=gp, event=session))
                            else:
                                loading = await conv.send_message(
                                    bot_text["loading"].format(year=year, gp=country_tr[gp.replace(" ", "_")],
                                                               event=type_tr[session.replace(" ", "_")]))
                            BASE_DIR = Path(__file__).resolve().parent
                            if session == "Practice_1" or session == "Practice_2" or session == "Practice_3":
                                session = sessions_convert[session]
                            image_stress = f"{year}-{gp}-{session}-stress_index.png"
                            image_base_stress = fr"{BASE_DIR}/{image_stress}"
                            if os.path.exists(image_base_stress) is False:
                                stress_path = await stress_index(year, gp, session)
                            await bot.delete_messages(user_id, loading.id)
                            await bot.send_file(user_id, caption="Stress Index", file=image_base_stress)
                            await bot.send_file(user_id, caption="Stress Index", file=image_base_stress, force_document=True)
                            config.all_statistics(event.message.message, user_id)
                            config.small_statistics(event.message.message, user_id)
                            user_find = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
                            user_level = user_find[10]
                            level_dict = {
                                "1": bot_text["level_one"],
                                "2": bot_text["level_two"],
                                "3": bot_text["level_three"],
                            }
                            user_level_fa = level_dict[f"{user_level}"]
                            if user_level == "1":
                                user_score = user_find[5]
                                user_score -= 2
                                cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                con.commit()
                                await event.reply(bot_text["score_data"].format(coin=2, level=user_level_fa))
                            elif user_level == "2":
                                user_score = user_find[5]
                                user_score -= 2
                                cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                con.commit()
                                await event.reply(bot_text["score_data"].format(coin=2, level=user_level_fa))
                            elif user_level == "3":
                                user_score = user_find[5]
                                user_score -= 1
                                cur.execute(f"UPDATE users SET score = {user_score} WHERE id = {user_id}")
                                con.commit()
                                await event.reply(bot_text["score_data"].format(coin=1, level=user_level_fa))
                            await conv.cancel_all()
        elif text == bot_text["off_all"]:
            is_admin = check_admin(user_id)
            if is_admin is False:
                keys = get_public_keys(user_id)
                await event.reply(bot_text["select"], buttons=keys)
            else:
                async with bot.conversation(user_id, timeout=1000) as conv_all:
                    keys = [
                        Button.inline(bot_text["off_all"], b'off'),
                        Button.inline(bot_text["on_all"], b'on')
                    ]
                    await conv_all.send_message(bot_text["select"], buttons=keys)
                    response = await conv_all.wait_event(events.CallbackQuery())
                    if response.data == b'off':
                        cur.execute(f"UPDATE data_status SET status = 'off'")
                        con.commit()
                    elif response.data == b'on':
                        cur.execute(f"UPDATE data_status SET status = 'on'")
                        con.commit()
                    else:
                        await event.reply(bot_text["action_not_found"])
                        return
                    await event.reply(bot_text["successfully"])
        elif text == bot_text["off_data"]:
            is_admin = check_admin(user_id)
            if is_admin is False:
                keys = get_public_keys(user_id)
                await event.reply(bot_text["select"], buttons=keys)
            else:
                async with bot.conversation(user_id, timeout=1000) as conv_all:
                    keys_all = [
                        [
                            Button.inline(bot_text["rpm"], b'rs'),
                            Button.inline(bot_text["overtake"], b'os'),
                        ],
                        [
                            Button.inline(bot_text["map_viz"], b'ms'),
                            Button.inline(bot_text["down_force"], b'ds'),
                        ],
                        [
                            Button.inline(bot_text["top_speed"], b'ts'),
                            Button.inline(bot_text["start_reaction"], b'sr'),
                        ],
                        [
                            Button.inline(bot_text["all_info"], b'gr'),
                            Button.inline(bot_text["driver"], b'gd'),
                        ],
                        [
                            Button.inline(bot_text["lap_times"], b'pd'),
                            Button.inline(bot_text["map_break"], b'mbs'),
                        ],
                        [
                            Button.inline(bot_text["all"], b'as'),
                            Button.inline(bot_text["strategy"], b'ss'),
                        ],
                        [
                            Button.inline(bot_text["data_to_pole"], b'dp'),
                            Button.inline(bot_text["lap_times_table"], b'lt'),
                        ],
                        [
                            Button.inline(bot_text["brake_configurations"], b'bc'),
                            Button.inline(bot_text["composite_perfomance"], b'cp'),
                        ],
                        [
                            Button.inline(bot_text["degradation_tyre"], b'dt'),
                            Button.inline(bot_text["weather_data"], b'wd'),
                        ],
                        [
                            Button.inline(bot_text["tyre_performance"], b'tp'),
                            Button.inline(bot_text["ers_analysis"], b'ea'),
                        ],
                        [
                            Button.inline(bot_text["comparison_fastest_lap"], b'cf'),
                            Button.inline(bot_text["efficiency_breakdown"], b'eb'),
                        ],
                        [
                            Button.inline(bot_text["stress_index"], b'si')
                        ],
                        [
                            Button.inline(bot_text["cancel"], b'cancel')
                        ]
                    ]
                    await conv_all.send_message(bot_text["select_off_data"], buttons=keys_all)
                    response = await conv_all.wait_event(events.CallbackQuery())
                    statistics_value = None
                    if response.data == b'rs':
                        statistics_value = bot_text["rpm"]
                    elif response.data == b'os':
                        statistics_value = bot_text["overtake"]
                    elif response.data == b'ms':
                        statistics_value = bot_text["map_viz"]
                    elif response.data == b'ds':
                        statistics_value = bot_text["down_force"]
                    elif response.data == b'ts':
                        statistics_value = bot_text["top_speed"]
                    elif response.data == b'sr':
                        statistics_value = bot_text["start_reaction"]
                    elif response.data == b'gr':
                        statistics_value = bot_text["all_info"]
                    elif response.data == b'gd':
                        statistics_value = bot_text["driver"]
                    elif response.data == b'pd':
                        statistics_value = bot_text["lap_times"]
                    elif response.data == b'mbs':
                        statistics_value = bot_text["map_break"]
                    elif response.data == b'as':
                        statistics_value = bot_text["all"]
                    elif response.data == b'ss':
                        statistics_value = bot_text["strategy"]
                    elif response.data == b'dp':
                        statistics_value = bot_text["data_to_pole"]
                    elif response.data == b'lt':
                        statistics_value = bot_text["lap_times_table"]
                    elif response.data == b'bc':
                        statistics_value = bot_text["brake_configurations"]
                    elif response.data == b'cp':
                        statistics_value = bot_text["composite_perfomance"]
                    elif response.data == b'dt':
                        statistics_value = bot_text["degradation_tyre"]
                    elif response.data == b'wd':
                        statistics_value = bot_text["weather_data"]
                    elif response.data == b'tp':
                        statistics_value = bot_text["tyre_performance"]
                    elif response.data == b'ea':
                        statistics_value = bot_text["ers_analysis"]
                    elif response.data == b'cf':
                        statistics_value = bot_text["comparison_fastest_lap"]
                    elif response.data == b'eb':
                        statistics_value = bot_text["efficiency_breakdown"]
                    elif response.data == b'si':
                        statistics_value = bot_text["stress_index"]
                    elif response.data == b'cancel':
                        return
                    else:
                        await conv_all.send_message(bot_text["action_not_found"])
                        return
                    find_status = cur.execute(f"SELECT status FROM data_status WHERE data = '{statistics_value}'").fetchone()
                    if find_status is not None:
                        fa_status_dic = {
                            "off": "خاموش",
                            "on": "روشن",
                        }
                        fa_status = dict(fa_status_dic).get(str(find_status[0]))
                        action_keys = [[Button.inline(bot_text["on"], b'on_data')] if fa_status == "خاموش" else [Button.inline(bot_text["off"], b'off_data')]]
                        action_keys.append([Button.inline(bot_text["cancel"], b'cancel')])
                        await conv_all.send_message(bot_text["data_status"].format(name=statistics_value, status=fa_status), buttons=action_keys)
                        response = await conv_all.wait_event(events.CallbackQuery())
                        if response.data == b'on_data':
                            cur.execute(f"UPDATE data_status SET status = 'on' WHERE data = '{statistics_value}'")
                            con.commit()
                            await event.reply(bot_text["on_data_success"])
                        elif response.data == b'off_data':
                            cur.execute(f"UPDATE data_status SET status = 'off' WHERE data = '{statistics_value}'")
                            con.commit()
                            await event.reply(bot_text["off_data_success"])
                        else:
                            await event.reply(bot_text["canceled"])
                            return
                    else:
                        fa_status_dic = {
                            "off": "خاموش",
                            "on": "روشن",
                        }
                        status = "on"
                        fa_status = dict(fa_status_dic).get(status)
                        action_keys = [[Button.inline(bot_text["on"], b'on_data')] if fa_status == "خاموش" else [Button.inline(bot_text["off"], b'off_data')]]
                        action_keys.append([Button.inline(bot_text["cancel"], b'cancel')])
                        await conv_all.send_message(bot_text["data_status"].format(name=statistics_value, status=fa_status), buttons=action_keys)
                        response = await conv_all.wait_event(events.CallbackQuery())
                        if response.data == b'on_data':
                            cur.execute(f"UPDATE data_status SET status = 'on' WHERE data = '{statistics_value}'")
                            con.commit()
                            await event.reply(bot_text["on_data_success"])
                        elif response.data == b'off_data':
                            cur.execute(f"UPDATE data_status SET status = 'off' WHERE data = '{statistics_value}'")
                            con.commit()
                            await event.reply(bot_text["off_data_success"])
        elif text == bot_text["add_grand"]:
            is_admin = check_admin(user_id)
            if is_admin is False:
                keys = get_public_keys(user_id)
                await event.reply(bot_text["select"], buttons=keys)
            else:
                async with bot.conversation(user_id, timeout=1000) as conv:
                    await conv.send_message(bot_text["enter_grand"])
                    grand_name = await conv.get_response()
                    if grand_name.raw_text == bot_text["cancel"]:
                        await conv.send_message(bot_text["canceled"])
                        return
                    find_grand_name = cur.execute(f"SELECT * FROM grand WHERE name = '{grand_name.raw_text}'").fetchone()
                    if find_grand_name is not None:
                        await event.reply(bot_text["name_already_exists"])
                        return
                    await conv.send_message(bot_text["enter_grand_num"])
                    grand_num = await conv.get_response()
                    if grand_num.raw_text == bot_text["cancel"]:
                        await conv.send_message(bot_text["canceled"])
                        return
                    find_grand_round = cur.execute(f"SELECT * FROM grand WHERE num = '{grand_num.raw_text}'").fetchone()
                    if find_grand_round is not None:
                        await event.reply(bot_text["round_already_exists"])
                        return
                    keys = [
                        Button.inline("1", b'1'),
                        Button.inline("2", b'2')
                    ]
                    await conv.send_message(bot_text["ask_state"], buttons=keys)
                    try:
                        state = await conv.wait_event(events.CallbackQuery())
                    except TimeoutError:
                        await conv.send_message(bot_text["timeout_error"])
                        await conv.cancel_all()
                    state_data = int(state.data.decode())
                    data = [
                        (grand_num.raw_text, grand_name.raw_text, False, state_data)
                    ]
                    cur.executemany(f"INSERT INTO grand VALUES (?,?,?,?)", data)
                    con.commit()
                    # request to ergast
                    ergast_requesting = await event.reply(bot_text["requesting_ergast"])
                    url = f"http://ergast.com/api/f1/2024/{grand_num.raw_text}/drivers.json"
                    result = requests.get(url).json()
                    drivers = result["MRData"]["DriverTable"]["Drivers"]
                    num = 0
                    while num < len(drivers):
                        driver_name = drivers[num]["givenName"] + "_" + drivers[num]["familyName"]
                        driver_id = drivers[num]["driverId"]
                        data = [
                            (int(grand_num.raw_text), driver_name, driver_id, 0, 0, 0),
                        ]
                        cur.executemany("INSERT INTO drivers VALUES (?,?,?,?,?,?)", data)
                        con.commit()
                        num += 1
                    print(ergast_requesting)
                    await bot.delete_messages(user_id, ergast_requesting.id)
                    await event.reply(bot_text["successfully"])
        elif text == bot_text["save_reply"]:
            async with bot.conversation(user_id) as conv:
                # year_keys = [
                #     [
                #         Button.inline("2024", b'2024')
                #     ],
                #     [
                #         Button.inline("2023", b'2023')
                #     ],
                #     [
                #         Button.inline("2022", b'2022')
                #     ],
                #     [
                #         Button.inline("2021", b'2021')
                #     ],
                #     [
                #         Button.inline("2020", b'2020')
                #     ],
                #     [
                #         Button.inline("2019", b'2019')
                #     ],
                #     [
                #         Button.inline("2018", b'2018')
                #     ],
                #     [
                #         Button.inline(bot_text["cancel"], b'cancel')
                #     ]
                # ]
                year_keys = []
                for i in range(2010, 2026):
                    btn = [Button.inline(str(i), str.encode(str(i)))]
                    year_keys.append(btn)
                year_keys.append([Button.inline(bot_text["cancel"], b'cancel')])
                ask_year = await conv.send_message(bot_text["select_year"], buttons=year_keys)
                try:
                    year_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                    await bot.delete_messages(user_id, ask_year.id)
                except TimeoutError:
                    await conv.send_message(bot_text["timeout_error"])
                    await bot.delete_messages(user_id, ask_year.id)
                    return
                year_data = year_res.data
                if year_data == b'cancel':
                    await conv.send_message(bot_text["canceled"])
                    await bot.delete_messages(user_id, ask_year.id)
                    await conv.cancel_all()
                else:
                    year = int(year_data)
                    response = manager.get_event(year=year)["Country"]
                    gp_keys = []
                    for gp in response:
                        if lang == 1:
                            gp_text = gp["t"]
                        else:
                            gp_text = country_tr[gp["tr"]]
                        gp_data = gp["t"].encode()
                        key = Button.inline(gp_text, data=gp_data)
                        gp_keys.append(key)
                    result = []
                    for i in range(0, len(gp_keys), 2):
                        if i + 1 < len(gp_keys):
                            result.append([gp_keys[i], gp_keys[i + 1]])
                        else:
                            result.append([gp_keys[i]])
                    result.append([Button.inline(bot_text["cancel"], b'cancel')])
                    ask_gp = await conv.send_message(bot_text["select_gp"], buttons=result)
                    try:
                        gp_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                        await bot.delete_messages(user_id, ask_gp.id)
                    except TimeoutError:
                        await conv.send_message(bot_text["timeout_error"])
                        await bot.delete_messages(user_id, ask_gp.id)
                        return
                    gp_data = gp_res.data
                    if gp_data == b'cancel':
                        await conv.send_message(bot_text["canceled"])
                        await conv.cancel_all()
                    else:
                        gp = gp_data.decode()
                        # url = f"https://f1datas.com/api/v1/fastf1/session?year={year}&country={gp}"
                        sessions = manager.get_session(year=year, country=gp)["sessions"]
                        # sessions = requests.get(url).json()["sessions"]
                        type_tr = {
                            "Practice_1": "تمرین اول",
                            "Practice_2": "تمرین دوم",
                            "Practice_3": "تمرین سوم",
                            "Sprint": "اسپرینت",
                            "Sprint_Shootout": "اسپرینت شوت آوت",
                            "Sprint_Qualifying": "تعیین خط اسپرینت",
                            "Qualifying": "تعیین خط",
                            "Race": "مسابقه"
                        }
                        sessions_keys = []
                        for session in sessions:
                            if lang == 1:
                                session_text = session
                            else:
                                session_text = type_tr[session]
                            session_key = [
                                Button.inline(session_text, session.encode()),
                            ]
                            sessions_keys.append(session_key)
                        ask_event = await event.reply(bot_text["select_session"], buttons=sessions_keys)
                        try:
                            session_res = await conv.wait_event(events.CallbackQuery(), timeout=60)
                            await bot.delete_messages(user_id, ask_event.id)
                        except TimeoutError:
                            await conv.send_message(bot_text["timeout_error"])
                            await bot.delete_messages(user_id, ask_event.id)
                            return
                        event_data = session_res.data
                        if event_data == b'cancel':
                            await conv.send_message(bot_text["canceled"])
                            await conv.cancel_all()
                        else:
                            session = event_data.decode()
                            if session == "Practice_1" or session == "Practice_2" or session == "Practice_3":
                                # ask user in conversation for enter type he want register link
                                type_buttons = [
                                    [
                                        Button.inline(bot_text["event_drivers"], data=b'drivers'),
                                        Button.inline(bot_text["event_select"], data=b'select'),
                                    ],
                                    [
                                        Button.inline(bot_text["cancel"], b'cancel')
                                    ],
                                ]
                                ask_type = await conv.send_message(bot_text["select_type"], buttons=type_buttons)
                                # handle user response
                                user_response = await conv.wait_event(events.CallbackQuery())
                                if user_response.data == b'drivers':
                                    # to do for next day
                                    await conv.send_message(bot_text["soon"])
                                    return
                                elif user_response.data == b'select':
                                    find_reply = reply_collection.find_one({"year": year, "gp": gp, "event": session, "driver": None})
                                    if find_reply is None:
                                        # ask user for video quality with inline keys in conversation
                                        quality_buttons = [
                                            [
                                                Button.inline("360p❌", data=b'360p'),
                                            ],
                                            [
                                                Button.inline("480p❌", data=b'480p'),
                                            ],
                                            [
                                                Button.inline("720p❌", data=b'720p'),
                                            ],
                                            [
                                                Button.inline("1080p❌", data=b'1080p'),
                                            ],
                                            [
                                                Button.inline("4k❌", data=b'4k'),
                                            ],
                                            [
                                                Button.inline(bot_text["cancel"], data=b'cancel')
                                            ]
                                        ]
                                        ask_quality = await conv.send_message(bot_text["select_quality"], buttons=quality_buttons)
                                        # handle user response
                                        user_response = await conv.wait_event(events.CallbackQuery())
                                        quality = user_response.data
                                        if quality == b'cancel':
                                            await conv.send_message(bot_text["canceled"])
                                            return
                                        else:
                                            #get link from user 
                                            link = await conv.send_message(bot_text["enter_link"])
                                            get_link = await conv.get_response()
                                            get_link = str(get_link.raw_text).split("/")[-1]
                                            data = {
                                                "year": year,
                                                "gp": gp,
                                                "event": session,
                                                "driver": None,
                                                "link": {
                                                    quality.decode(): get_link,
                                                },
                                            }
                                            reply_collection.insert_one(data)
                                            await event.reply(bot_text["saved"])
                                    else:
                                        # ask user for video quality with inline keys in conversation
                                        avalable_quality = find_reply["link"].keys()
                                        quality_buttons = [
                                            [
                                                Button.inline("360p✅" if "360p" in avalable_quality else "360p❌", data=b'360p'),
                                            ],
                                            [
                                                Button.inline("480p✅" if "480p" in avalable_quality else "480p❌", data=b'480p'),
                                            ],
                                            [
                                                Button.inline("720p✅" if "720p" in avalable_quality else "720p❌", data=b'720p'),
                                            ],
                                            [
                                                Button.inline("1080p✅" if "1080p" in avalable_quality else "1080p❌", data=b'1080p'),
                                            ],
                                            [
                                                Button.inline("4k✅" if "4k" in avalable_quality else "4k❌", data=b'4k'),
                                            ],
                                            [
                                                Button.inline(bot_text["cancel"], data=b'cancel')
                                            ]
                                        ]
                                        ask_quality = await conv.send_message(bot_text["select_quality"], buttons=quality_buttons)
                                        # handle user response
                                        user_response = await conv.wait_event(events.CallbackQuery())
                                        quality = user_response.data
                                        if quality == b'cancel':
                                            await conv.send_message(bot_text["canceled"])
                                            return
                                        else:
                                            #get link from user 
                                            link = await conv.send_message(bot_text["enter_link"])
                                            get_link = await conv.get_response()
                                            get_link = str(get_link.raw_text).split("/")[-1]
                                            if quality.decode() not in avalable_quality:
                                                before_link = find_reply["link"]
                                                before_link[quality.decode()] = get_link
                                                # data = {
                                                #     "year": year,
                                                #     "gp": gp,
                                                #     "event": session,
                                                #     "driver": None,
                                                #     "link": {
                                                #         quality.decode(): get_link,
                                                #     },
                                                # }
                                                reply_collection.update_one(find_reply, {"$set": {"link": before_link}})
                                                await event.reply(bot_text["saved"])
        elif text == bot_text["reply"]:
            await bot.forward_messages(user_id, 1, 2475588093)
            # show saved datas in reply collection in inline buttons and send to user
            reply_count = reply_collection.count_documents({})
            if reply_count == 0:
                await event.reply(bot_text["not_found"])
                return
            else:
                reply_data = reply_collection.find()
                buttons = []
                for i in reply_data:
                    # make button with year and gp and event
                    if i["driver"] is None:
                        buttons.append([Button.inline(f"{i['year']} {i['gp']} {i['event']}", str.encode('reply:' + str(i["_id"])))])
                    else:
                        buttons.append([Button.inline(f"{i['year']} {i['gp']} {i['event']} {i['driver']}", str.encode('reply:' + str(i["_id"])))])
                await event.reply(bot_text["select"], buttons=buttons)
                            # await event.reply(f"{year}-{gp}-{session}")
        # elif text == bot_text["add_grand"]:
        #     is_admin = check_admin(user_id)
        #     if is_admin is False:
        #         keys = [
        #             [Button.text(bot_text["archive"], resize=True)],
        #             [Button.text(bot_text["account"]), Button.text(bot_text["support"])],
        #             [Button.text(bot_text["protection"]), Button.text(bot_text["search"]),
        #              Button.text(bot_text["rules"])],
        #         ]
        #         await event.reply(bot_text["select"], buttons=keys)
        #     else:
        #         async with bot.conversation(user_id, timeout=1000) as conv:
        #             await conv.send_message(bot_text["enter_grand"])
        #             grand_name = await conv.get_response()
        #             if grand_name.raw_text == bot_text["cancel"] or grand_name.raw_text == bot_text["back"]:
        #                 await conv.send_message(bot_text["canceled"])
        #                 return
        #             find_grand_name = cur.execute(f"SELECT * FROM grand WHERE name = '{grand_name.raw_text}'").fetchone()
        #             if find_grand_name is not None:
        #                 await event.reply(bot_text["name_already_exists"])
        #                 return
        #             await conv.send_message(bot_text["enter_grand_num"])
        #             grand_num = await conv.get_response()
        #             if grand_num.raw_text == bot_text["cancel"] or grand_num.raw_text == bot_text["back"]:
        #                 await conv.send_message(bot_text["canceled"])
        #                 return
        #             find_grand_round = cur.execute(f"SELECT * FROM grand WHERE num = '{grand_num.raw_text}'").fetchone()
        #             if find_grand_round is not None:
        #                 await event.reply(bot_text["round_already_exists"])
        #                 return
        #             keys = [
        #                 Button.inline("1", b'1'),
        #                 Button.inline("2", b'2')
        #             ]
        #             await conv.send_message(bot_text["ask_state"], buttons=keys)
        #             try:
        #                 state = await conv.wait_event(events.CallbackQuery())
        #             except TimeoutError:
        #                 await conv.send_message(bot_text["timeout_error"])
        #                 await conv.cancel_all()
        #             state_data = int(state.data.decode())
        #             data = [
        #                 (grand_num.raw_text, grand_name.raw_text, False, state_data)
        #             ]
        #             cur.executemany(f"INSERT INTO grand VALUES (?,?,?,?)", data)
        #             con.commit()
        #             # request to ergast
        #             ergast_requesting = await event.reply(bot_text["requesting_ergast"])
        #             url = f"http://ergast.com/api/f1/2024/{grand_num.raw_text}/drivers.json"
        #             result = requests.get(url).json()
        #             drivers = result["MRData"]["DriverTable"]["Drivers"]
        #             for driver in drivers:
        #                 # print(driver)
        #                 driver_name = driver["givenName"] + "_" + driver["familyName"]
        #                 driver_id = driver["driverId"]
        #                 print(driver_id)
        #                 # data = [
        #                     # (int(grand_num.raw_text), driver_name, driver_id, 0, 0, 0),
        #                 # ]
        #                 cur.execute(f"INSERT INTO drivers VALUES ({int(grand_num.raw_text)},'{driver_name}','{driver_id}',{0},{0},{0})")
        #                 con.commit()
        #             await bot.delete_messages(user_id, ergast_requesting.id)
        #             await event.reply(bot_text["successfully"])
        elif text == bot_text["show_grand"]:
            is_admin = check_admin(user_id)
            if is_admin is False:
                keys = get_public_keys(user_id)
                await event.reply(bot_text["select"], buttons=keys)
            else:
                find_count = len(cur.execute("SELECT * FROM grand").fetchall())
                if find_count == 0:
                    await event.reply(bot_text['not_found'])
                    return
                await event.reply(bot_text['welcome_show_grand'])
                find_grands = cur.execute("SELECT * FROM grand ORDER BY num").fetchall()[:5]
                items_per_page = 5
                pages = find_count // items_per_page
                if find_count % items_per_page != 0:
                    pages += 1
                paginate_keys = paginate('show_grand', 1, pages, ':')
                for grand in find_grands:
                    grand_num = grand[0]
                    grand_name = grand[1]
                    key = [
                        [
                            Button.inline(bot_text['close_grand'],
                                          data=str.encode('close_grand:' + str(grand_num))),
                            Button.inline(bot_text['delete_grand'], 'delete_grand:' + str(grand_num)),
                        ]
                    ]
                    full_channel = f'{bot_text["grand_round"]}:{grand_num}\n{bot_text["grand_name"]}:{grand_name}'
                    await bot.send_message(user_id, full_channel, buttons=key)
                try:
                    await bot.send_message(user_id, bot_text['come_next'], buttons=paginate_keys)
                except:
                    pass
        elif text == bot_text["personal_account"]:
            async with bot.conversation(user_id, timeout=1000) as conv_all:
                keys_all = [
                    [
                        Button.inline(bot_text["rpm"], b'rs'),
                        Button.inline(bot_text["overtake"], b'os'),
                    ],
                    [
                        Button.inline(bot_text["map_viz"], b'ms'),
                        Button.inline(bot_text["down_force"], b'ds'),
                    ],
                    [
                        Button.inline(bot_text["top_speed"], b'ts'),
                        Button.inline(bot_text["start_reaction"], b'sr'),
                    ],
                    [
                        Button.inline(bot_text["all_info"], b'gr'),
                        Button.inline(bot_text["driver"], b'gd'),
                    ],
                    [
                        Button.inline(bot_text["lap_times"], b'pd'),
                        Button.inline(bot_text["map_break"], b'mbs'),
                    ],
                    [
                        Button.inline(bot_text["all"], b'as'),
                        Button.inline(bot_text["strategy"], b'ss'),
                    ],
                    [
                        Button.inline(bot_text["data_to_pole"], b'dp'),
                        Button.inline(bot_text["lap_times_table"], b'lt'),
                    ],
                    [
                        Button.inline(bot_text["brake_configurations"], b'bc'),
                        Button.inline(bot_text["composite_perfomance"], b'cp'),
                    ],
                    [
                        Button.inline(bot_text["degradation_tyre"], b'dt'),
                        Button.inline(bot_text["weather_data"], b'wd'),
                    ],
                    [
                        Button.inline(bot_text["tyre_performance"], b'tp'),
                        Button.inline(bot_text["ers_analysis"], b'ea'),
                    ],
                    [
                        Button.inline(bot_text["comparison_fastest_lap"], b'cf'),
                        Button.inline(bot_text["efficiency_breakdown"], b'eb'),
                    ],
                    [
                        Button.inline(bot_text["stress_index"], b'si'),
                    ],
                    [
                        Button.inline(bot_text["cancel"], b'cancel')
                    ]
                ]
                await conv_all.send_message(bot_text["select"], buttons=keys_all)
                response = await conv_all.wait_event(events.CallbackQuery())
                statistics_value = None
                if response.data == b'rs':
                    statistics_value = bot_text["rpm"]
                elif response.data == b'os':
                    statistics_value = bot_text["overtake"]
                elif response.data == b'ms':
                    statistics_value = bot_text["map_viz"]
                elif response.data == b'ds':
                    statistics_value = bot_text["down_force"]
                elif response.data == b'ts':
                    statistics_value = bot_text["top_speed"]
                elif response.data == b'sr':
                    statistics_value = bot_text["start_reaction"]
                elif response.data == b'gr':
                    statistics_value = bot_text["all_info"]
                elif response.data == b'gd':
                    statistics_value = bot_text["driver"]
                elif response.data == b'pd':
                    statistics_value = bot_text["lap_times"]
                elif response.data == b'mbs':
                    statistics_value = bot_text["map_break"]
                elif response.data == b'as':
                    statistics_value = bot_text["all"]
                elif response.data == b'ss':
                    statistics_value = bot_text["strategy"]
                elif response.data == b'dp':
                    statistics_value = bot_text["data_to_pole"]
                elif response.data == b'lt':
                    statistics_value = bot_text["lap_times_table"]
                elif response.data == b'bc':
                    statistics_value = bot_text["brake_configurations"]
                elif response.data == b'cp':
                    statistics_value = bot_text["composite_perfomance"]
                elif response.data == b'dt':
                    statistics_value = bot_text["degradation_tyre"]
                elif response.data == b'wd':
                    statistics_value = bot_text["weather_data"]
                elif response.data == b'tp':
                    statistics_value = bot_text["tyre_performance"]
                elif response.data == b'ea':
                    statistics_value = bot_text["ers_analysis"]
                elif response.data == b'cf':
                    statistics_value = bot_text["comparison_fastest_lap"]
                elif response.data == b'eb':
                    statistics_value = bot_text["efficiency_breakdown"]
                elif response.data == b'si':
                    statistics_value = bot_text["stress_index"]
                elif response.data == b'cancel':
                    return
                else:
                    await conv_all.send_message(bot_text["action_not_found"])
                    return
                count = cur.execute(f"SELECT * FROM statistics_all WHERE data = '{statistics_value}' AND user_id = {user_id}").fetchall()
                count = len(count)
                await event.reply(bot_text["personal_report"].format(count=count, data=statistics_value))
            # await event.reply(bot_text["soon"])
        elif text == bot_text["user_information"]:
            user = cur.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
            if user is None:
                await event.reply(bot_text["first_start"])
            else:
                num_id = user[0]
                join_date = user[3]
                sub_count = user[4]
                score = user[5]
                protection = user[7]
                fantasy = user[6]
                validity = user[8]
                user_level = user[10]
                if user_level == "1":
                    user_level = bot_text["level_one"]
                elif user_level == "2":
                    user_level = bot_text["level_two"]
                elif user_level == "3":
                    user_level = bot_text["level_three"]
                tel_user = await bot.get_entity(user_id)
                first_name = tel_user.first_name
                last_name = tel_user.last_name
                username = tel_user.username if tel_user.username is not None else '❌'
                full_name = first_name + last_name if last_name is not None else first_name
                a_tag = f'<a href="tg://user?id={user_id}">{full_name}</a>'
                c_tag = f'<code>{num_id}</code>'
                if lang == 1:
                    b_tag = "<b>📜 Your user information is as follows:</b>"
                    full_text = "{btag}\n\n" \
                                "⁣👦🏻name: {name}\n" \
                                "🌐id: {username}\n" \
                                "👤number id: {num_id}\n" \
                                "🕰join date: {join_date}\n" \
                                "🌟level: {user_level}\n" \
                                "⭐️score count: {score}\n" \
                                "💳validity: {validity}\n" \
                                "💰sub collection count: {sub_count}\n" \
                                "💵amount of support: {protection}\n" \
                                "💎fantasy coins: {fantasy}\n".format(num_id=c_tag, join_date=join_date,
                                                                      sub_count=sub_count,
                                                                      protection=protection, score=score,
                                                                      fantasy=fantasy,
                                                                      validity=validity, name=a_tag, username=username,
                                                                      btag=b_tag,user_level=user_level)
                else:
                    b_tag = f'<b>📜 اطلاعات کاربری شما به شرح ذیل می باشد:</b>'
                    full_text = "{btag}\n\n" \
                                "⁣👦🏻نام: {name}\n" \
                                "🌐آیدی: {username}\n" \
                                "👤آیدی عددی: {num_id}\n" \
                                "🕰زمان عضویت: {join_date}\n" \
                                "🌟سطح عضویت: {user_level}\n" \
                                "⭐️تعداد امتیاز: {score}\n" \
                                "💳میزان اعتبار: {validity}\n" \
                                "💰تعداد زیر مجموعه: {sub_count}\n" \
                                "💵مقدار حمایت: {protection}\n" \
                                "💎تعداد سکه فانتزی: {fantasy}\n".format(num_id=c_tag, join_date=join_date,
                                                                      sub_count=sub_count,
                                                                      protection=protection, score=score,
                                                                      fantasy=fantasy,
                                                                      validity=validity, name=a_tag, username=username,
                                                                      btag=b_tag,
                                                                      user_level=user_level)
                full_text += "\n🆔 @F1DATAIQBOT"
                buttons = [
                    Button.inline(bot_text["delete_history"], b'delete_history')
                ]
                await bot.send_message(user_id, full_text,
                                       parse_mode='html', buttons=buttons)
        elif text == bot_text["sub_collection"]:
            bot_id = config.BOT_ID
            invite_link = bot_id + "?start=" + str(user_id)
            text = bot_text["sub_link"].format(link=invite_link)
            await event.reply(text)
        elif text == bot_text["show_words"]:
            is_admin = check_admin(user_id)
            if is_admin is False:
                keys = get_public_keys(user_id)
                await event.reply(bot_text["select"], buttons=keys)
            else:
                find_count = len(cur.execute("SELECT * FROM btn").fetchall())
                if find_count == 0:
                    await event.reply(bot_text['not_found'])
                    return
                await event.reply(bot_text['welcome_show_words'])
                find_words = cur.execute("SELECT * FROM btn").fetchall()[:5]
                items_per_page = 5
                pages = find_count // items_per_page
                if find_count % items_per_page != 0:
                    pages += 1
                paginate_keys = paginate('show_btn', 1, pages, ':')
                for word in find_words:
                    word_tag = word[0]
                    word_text = word[1]
                    key = [
                        [
                            Button.inline(bot_text['edit_btn'],
                                          data=str.encode('edit_btn:' + str(word_tag))),
                            Button.inline(bot_text['delete_btn'], 'delete_btn:' + str(word_tag)),
                        ]
                    ]
                    full_channel = f'{bot_text["word_text"]}:{word_text}\n{bot_text["word_tag"]}:{word_tag}'
                    await bot.send_message(user_id, full_channel, buttons=key)
                try:
                    await bot.send_message(user_id, bot_text['come_next'], buttons=paginate_keys)
                except:
                    pass
        elif text == bot_text["coffee"]:
            amount = 100000
            pay = True
        elif text == bot_text["small_party"]:
            amount = 500000
            pay = True
        elif text == bot_text["big_party"]:
            amount = 1000000
            pay = True
        elif text == bot_text["you_pay"]:
            you = True
            pay = True
        elif text == bot_text["dinner"]:
            amount = 500000
            end = True
            pay = True
        if end == True:
            user_end = user[2]
            if user_end:
                await event.reply(bot_text["option"])
                return
        if pay:
            async with bot.conversation(user_id, timeout=1000) as conv:
                if you:
                    await conv.send_message(bot_text["enter_amount"])
                    while True:
                        try:
                            amount = await conv.get_response()
                            amount = amount.raw_text
                            if amount == bot_text["cancel"] or amount == bot_text["back"]:
                                await conv.send_message(bot_text["canceled"])
                                return
                            if int(amount) < 1000:
                                await conv.send_message(bot_text["small_amount"])
                            elif int(amount) > 500000000:
                                await conv.send_message(bot_text["big_amount"])
                            else:
                                break
                        except ValueError:
                            await conv.send_message(bot_text["just_num"])
                await conv.send_message(bot_text["name"])
                name = await conv.get_response()
                if name.media is not None:
                    await conv.send_message(bot_text["dont_image"])
                    return
                if name.raw_text == bot_text["cancel"] or name.raw_text == bot_text["back"]:
                    await conv.send_message(bot_text["canceled"])
                    return
                pay_num = randint(10000, 99999)
                await conv.send_message(bot_text["phone"])
                phone = await conv.get_response()
                if phone.media is not None:
                    await conv.send_message(bot_text["dont_image"])
                    return
                if phone.raw_text == bot_text["cancel"] or phone.raw_text == bot_text["back"]:
                    await conv.send_message(bot_text["canceled"])
                    return
                await conv.send_message(bot_text["email"])
                mail = await conv.get_response()
                if mail.media is not None:
                    await conv.send_message(bot_text["dont_image"])
                    return
                if mail.raw_text == bot_text["cancel"] or mail.raw_text == bot_text["back"]:
                    await conv.send_message(bot_text["canceled"])
                    return
                await conv.send_message(bot_text["desc"])
                desc = await conv.get_response()
                if desc.media is not None:
                    await conv.send_message(bot_text["dont_image"])
                    return
                if desc.raw_text == bot_text["cancel"] or desc.raw_text == bot_text["back"]:
                    await conv.send_message(bot_text["canceled"])
                    return
                name = name.raw_text
                phone = phone.raw_text
                mail = mail.raw_text
                desc = desc.raw_text
                headers = {
                    'Content-Type': 'application/json',
                    'X-API-KEY': pay_token,
                    'X-SANDBOX': '1',
                }

                json_data = {
                    'order_id': pay_num,
                    'amount': amount,
                    'name': name,
                    'phone': phone,
                    'mail': mail,
                    'desc': desc,
                    'callback': config.CALLBACK_URL,
                }
                response = requests.post('https://api.idpay.ir/v1.1/payment', headers=headers, json=json_data)
                res = response.json()
                link = res["link"]
                pay_id = res["id"]
                data = [
                    (user_id, pay_id, pay_num, text)
                ]
                cur.executemany("INSERT INTO pay VALUES(?,?,?,?)", data)
                con.commit()
                data = str.encode("pay_true:" + str(pay_num))
                key = Button.inline(bot_text["success_pay"], data)
                text = bot_text["pay_link"].format(
                    link)
                await event.reply(text, buttons=key)


@bot.on(events.CallbackQuery(pattern="pay_true:*"))
async def pay_hand(event):
    user_id = event.sender_id
    lang = check_lang(user_id)
    if lang == 1:
        bot_text = config.EN_TEXT
    else:
        bot_text = config.TEXT
    back = Button.text(bot_text["back"], resize=True)
    msg_id = event.original_update.msg_id
    order_id = event.data.decode().split(":")[1]
    pay = cur.execute(f"SELECT * FROM pay WHERE order_id={order_id}").fetchone()
    pay_id = pay[1]
    pay_num = pay[2]
    headers = {
        'Content-Type': 'application/json',
        'X-API-KEY': pay_token,
        'X-SANDBOX': '1',
    }

    json_data = {
        'id': pay_id,
        'order_id': pay_num,
    }

    response = requests.post('https://api.idpay.ir/v1.1/payment/inquiry', headers=headers, json=json_data)
    res = response.json()
    status = int(res["status"])
    print(status)
    if status == 200 or status == 10 or status == 100:
        headers = {
            'Content-Type': 'application/json',
            'X-API-KEY': pay_token,
            'X-SANDBOX': '1',
        }

        json_data = {
            'id': pay_id,
            'order_id': pay_num,
        }
        response_v = requests.post("https://api.idpay.ir/v1.1/payment/verify", headers=headers, json=json_data)
        print(response.json())
        if response_v.json()["status"] == 100:
            await bot.delete_messages(user_id, msg_id)
            if pay[3] == bot_text["dinner"]:
                cur.execute(f"UPDATE users SET lastd = {True} WHERE id={user_id}")
                con.commit()
            score = cur.execute(f"SELECT score FROM users WHERE id = {user_id}").fetchone()[0]
            score += 5
            cur.execute(f"UPDATE users SET score = {score} WHERE id = {user_id}")
            con.commit()
            await event.reply(bot_text["pay_verified"])
            return
    else:
        await event.reply(bot_text["dont_pay"])
        return


@bot.on(events.CallbackQuery(pattern="edit_btn:*"))
async def eb(event):
    user_id = event.sender_id
    lang = check_lang(user_id)
    if lang == 1:
        bot_text = config.EN_TEXT
    else:
        bot_text = config.TEXT
    back = Button.text(bot_text["back"], resize=True)
    is_admin = check_admin(user_id)
    if is_admin is False:
        keys = get_public_keys(user_id)
        await event.reply(bot_text["select"], buttons=keys)
        return
    word_tag = event.data.decode().split(":")[1]
    button = cur.execute(f"SELECT * FROM btn WHERE tag = '{word_tag}'").fetchone()
    if button is None:
        await bot.send_message(user_id, bot_text["not_found"])
        return
    else:
        async with bot.conversation(user_id, timeout=1000) as conv:
            await conv.send_message(bot_text["enter_new_text"])
            new_text = await conv.get_response()
            if new_text.raw_text == bot_text["cancel"] or new_text.raw_text == bot_text["back"]:
                await conv.send_message(bot_text["canceled"])
                await conv.cancel_all()
            else:
                text_tag = new_text.raw_text.split('_')
                cur.execute(f"UPDATE btn SET text = '{text_tag[1]}',tag = '{text_tag[0]}' WHERE tag = '{word_tag}'")
                con.commit()
                await conv.send_message(bot_text["edited"])
                await conv.cancel_all()


@bot.on(events.CallbackQuery(pattern="delete_btn:*"))
async def del_btn(event):
    user_id = event.sender_id
    lang = check_lang(user_id)
    if lang == 1:
        bot_text = config.EN_TEXT
    else:
        bot_text = config.TEXT
    back = Button.text(bot_text["back"], resize=True)
    is_admin = check_admin(user_id)
    if is_admin is False:
        keys = get_public_keys(user_id)
        await event.reply(bot_text["select"], buttons=keys)
        return
    btn_tag = event.data.decode().split(":")[1]
    find_btn = cur.execute(f"SELECT * FROM btn WHERE tag = '{btn_tag}'").fetchone()
    if find_btn is None:
        await bot.send_message(user_id, bot_text["not_found"])
    else:
        cur.execute(f"DELETE FROM btn WHERE tag = '{btn_tag}'")
        con.commit()
        await bot.send_message(user_id, bot_text["deleted"])


@bot.on(events.CallbackQuery(pattern='show_btn:*'))
async def show_btn_handler(event):
    user_id = event.sender_id
    lang = check_lang(user_id)
    if lang == 1:
        bot_text = config.EN_TEXT
    else:
        bot_text = config.TEXT
    back = Button.text(bot_text["back"], resize=True)
    start_text = bot_text['select']
    ch_admin = check_admin(user_id)
    if ch_admin is False:
        keys = get_public_keys(user_id)
        await event.reply(bot_text["select"], buttons=keys)
        return
    find_count = len(cur.execute("SELECT * FROM btn").fetchall())
    if find_count == 0:
        await bot.send_message(user_id, bot_text['not_found'])
        return
    page_number = int(event.data.decode().split(':')[1])
    skip_number = (page_number * 5) - 5
    # find_connections = db.connections.find().skip(skip_number).limit(5)
    find_btn = cur.execute("SELECT * FROM btn LIMIT 5 OFFSET ?;", (skip_number,)).fetchall()
    items_per_page = 5
    pages = find_count // items_per_page
    if find_count % items_per_page != 0:
        pages += 1
    paginate_keys = paginate('show_btn', page_number, pages, ':')
    for btn in find_btn:
        word_tag = btn[0]
        btn_text = btn[1]
        key = [
            [
                Button.inline(bot_text['edit_btn'],
                              data=str.encode('edit_btn:' + str(word_tag))),
                Button.inline(bot_text['delete_btn'], 'delete_btn:' + str(word_tag)),
            ]
        ]
        full_channel = f'{bot_text["word_text"]}:{btn_text}\n{bot_text["word_tag"]}:{word_tag}'
        await bot.send_message(user_id, full_channel, buttons=key)
    try:
        await bot.send_message(user_id, bot_text['come_next'], buttons=paginate_keys)
    except:
        pass


@bot.on(events.CallbackQuery(pattern='show_grand:*'))
async def show_grand_handler(event):
    user_id = event.sender_id
    lang = check_lang(user_id)
    if lang == 1:
        bot_text = config.EN_TEXT
    else:
        bot_text = config.TEXT
    back = Button.text(bot_text["back"], resize=True)
    start_text = bot_text['select']
    ch_admin = check_admin(user_id)
    if ch_admin is False:
        keys = get_public_keys(user_id)
        await event.reply(bot_text["select"], buttons=keys)
        return
    find_count = len(cur.execute("SELECT * FROM grand ORDER BY num").fetchall())
    if find_count == 0:
        await bot.send_message(user_id, bot_text['not_found'])
        return
    page_number = int(event.data.decode().split(':')[1])
    skip_number = (page_number * 5) - 5
    # find_connections = db.connections.find().skip(skip_number).limit(5)
    find_grands = cur.execute("SELECT * FROM grand LIMIT 5 OFFSET ?;", (skip_number,)).fetchall()
    items_per_page = 5
    pages = find_count // items_per_page
    if find_count % items_per_page != 0:
        pages += 1
    paginate_keys = paginate('show_grand', page_number, pages, ':')
    for grand in find_grands:
        grand_num = grand[0]
        grand_name = grand[1]
        key = [
            [
                Button.inline(bot_text['close_grand'],
                              data=str.encode('close_grand:' + str(grand_num))),
                Button.inline(bot_text['delete_grand'], 'delete_grand:' + str(grand_num)),
            ]
        ]
        full_channel = f'{bot_text["grand_round"]}:{grand_num}\n{bot_text["grand_name"]}:{grand_name}'
        await bot.send_message(user_id, full_channel, buttons=key)
    try:
        await bot.send_message(user_id, bot_text['come_next'], buttons=paginate_keys)
    except:
        pass

@bot.on(events.CallbackQuery(pattern='show_join:*'))
async def show_join_handler(event):
    user_id = event.sender_id
    lang = check_lang(user_id)
    if lang == 1:
        bot_text = config.EN_TEXT
    else:
        bot_text = config.TEXT
    back = Button.text(bot_text["back"], resize=True)
    start_text = bot_text['select']
    ch_admin = check_admin(user_id)
    if ch_admin is False:
        keys = get_public_keys(user_id)
        await event.reply(bot_text["select"], buttons=keys)
        return
    find_count = len(cur.execute("SELECT * FROM join_channel").fetchall())
    if find_count == 0:
        await bot.send_message(user_id, bot_text['not_found'])
        return
    page_number = int(event.data.decode().split(':')[1])
    skip_number = (page_number * 5) - 5
    # find_connections = db.connections.find().skip(skip_number).limit(5)
    channels = cur.execute("SELECT * FROM join_channel LIMIT 5 OFFSET ?;", (skip_number,)).fetchall()
    items_per_page = 5
    pages = find_count // items_per_page
    if find_count % items_per_page != 0:
        pages += 1
    paginate_keys = paginate('show_join', page_number, pages, ':')
    for channel_id, senior in channels:
        full_channel = f'{bot_text["channel_id"]}:{channel_id}\n{bot_text["senior"]}:{senior}'
        await bot.send_message(user_id, full_channel)
    try:
        await bot.send_message(user_id, bot_text['come_next'], buttons=paginate_keys)
    except:
        pass


@bot.on(events.CallbackQuery(pattern='show_time:*'))
async def show_time_handler(event):
    user_id = event.sender_id
    lang = check_lang(user_id)
    if lang == 1:
        bot_text = config.EN_TEXT
    else:
        bot_text = config.TEXT
    back = Button.text(bot_text["back"], resize=True)
    start_text = bot_text['select']
    ch_admin = check_admin(user_id)
    if ch_admin is False:
        keys = get_public_keys(user_id)
        await event.reply(bot_text["select"], buttons=keys)
        return
    find_count = len(cur.execute("SELECT * FROM grand_time ORDER BY time_num").fetchall())
    if find_count == 0:
        await bot.send_message(user_id, bot_text['not_found'])
        return
    page_number = int(event.data.decode().split(':')[1])
    skip_number = (page_number * 5) - 5
    # find_connections = db.connections.find().skip(skip_number).limit(5)
    find_grands = cur.execute("SELECT * FROM grand_time LIMIT 5 OFFSET ?;", (skip_number,)).fetchall()
    items_per_page = 5
    pages = find_count // items_per_page
    if find_count % items_per_page != 0:
        pages += 1
    paginate_keys = paginate('show_time', page_number, pages, ':')
    for grand in find_grands:
        grand_time = grand[2]
        grand_event = grand[1]
        grand_name = grand[0]
        grand_num = grand[3]
        key = [
            [
                Button.inline(bot_text['delete_grand'], 'delete_time:' + str(grand_num)),
            ]
        ]
        full_channel = f'{bot_text["grand_name"]}:{grand_name}\n{bot_text["time_event"]}:{grand_event}\n{bot_text["time"]}:`{grand_time}`'
        await bot.send_message(user_id, full_channel, buttons=key)
    try:
        await bot.send_message(user_id, bot_text['come_next'], buttons=paginate_keys)
    except:
        pass


@bot.on(events.CallbackQuery(pattern="delete_grand:*"))
async def del_grand(event):
    user_id = event.sender_id
    lang = check_lang(user_id)
    if lang == 1:
        bot_text = config.EN_TEXT
    else:
        bot_text = config.TEXT
    back = Button.text(bot_text["back"], resize=True)
    is_admin = check_admin(user_id)
    if is_admin is False:
        keys = get_public_keys(user_id)
        await event.reply(bot_text["select"], buttons=keys)
        return
    grand_num = event.data.decode().split(":")[1]
    find_btn = cur.execute(f"SELECT * FROM grand WHERE num = '{grand_num}'").fetchone()
    if find_btn is None:
        await bot.send_message(user_id, bot_text["not_found"])
    else:
        cur.execute(f"DELETE FROM grand WHERE num = '{grand_num}'")
        con.commit()
        await bot.send_message(user_id, bot_text["deleted"])

@bot.on(events.CallbackQuery(pattern="delete_time:*"))
async def del_time(event):
    user_id = event.sender_id
    lang = check_lang(user_id)
    if lang == 1:
        bot_text = config.EN_TEXT
    else:
        bot_text = config.TEXT
    back = Button.text(bot_text["back"], resize=True)
    is_admin = check_admin(user_id)
    if is_admin is False:
        keys = get_public_keys(user_id)
        await event.reply(bot_text["select"], buttons=keys)
        return
    grand_num = event.data.decode().split(":")[1]
    find_btn = cur.execute(f"SELECT * FROM grand_time WHERE time_num = {grand_num}").fetchone()
    if find_btn is None:
        await bot.send_message(user_id, bot_text["time_not_found"])
    else:
        cur.execute(f"DELETE FROM grand_time WHERE time_num = {grand_num}")
        con.commit()
        await bot.send_message(user_id, bot_text["deleted"])

@bot.on(events.CallbackQuery(pattern="close_grand:*"))
async def close_grand_handler(event):
    user_id = event.sender_id
    lang = check_lang(user_id)
    if lang == 1:
        bot_text = config.EN_TEXT
    else:
        bot_text = config.TEXT
    back = Button.text(bot_text["back"], resize=True)
    is_admin = check_admin(user_id)
    if is_admin is False:
        keys = get_public_keys(user_id)
        await event.reply(bot_text["select"], buttons=keys)
        return
    grand_num = event.data.decode().split(":")[1]
    grand = cur.execute(f"SELECT * FROM grand WHERE num = '{grand_num}'").fetchone()
    if grand is None:
        await event.reply(bot_text["grand_not_found"])
        return
    if grand[2]:
        cur.execute(f"UPDATE grand SET close = {False} WHERE num = '{grand_num}'")
        con.commit()
        await event.reply(bot_text["grand_opened"])
    else:
        cur.execute(f"UPDATE grand SET close = {True} WHERE num = '{grand_num}'")
        con.commit()
        await event.reply(bot_text["grand_closed"])

@bot.on(events.CallbackQuery(pattern="get_drivers:*"))
async def get_drivers_handler(event):
    user_id = event.sender_id
    lang = check_lang(user_id)
    if lang == 1:
        bot_text = config.EN_TEXT
    else:
        bot_text = config.TEXT
    back = Button.text(bot_text["back"], resize=True)
    grand_num = event.data.decode().split(":")[1]
    find_grand = cur.execute(f"SELECT * FROM grand WHERE num = '{grand_num}'").fetchone()
    if find_grand is None:
        await event.reply(bot_text["grand_not_found"])
    elif find_grand[2]:
        await event.reply(bot_text["grand_is_close"])
    else:
        drivers = cur.execute(f"SELECT * FROM drivers WHERE for_grand = {grand_num}").fetchall()
        print(drivers)
        drivers_keys = []

        for driver in drivers:
            btn_text = drivers_translate[driver[1]]
            driver_key = Button.inline(btn_text, str.encode("driver_score" + ":" + driver[2] + ":"
                                                                                 + str(grand_num)))
            drivers_keys.append(driver_key)
        result = []
        for i in range(0, len(drivers_keys), 2):
            if i + 1 < len(drivers_keys):
                result.append([drivers_keys[i], drivers_keys[i + 1]])
            else:
                result.append([drivers_keys[i]])
        await event.reply(bot_text["select_driver"].format(gp=find_grand[1]), buttons=result)


@bot.on(events.CallbackQuery(pattern="driver_score:*"))
async def driver_score_handler(event):
    user_id = event.sender_id
    lang = check_lang(user_id)
    if lang == 1:
        bot_text = config.EN_TEXT
    else:
        bot_text = config.TEXT
    back = Button.text(bot_text["back"], resize=True)
    spl = event.data.decode().split(":")
    driver_id = spl[1]
    grand_num = spl[2]
    find_grand = cur.execute(f"SELECT * FROM grand WHERE num = '{grand_num}'").fetchone()
    if find_grand is None:
        await event.reply(bot_text["grand_not_found"])
    elif find_grand[2]:
        await event.reply(bot_text["grand_is_close"])
    else:
        driver_score = cur.execute(f"SELECT * FROM driver_score WHERE user_id = {user_id} AND driver_id = '{driver_id}' "
                                   f"AND for_grand = '{grand_num}'").fetchone()
        if driver_score is not None:
            await event.reply(bot_text["you_scored"])
            return
        grand_state = find_grand[3]
        if grand_state == 2:
            async with bot.conversation(user_id, timeout=1000) as conv:
                await conv.send_message(bot_text["qualifying"])
                while True:
                    qscore = await conv.get_response()
                    qscore = qscore.raw_text
                    if qscore == bot_text["back"] or qscore == bot_text["cancel"]:
                        await event.reply(bot_text["canceled"])
                        return
                    check = config.check_number(qscore)
                    if check:
                        break
                    else:
                        await event.reply(bot_text["try_again"])
                await conv.send_message(bot_text["race"])
                while True:
                    rscore = await conv.get_response()
                    rscore = rscore.raw_text
                    if rscore == bot_text["back"] or rscore == bot_text["cancel"]:
                        await event.reply(bot_text["canceled"])
                        return
                    check = config.check_number(rscore)
                    if check:
                        break
                    else:
                        await event.reply(bot_text["try_again"])
                await conv.send_message(bot_text["car"])
                while True:
                    cscore = await conv.get_response()
                    cscore = cscore.raw_text
                    if cscore == bot_text["back"] or cscore == bot_text["cancel"]:
                        await event.reply(bot_text["canceled"])
                        return
                    check = config.check_number(cscore)
                    if check:
                        break
                    else:
                        await event.reply(bot_text["try_again"])
                avg = (float(rscore) + float(qscore) + float(cscore)) / 3
                avg = round(avg, 2)
                find_driver = cur.execute(f"SELECT * FROM drivers WHERE for_grand = {grand_num} AND driver_id = '{driver_id}'").fetchone()
                avg_plus = find_driver[4]
                avg_count = find_driver[5]
                avg_plus += avg
                avg_count += 1
                avg_all = avg_plus / avg_count
                avg_all = round(avg_all, 2)
                cur.execute(f"UPDATE drivers SET avg_plus = {avg_plus},avg_count = {avg_count},avg = {avg_all} WHERE for_grand ="
                            f" {grand_num} AND driver_id = '{driver_id}'")
                con.commit()
                data = [
                    (user_id, driver_id, grand_num)
                ]
                cur.executemany("INSERT INTO driver_score VALUES (?,?,?)", data)
                con.commit()
                await event.reply(bot_text["successfully_scored"], buttons=back)
        else:
            async with bot.conversation(user_id, timeout=1000) as conv:
                await conv.send_message(bot_text["ask_performance"])
                while True:
                    pscore = await conv.get_response()
                    pscore = pscore.raw_text
                    if pscore == bot_text["back"] or pscore == bot_text["cancel"]:
                        await event.reply(bot_text["canceled"])
                        return
                    check = config.check_number(pscore)
                    if check:
                        break
                    else:
                        await event.reply(bot_text["try_again"])
                find_driver = cur.execute(f"SELECT * FROM drivers WHERE for_grand = {grand_num} AND driver_id = '{driver_id}'").fetchone()
                avg_plus = find_driver[4]
                avg_count = find_driver[5]
                avg_plus += int(pscore)
                avg_count += 1
                avg_all = avg_plus / avg_count
                avg_all = round(avg_all, 2)
                cur.execute(f"UPDATE drivers SET avg_plus = {avg_plus},avg_count = {avg_count},avg = {avg_all} WHERE for_grand ="
                            f" {grand_num} AND driver_id = '{driver_id}'")
                con.commit()
                data = [
                    (user_id, driver_id, grand_num)
                ]
                cur.executemany("INSERT INTO driver_score VALUES (?,?,?)", data)
                con.commit()
                await event.reply(bot_text["successfully_scored"], buttons=back)
@bot.on(events.CallbackQuery(pattern="see_score:*"))
async def see_score_handler(event):
    user_id = event.sender_id
    lang = check_lang(user_id)
    if lang == 1:
        bot_text = config.EN_TEXT
    else:
        bot_text = config.TEXT
    back = Button.text(bot_text["back"], resize=True)
    grand_num = int(event.data.decode().split(":")[1])
    find_grand = cur.execute(f"SELECT * FROM grand WHERE num = '{grand_num}'").fetchone()
    if find_grand is None:
        await event.reply(bot_text["grand_not_found"], buttons = back)
    else:
        drivers = cur.execute(f"SELECT * FROM drivers WHERE for_grand = {grand_num} ORDER BY avg").fetchall()
        drivers = drivers[::-1]
        if lang == 1:
            text = """Average points registered for drivers {grand_name}👇 \n\n""".format(grand_name=find_grand[1])
        else:
            text = """میانگین امتیازات ثبت شده برای رانندگان {grand_name}👇 \n\n""".format(grand_name=find_grand[1])
        for driver in drivers:
            driver_name = drivers_translate[driver[1]]
            avg = driver[3]
            driver_text = f"{driver_name} : `{avg}`"
            text = text + driver_text + "\n\n"
        await event.reply(text)

@bot.on(events.CallbackQuery(pattern='ticket_answer:*'))
async def ticket_answer_handler(event):
    user_id = event.original_update.user_id
    lang = check_lang(user_id)
    if lang == 1:
        bot_text = config.EN_TEXT
    else:
        bot_text = config.TEXT
    global q_text
    answer_number = int(event.data.decode().split(':')[1])
    # find_tk = db.tickets.find_one({'count': answer_number})
    find_tk = cur.execute(f"SELECT * FROM tickets WHERE count={answer_number}").fetchone()
    if find_tk is None:
        await event.reply(bot_text['ticket_dl_error'])
        return
    else:
        status = find_tk[4]
        if status == 'close':
            await event.reply(bot_text['close_error'])
            return
    tk_user_id = find_tk[3]
    tk_text = find_tk[1]
    async with bot.conversation(user_id, timeout=1000) as conv:
        await conv.send_message(bot_text['question_image_answer'])
        image_msg = await conv.get_response()
        image_path = None
        if image_msg.media is not None:
            image_path = await image_msg.download_media()
            msg1 = await conv.send_message(bot_text['question_text'])
            text = await conv.get_response()
            q_text = text.message
            if q_text == bot_text['cancel'] or q_text == bot_text['back']:
                key = [
                    Button.text(bot_text['back'])
                ]
                await bot.send_message(user_id, bot_text['canceled'], buttons=key)
                return
        else:
            if image_msg.message == bot_text['cancel'] or image_msg.message == bot_text['back']:
                key = [
                    Button.text(bot_text['back'])
                ]
                await bot.send_message(user_id, bot_text['canceled'], buttons=key)
                return
            else:
                q_text = image_msg.message
    key = [
        [
            Button.text(bot_text['back'])
        ]
    ]
    key_user = [
        Button.inline(bot_text['ticket_answer_ad'],
                      data=str.encode('user_ad:' + str(answer_number))),
    ]
    await bot.send_message(user_id, bot_text['answer_successfully'].format(num=answer_number),
                           buttons=key)
    try:
        await bot.send_message(tk_user_id,
                               bot_text['user_notification'].format(user_text=tk_text,
                                                                                           admin_text=q_text),
                               file=image_path, buttons=key_user)
    except:
        await bot.send_message(tk_user_id,
                               bot_text['user_notification'].format(user_text=tk_text,
                                                                                           admin_text=q_text),
                               buttons=key_user)
    try:
        os.remove(image_path)
    except:
        pass

@bot.on(events.CallbackQuery(pattern='user_ad:*'))
async def user_ad_handler(event):
    user_id = event.original_update.user_id
    lang = check_lang(user_id)
    if lang == 1:
        bot_text = config.EN_TEXT
    else:
        bot_text = config.TEXT
    global q_text
    user_id = event.original_update.user_id
    answer_number = int(event.data.decode().split(':')[1])
    # find_tk = db.tickets.find_one({'count': answer_number})
    find_tk = cur.execute(f"SELECT * FROM tickets WHERE count={answer_number}").fetchone()
    if find_tk is None:
        await event.reply(bot_text['ticket_dl_error'])
        return
    else:
        status = find_tk[4]
        if status == 'close':
            await event.reply(bot_text['close_error'])
            return
        else:
            pass
    async with bot.conversation(user_id, timeout=1000) as conv:
        await conv.send_message(bot_text['question_image_answer'])
        image_msg = await conv.get_response(timeout=1000)
        image_path = None
        if image_msg.media is not None:
            image_path = await image_msg.download_media()
            msg1 = await conv.send_message(bot_text['question_text'])
            text = await conv.get_response()
            q_text = text.message
            if q_text == bot_text['cancel'] or q_text == bot_text['back']:
                key = [
                    Button.text(bot_text['back'])
                ]
                await bot.send_message(user_id, bot_text['canceled'], buttons=key)
                return
        else:
            if image_msg.message == bot_text['cancel'] or image_msg.message == bot_text['back']:
                key = [
                    Button.text(bot_text['back'])
                ]
                await bot.send_message(user_id, bot_text['canceled'], buttons=key)
                return
            else:
                q_text = image_msg.message
    key = [
        [
            Button.text(bot_text['back'])
        ]
    ]
    key_user = [
        Button.inline(bot_text['ticket_answer'],
                      data=str.encode('ticket_answer:' + str(answer_number))),
    ]
    await bot.send_message(user_id, bot_text['answer_successfully_user'], buttons=key)
    admins = cur.execute("SELECT * FROM admins").fetchall()
    for admin in admins:
        ad_id = admin[0]
        user_details = await bot.get_entity(user_id)
        full_name = user_details.first_name + user_details.last_name if user_details.last_name is not None else user_details.first_name
        try:
            await bot.send_message(int(ad_id),
                                   bot_text['admin_notification_answer'].format(text=q_text,
                                                                                                       num=answer_number,
                                                                                                       id=user_id,
                                                                                                       name=full_name,
                                                                                                       username=user_details.username
                                                                                                       ),
                                   file=image_path, buttons=key_user)
        except:
            await bot.send_message(int(ad_id),
                                   bot_text['admin_notification_answer'].format(text=q_text,
                                                                                                       num=answer_number,
                                                                                                       id=user_id,
                                                                                                       name=full_name,
                                                                                                       username=user_details.username
                                                                                                       ),
                                   buttons=key_user)
    try:
        os.remove(image_path)
    except:
        pass
@bot.on(events.CallbackQuery(pattern='show_ticket:*'))
async def show_ticket_handler(event):
    user_id = event.sender_id
    lang = check_lang(user_id)
    if lang == 1:
        bot_text = config.EN_TEXT
    else:
        bot_text = config.TEXT
    back = Button.text(bot_text["back"], resize=True)
    start_text = bot_text['select']
    ch_admin = check_admin(user_id)
    if ch_admin is False:
        keys = get_public_keys(user_id)
        await event.reply(bot_text["select"], buttons=keys)
        return
    find_count = len(cur.execute("SELECT * FROM tickets").fetchall())
    if find_count == 0:
        await bot.send_message(user_id, bot_text['not_found'])
        return
    page_number = int(event.data.decode().split(':')[1])
    skip_number = (page_number * 5) - 5
    # find_connections = db.connections.find().skip(skip_number).limit(5)
    find_tickets = cur.execute("SELECT * FROM tickets LIMIT 5 OFFSET ?;", (skip_number,)).fetchall()
    items_per_page = 5
    pages = find_count // items_per_page
    if find_count % items_per_page != 0:
        pages += 1
    paginate_keys = paginate('show_ticket', page_number, pages, ':')
    for ticket in find_tickets:
        banner_media = ticket[0]
        banner_text = ticket[1]
        banner_user = ticket[3]
        ticket_count = ticket[2]
        full_question = f'{bot_text["ticket_text"]}:{banner_text}\n' \
                        f'{bot_text["ticket_count"]}:{ticket_count}\n' \
                        f'{bot_text["ticket_user_id"]}:`{banner_user}`'

        key = [
            Button.inline(bot_text['ticket_answer'], data=str.encode('ticket_answer:' + str(ticket_count))),
            Button.inline(bot_text['close_ticket'],data=str.encode('close_ticket:' + str(ticket_count))),
        ]
        try:
            await bot.send_message(user_id, full_question, file=banner_media, buttons=key)
        except:
            await bot.send_message(user_id,full_question, buttons=key)
    try:
        await bot.send_message(user_id, bot_text['come_next'], buttons=paginate_keys)
    except:
        pass

@bot.on(events.CallbackQuery(pattern="close_ticket:*"))
async def close_ticket_handler(event):
    user_id = event.sender_id
    lang = check_lang(user_id)
    if lang == 1:
        bot_text = config.EN_TEXT
    else:
        bot_text = config.TEXT
    is_admin = check_admin(user_id)
    if is_admin is False:
        keys = get_public_keys(user_id)
        await event.reply(bot_text["select"], buttons=keys)
        return
    ticket_num = event.data.decode().split(":")[1]
    ticket = cur.execute(f"SELECT * FROM tickets WHERE count = {ticket_num}").fetchone()
    if ticket is None:
        await event.reply(bot_text["ticket_not_found"])
        return
    if ticket[4] == "open":
        cur.execute(f"UPDATE tickets SET status = 'close' WHERE count = {ticket_num}")
        con.commit()
        await event.reply(bot_text["ticket_closed"])
    else:
        cur.execute(f"UPDATE tickets SET status = 'open' WHERE count = {ticket_num}")
        con.commit()
        await event.reply(bot_text["ticket_opened"])

@bot.on(events.NewMessage(pattern="/set:*"))
async def set_channel(event):
    print(event.raw_text)
    channel_id = event.raw_text.split(":")[2]
    channel_id = "https:" + channel_id
    cur.execute("DELETE FROM join_channel")
    cur.execute(f"INSERT INTO join_channel VALUES ('{channel_id}')")
    con.commit()
    config.CHANNEL_ID_PLUS = channel_id

@bot.on(events.CallbackQuery(pattern="delete_channel:*"))
async def del_channel(event):
    user_id = event.sender_id
    lang = check_lang(user_id)
    if lang == 1:
        bot_text = config.EN_TEXT
    else:
        bot_text = config.TEXT
    is_admin = check_admin(user_id)
    if is_admin is False:
        keys = get_public_keys(user_id)
        await event.reply(bot_text["select"], buttons=keys)
        return
    channel_num = event.data.decode().split(":")[1]
    channel = cur.execute(f"SELECT * FROM join_channel WHERE channel_num = {channel_num}").fetchone()
    if channel is None:
        await bot.send_message(user_id, bot_text["not_found"])
    else:
        cur.execute(f"DELETE FROM join_channel WHERE channel_num = {channel_num}")
        con.commit()
        await bot.send_message(user_id, bot_text["deleted"])
@bot.on(events.CallbackQuery(pattern="senior_channel:*"))
async def senior_channel(event):
    user_id = event.sender_id
    lang = check_lang(user_id)
    if lang == 1:
        bot_text = config.EN_TEXT
    else:
        bot_text = config.TEXT
    is_admin = check_admin(user_id)
    if is_admin is False:
        keys = get_public_keys(user_id)
        await event.reply(bot_text["select"], buttons=keys)
        return
    channel_num = int(event.data.decode().split(":")[1])
    channel = cur.execute(f"SELECT * FROM join_channel WHERE channel_num = {channel_num}").fetchone()
    if channel is None:
        await bot.send_message(user_id, bot_text["not_found"])
        return
    if channel[1] == 1:
        await bot.send_message(user_id, bot_text["before_senior"])
        return
    channels = cur.execute("SELECT channel_num FROM join_channel").fetchall()
    for channel_n in channels:
        channel_n = channel_n[0]
        cur.execute(f"UPDATE join_channel SET senior = {False} WHERE channel_num = {channel_n}")
        con.commit()
    cur.execute(f"UPDATE join_channel SET senior = {True} WHERE channel_num = {channel_num}")
    con.commit()
    channel_link = cur.execute(f"SELECT channel_id FROM join_channel WHERE channel_num = {channel_num}").fetchone()[0]
    config.CHANNEL_ID_PLUS = channel_link
    await bot.send_message(user_id, bot_text["channel_up"])

@bot.on(events.CallbackQuery(pattern="down_channel:*"))
async def down_channel(event):
    user_id = event.sender_id
    lang = check_lang(user_id)
    if lang == 1:
        bot_text = config.EN_TEXT
    else:
        bot_text = config.TEXT
    is_admin = check_admin(user_id)
    if is_admin is False:
        keys = get_public_keys(user_id)
        await event.reply(bot_text["select"], buttons=keys)
        return
    channel_id = event.data.decode().split(":")[1]
    channel = cur.execute(f"SELECT * FROM join_channel WHERE channel_num = {channel_id}").fetchone()
    if channel is None:
        await bot.send_message(user_id, bot_text["not_found"])
        return
    if channel[1] is False:
        await bot.send_message(user_id, bot_text["before_down"])
        return
    cur.execute(f"UPDATE join_channel SET senior = {False} WHERE channel_num = {channel_id}")
    con.commit()
    config.CHANNEL_ID_PLUS = None
    await bot.send_message(user_id, bot_text["channel_down"])


@bot.on(events.CallbackQuery(data=b'user_account'))
async def user_account(event):
    user_id = event.sender_id
    lang = check_lang(user_id)
    if lang == 1:
        bot_text = config.EN_TEXT
    else:
        bot_text = config.TEXT
    keys = [
        [
            Button.text(bot_text["user_information"]),
            Button.text(bot_text["personal_account"]),
        ],
        [
            Button.text(bot_text["sub_collection"], resize=1)
        ],
        [
            Button.text(bot_text["back"])
        ]
    ]
    await bot.send_message(user_id, bot_text["select"], buttons=keys)


@bot.on(events.NewMessage(pattern="/reset_idea"))
async def reset_idea(event):
    user_id = event.sender_id
    lang = check_lang(user_id)
    if lang == 1:
        bot_text = config.EN_TEXT
    else:
        bot_text = config.TEXT
    is_admin = check_admin(user_id)
    if is_admin is False:
        keys = get_public_keys(user_id)
        await event.reply(bot_text["select"], buttons=keys)
        return
    cur.execute("DELETE FROM idealization")
    con.commit()
    await event.reply(bot_text["reset_success"])


@bot.on(events.CallbackQuery(data=b'delete_history'))
async def delete_history(event):
    user_id = event.sender_id
    lang = check_lang(user_id)
    text = ""
    delete_users = cur.execute(f"SELECT * FROM deleted_accounts WHERE id={user_id}").fetchall()
    for index, user in enumerate(delete_users):
        print(user)
        num_id = user[0]
        join_date = user[3]
        sub_count = user[4]
        score = user[5]
        protection = user[7]
        fantasy = user[6]
        validity = user[8]
        user_level = user[10]
        delete_time = user[12]
        dt_obj = datetime.fromtimestamp(delete_time)
        delete_time = jdatetime.datetime.fromgregorian(
            year=dt_obj.year,
            month=dt_obj.month,
            day=dt_obj.day,
            hour=dt_obj.hour,
            minute=dt_obj.minute,
            second=dt_obj.second,
        )
        delete_time = f"{delete_time.year}-{delete_time.month}-{delete_time.day} {delete_time.hour}:{delete_time.minute}:{delete_time.second}"
        if user_level == "1":
            user_level = bot_text["level_one"]
        elif user_level == "2":
            user_level = bot_text["level_two"]
        elif user_level == "3":
            user_level = bot_text["level_three"]
        tel_user = await bot.get_entity(num_id)
        first_name = tel_user.first_name
        last_name = tel_user.last_name
        username = tel_user.username if tel_user.username is not None else '❌'
        full_name = first_name + last_name if last_name is not None else first_name
        a_tag = f'<a href="tg://user?id={num_id}">{full_name}</a>'
        c_tag = f'<code>{num_id}</code>'
        if lang == 1:
            b_tag = f"<b>Delete Number {index + 1}</b>"
            text += "\n{btag}\n\n" \
                    "⁣👦🏻name: {name}\n" \
                    "🌐id: {username}\n" \
                    "👤number id: {num_id}\n" \
                    "🕰join date: {join_date}\n" \
                    "🌟level: {user_level}\n" \
                    "⭐️score count: {score}\n" \
                    "💳validity: {validity}\n" \
                    "💰sub collection count: {sub_count}\n" \
                    "💵amount of support: {protection}\n" \
                    "💎fantasy coins: {fantasy}\n" \
                    "delete time: {delete_time}\n".format(num_id=c_tag, join_date=join_date,
                                                          sub_count=sub_count,
                                                          protection=protection, score=score,
                                                          fantasy=fantasy,
                                                          validity=validity, name=a_tag, username=username,
                                                          btag=b_tag, user_level=user_level,
                                                          delete_time=delete_time)
            text += "\n" + "➖➖➖➖➖➖➖➖➖"
        else:
            b_tag = f'<b>حذف شماره {index + 1}</b>'
            text += "\n{btag}\n\n" \
                    "⁣👦🏻نام: {name}\n" \
                    "🌐آیدی: {username}\n" \
                    "👤آیدی عددی: {num_id}\n" \
                    "🕰زمان عضویت: {join_date}\n" \
                    "🌟سطح عضویت: {user_level}\n" \
                    "⭐️تعداد امتیاز: {score}\n" \
                    "💳میزان اعتبار: {validity}\n" \
                    "💰تعداد زیر مجموعه: {sub_count}\n" \
                    "💵مقدار حمایت: {protection}\n" \
                    "💎تعداد سکه فانتزی: {fantasy}\n" \
                    "تاریخ حذف: {delete_time}".format(num_id=c_tag, join_date=join_date,
                                                      sub_count=sub_count,
                                                      protection=protection, score=score,
                                                      fantasy=fantasy,
                                                      validity=validity, name=a_tag, username=username,
                                                      btag=b_tag,
                                                      user_level=user_level, delete_time=delete_time)
            text += "\n" + "➖➖➖➖➖➖➖➖➖"
    await bot.send_message(user_id, text, parse_mode="html")
@bot.on(events.CallbackQuery(pattern="reply:*"))
async def reply(event):
    video_id
bot.run_until_disconnected()
