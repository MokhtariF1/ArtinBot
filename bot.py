import requests
from random import randint
from telethon.sync import TelegramClient, events, Button
from telethon.tl.functions.channels import GetParticipantsRequest, GetFullChannelRequest
from telethon.tl.types import ChannelParticipantsSearch, InputChannel
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
import config
import sqlite3
from navlib import paginate
from datetime import datetime
from funections import top_speed
from pathlib import Path
import os
import time


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

drivers_translate = {
    "Max_Verstappen": "مکس ورستپن",
    "Liam_Lawson": "لیام لاوسون",
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
    "Kevin_Magnussen": "کوین مگنوسن"
}

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
        keys = [
            [Button.text(bot_text["archive"], resize=True)],
            [Button.text(bot_text["account"]), Button.text(bot_text["support"])],
            [Button.text(bot_text["protection"]), Button.text(bot_text["search"]),
             Button.text(bot_text["rules"])],
        ]
        if is_admin:
            keys = [
                [Button.text(bot_text["panel"], resize=True)],
                [Button.text(bot_text["archive"], resize=True)],
                [Button.text(bot_text["account"]), Button.text(bot_text["support"])],
                [Button.text(bot_text["protection"]), Button.text(bot_text["search"]),
                 Button.text(bot_text["rules"])],

            ]
        await bot.delete_messages(user_id, msg_id)
        await bot.send_message(user_id, en, buttons=keys)
    elif event.data == b'lang:fa':
        fa = 2
        up_fa = cur.execute(f"UPDATE users SET lang = {fa} WHERE id={user_id}")
        con.commit()
        bot_text = config.TEXT
        fa = bot_text["FA_SELECTED"]
        is_admin = check_admin(user_id)
        keys = [
            [Button.text(bot_text["archive"], resize=True)],
            [Button.text(bot_text["account"]), Button.text(bot_text["support"])],
            [Button.text(bot_text["protection"]), Button.text(bot_text["search"]),
             Button.text(bot_text["rules"])],
        ]
        if is_admin:
            keys = [
                [Button.text(bot_text["panel"], resize=True)],
                [Button.text(bot_text["archive"], resize=True)],
                [Button.text(bot_text["account"]), Button.text(bot_text["support"])],
                [Button.text(bot_text["protection"]), Button.text(bot_text["search"]),
                 Button.text(bot_text["rules"])],
            ]
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
                    Button.text(bot_text["rules_show"]),
                    Button.text(bot_text["language"], resize=True),
                ],
                [
                    Button.text(bot_text["soon"]),
                    Button.text(bot_text["bot_ping"]),
                    Button.text(bot_text["account_setup"]),
                ],
                [
                    Button.text(bot_text["back"])
                ]
            ]
            await event.reply(bot_text["select"], buttons=keys)
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
            keys = [
                [Button.text(bot_text["archive"], resize=True)],
                [Button.text(bot_text["account"]), Button.text(bot_text["support"])],
                [Button.text(bot_text["protection"]), Button.text(bot_text["search"]),
                 Button.text(bot_text["rules"])],
            ]
            await event.reply(bot_text["FA_SELECTED"], buttons= keys)
        elif text == bot_text["en"]:
            cur.execute(f"UPDATE users SET lang = 1 WHERE id = {user_id}")
            con.commit()
            bot_text = config.EN_TEXT
            keys = [
                [Button.text(bot_text["archive"], resize=True)],
                [Button.text(bot_text["account"]), Button.text(bot_text["support"])],
                [Button.text(bot_text["protection"]), Button.text(bot_text["search"]),
                 Button.text(bot_text["rules"])],
            ]
            await event.reply(bot_text["EN_SELECTED"], buttons= keys)
        elif text == bot_text["rules_show"]:
            await event.reply(bot_text["rules_text"])
        elif text == bot_text["archive"]:
            keys = [
                [
                    Button.text(bot_text["reply"], resize=True)
                ],
                [
                    Button.text(bot_text["fantasy"]),
                    Button.text(bot_text["data_archive"])
                ],
                [
                    Button.text(bot_text["soon"]),
                    Button.text(bot_text["scores"]),
                    Button.text(bot_text["soon"]),
                ],
                [
                    Button.text(bot_text["back"])
                ]
            ]
            await event.reply(bot_text["select"], buttons=keys)
        elif text == bot_text["account"]:
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
        elif text == bot_text["search_in_channel"]:
            async with bot.conversation(user_id, timeout=1000) as conv:
                await conv.send_message(bot_text["enter_hashtag"])
                hashtag = await conv.get_response()
                query = f"SELECT * FROM hashtag WHERE text LIKE '%{hashtag.raw_text}%'"
                search = cur.execute(query).fetchall()
                if len(search) == 0:
                    key = Button.text(bot_text["back"], resize=True)
                    await conv.send_message(bot_text["not_found"], buttons=key)
                    await conv.cancel_all()
                print(search)
                result = "\nنتایج پیدا شده👇\n"
                for tag in search:
                    result += config.CHANNEL_ID + "/" + str(tag[0]) + "\n"
                await conv.send_message(result)
        elif text == bot_text["search_in_bot"]:
            async with bot.conversation(user_id, timeout=1000) as conv:
                msg = await conv.send_message(bot_text["enter_button"])
                btn = await conv.get_response()
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
                    print(start_parameter)
                    if start_parameter != user_id:
                        print("hi1")
                        find_invite = cur.execute(f"SELECT * FROM invite WHERE user_id = {user_id} AND invite_id = "
                                                f"{start_parameter}").fetchone()
                        print(find_invite)
                        if find_invite is None:
                            print("hi")
                            data = [
                                (user_id, start_parameter)
                            ]
                            cur.executemany(f"INSERT INTO invite VALUES (?,?)", data)
                            con.commit()
                            find_user = cur.execute(f"SELECT * FROM users WHERE id = {start_parameter}").fetchone()
                            sub_count = find_user[4]
                            cur.execute(f"UPDATE users SET sub_count = {sub_count + 1} WHERE id = {start_parameter}")
                            con.commit()

            user = cur.execute(f"SELECT * FROM users WHERE id={user_id}").fetchone()
            if user is None:
                currentDateAndTime = datetime.now()
                currentTime = currentDateAndTime.strftime("%Y-%m-%d %H:%M:%S")
                data = [
                    (user_id, None, False, currentTime, 0, 0, 0, 0, 0),
                ]
                cur.executemany(f"INSERT INTO users VALUES (?,?,?,?,?,?,?,?,?)", data)
                con.commit()
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
                    keys = [
                        [Button.text(bot_text["archive"], resize=True)],
                        [Button.text(bot_text["account"]), Button.text(bot_text["support"])],
                        [Button.text(bot_text["protection"]), Button.text(bot_text["search"]),
                         Button.text(bot_text["rules"])],
                    ]
                    if is_admin is not None:
                        keys = [
                            [Button.text(bot_text["panel"], resize=True)],
                            [Button.text(bot_text["archive"], resize=True)],
                            [Button.text(bot_text["account"]), Button.text(bot_text["support"])],
                            [Button.text(bot_text["protection"]), Button.text(bot_text["search"]),
                             Button.text(bot_text["rules"])],

                        ]
                    await event.reply(bot_text["select"], buttons=keys)
        elif text == bot_text["panel"]:
            is_admin = check_admin(user_id)
            if is_admin is False:
                keys = [
                    [Button.text(bot_text["archive"], resize=True)],
                    [Button.text(bot_text["account"]), Button.text(bot_text["support"])],
                    [Button.text(bot_text["protection"]), Button.text(bot_text["search"]),
                     Button.text(bot_text["rules"])],
                ]
                await event.reply(bot_text["select"], buttons=keys)
            else:
                keys = [
                    [
                        Button.text(bot_text["words"], resize=True),
                        Button.text(bot_text["grand"]),
                        Button.text(bot_text["robot_statistics"]),
                    ],
                    [Button.text(bot_text['back'])]
                ]
                await event.reply(bot_text["select"], buttons=keys)
        elif text == bot_text["robot_statistics"]:
            users = cur.execute("SELECT * FROM users").fetchall()
            await event.reply(bot_text["statistics_text"].format(users=len(users)))
        elif text == bot_text["words"]:
            is_admin = check_admin(user_id)
            if is_admin is False:
                keys = [
                    [Button.text(bot_text["archive"], resize=True)],
                    [Button.text(bot_text["account"]), Button.text(bot_text["support"])],
                    [Button.text(bot_text["protection"]), Button.text(bot_text["search"]),
                     Button.text(bot_text["rules"])],
                ]
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
        elif text == bot_text["add_score"]:
            find_grands = cur.execute("SELECT * FROM grand ORDER BY num").fetchall()
            if len(find_grands) == 0:
                await event.reply(bot_text["grands_not_found"], buttons=back)
                return
            inline_keys = []
            for grand in find_grands:
                grand_name = grand[1]
                grand_num = grand[0]
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
                keys = [
                    [Button.text(bot_text["archive"], resize=True)],
                    [Button.text(bot_text["account"]), Button.text(bot_text["support"])],
                    [Button.text(bot_text["protection"]), Button.text(bot_text["search"]),
                     Button.text(bot_text["rules"])],
                ]
                await event.reply(bot_text["select"], buttons=keys)
            else:
                async with bot.conversation(user_id, timeout=1000) as conv:
                    await conv.send_message(bot_text["enter_word"])
                    word = await conv.get_response()
                    if word.raw_text == bot_text["cancel"]:
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
        elif text == bot_text["data_archive"]:
            keys = [
                [
                    Button.text(bot_text["top_speed"])
                ],
                [
                    Button.text(bot_text["back"], resize=1)
                ]
            ]
            await event.reply(bot_text["select"], buttons=keys)
        elif text == bot_text["top_speed"]:
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
                    await conv.cancel_all()
                year_data = year_res.data
                if year_data == b'cancel':
                    await conv.send_message(bot_text["canceled"])
                    await bot.delete_messages(user_id, ask_year.id)
                    await conv.cancel_all()
                else: 
                    year = int(year_data)
                    url = f"https://f1datas.com/api/v1/fastf1/session/gp?year={year}"
                    response = requests.get(url).json()["Country"]
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
                    }
                    gp_keys = []
                    for gp in response:
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
                        await conv.cancel_all()
                    gp_data = gp_res.data
                    if gp_data == b'cancel':
                        await conv.send_message(bot_text["canceled"])
                        await conv.cancel_all()
                    else:
                        gp = gp_data.decode()
                        url = f"https://f1datas.com/api/v1/fastf1/session?year={year}&country={gp}"
                        sessions = requests.get(url).json()["sessions"]
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
                            await conv.cancel_all()
                        event_data = session_res.data
                        if event_data == b'cancel':
                            await conv.send_message(bot_text["canceled"])
                            await conv.cancel_all()
                        else:
                            session = event_data.decode()
                            loading = await conv.send_message(bot_text["loading"])
                            BASE_DIR = Path(__file__).resolve().parent
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
                            await conv.cancel_all()
        elif text == bot_text["add_grand"]:
            is_admin = check_admin(user_id)
            if is_admin is False:
                keys = [
                    [Button.text(bot_text["archive"], resize=True)],
                    [Button.text(bot_text["account"]), Button.text(bot_text["support"])],
                    [Button.text(bot_text["protection"]), Button.text(bot_text["search"]),
                     Button.text(bot_text["rules"])],
                ]
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
                    data = [
                        (grand_num.raw_text, grand_name.raw_text, False)
                    ]
                    cur.executemany(f"INSERT INTO grand VALUES (?,?,?)", data)
                    con.commit()
                    # request to ergast
                    ergast_requesting = await event.reply(bot_text["requesting_ergast"])
                    url = f"http://ergast.com/api/f1/2024/{grand_num.raw_text}/drivers.json"
                    result = requests.get(url).json()
                    drivers = result["MRData"]["DriverTable"]["Drivers"]
                    for driver in drivers:
                        driver_name = driver["givenName"] + "_" + driver["familyName"]
                        driver_id = driver["driverId"]
                        data = [
                            (int(grand_num.raw_text), driver_name, driver_id, 0, 0, 0),
                        ]
                        cur.executemany("INSERT INTO drivers VALUES (?,?,?,?,?,?)", data)
                        con.commit()
                    print(ergast_requesting)
                    await bot.delete_messages(user_id, ergast_requesting.id)
                    await event.reply(bot_text["successfully"])
        elif text == bot_text["show_grand"]:
            is_admin = check_admin(user_id)
            if is_admin is False:
                keys = [
                    [Button.text(bot_text["archive"], resize=True)],
                    [Button.text(bot_text["account"]), Button.text(bot_text["support"])],
                    [Button.text(bot_text["protection"]), Button.text(bot_text["search"]),
                     Button.text(bot_text["rules"])],
                ]
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
                                "💰sub collection count: {sub_count}\n" \
                                "⭐️score count: {score}\n" \
                                "💵amount of support: {protection}\n" \
                                "💎fantasy coins: {fantasy}\n" \
                                "💳validity: {validity}\n".format(num_id=c_tag, join_date=join_date,
                                                                      sub_count=sub_count,
                                                                      protection=protection, score=score,
                                                                      fantasy=fantasy,
                                                                      validity=validity, name=a_tag, username=username,
                                                                      btag=b_tag)
                else:
                    b_tag = f'<b>📜 اطلاعات کاربری شما به شرح ذیل می باشد:</b>'
                    full_text = "{btag}\n\n" \
                                "⁣👦🏻نام: {name}\n" \
                                "🌐آیدی: {username}\n" \
                                "👤آیدی عددی: {num_id}\n" \
                                "🕰زمان عضویت: {join_date}\n" \
                                "💰تعداد زیر مجموعه: {sub_count}\n" \
                                "⭐️تعداد امتیاز: {score}\n" \
                                "💵مقدار حمایت: {protection}\n" \
                                "💎تعداد سکه فانتزی: {fantasy}\n" \
                                "💳میزان اعتبار: {validity}\n".format(num_id=c_tag, join_date=join_date,
                                                                      sub_count=sub_count,
                                                                      protection=protection, score=score,
                                                                      fantasy=fantasy,
                                                                      validity=validity, name=a_tag, username=username,
                                                                      btag=b_tag)

                await bot.send_message(user_id, full_text,
                                       parse_mode='html')
        elif text == bot_text["sub_collection"]:
            bot_id = config.BOT_ID
            invite_link = bot_id + "?start=" + str(user_id)
            text = bot_text["sub_link"].format(link=invite_link)
            await event.reply(text)
        elif text == bot_text["show_words"]:
            is_admin = check_admin(user_id)
            if is_admin is False:
                keys = [
                    [Button.text(bot_text["archive"], resize=True)],
                    [Button.text(bot_text["account"]), Button.text(bot_text["support"])],
                    [Button.text(bot_text["protection"]), Button.text(bot_text["search"]),
                     Button.text(bot_text["rules"])],
                ]
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
                if name.raw_text == bot_text["cancel"]:
                    await conv.send_message(bot_text["canceled"])
                    return
                pay_num = randint(10000, 99999)
                await conv.send_message(bot_text["phone"])
                phone = await conv.get_response()
                if phone.media is not None:
                    await conv.send_message(bot_text["dont_image"])
                    return
                if phone.raw_text == bot_text["cancel"]:
                    await conv.send_message(bot_text["canceled"])
                    return
                await conv.send_message(bot_text["email"])
                mail = await conv.get_response()
                if mail.media is not None:
                    await conv.send_message(bot_text["dont_image"])
                    return
                if mail.raw_text == bot_text["cancel"]:
                    await conv.send_message(bot_text["canceled"])
                    return
                await conv.send_message(bot_text["desc"])
                desc = await conv.get_response()
                if desc.media is not None:
                    await conv.send_message(bot_text["dont_image"])
                    return
                if desc.raw_text == bot_text["cancel"]:
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
        keys = [
            [Button.text(bot_text["archive"], resize=True)],
            [Button.text(bot_text["account"]), Button.text(bot_text["support"])],
            [Button.text(bot_text["protection"]), Button.text(bot_text["search"]),
             Button.text(bot_text["rules"])],
        ]
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
            if new_text.raw_text == bot_text["cancel"]:
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
        keys = [
            [Button.text(bot_text["archive"], resize=True)],
            [Button.text(bot_text["account"]), Button.text(bot_text["support"])],
            [Button.text(bot_text["protection"]), Button.text(bot_text["search"]),
             Button.text(bot_text["rules"])],
        ]
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
        keys = [
            [Button.text(bot_text["archive"], resize=True)],
            [Button.text(bot_text["account"]), Button.text(bot_text["support"])],
            [Button.text(bot_text["protection"]), Button.text(bot_text["search"]),
             Button.text(bot_text["rules"])],
        ]
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
        keys = [
            [Button.text(bot_text["archive"], resize=True)],
            [Button.text(bot_text["account"]), Button.text(bot_text["support"])],
            [Button.text(bot_text["protection"]), Button.text(bot_text["search"]),
             Button.text(bot_text["rules"])],
        ]
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
        keys = [
            [Button.text(bot_text["archive"], resize=True)],
            [Button.text(bot_text["account"]), Button.text(bot_text["support"])],
            [Button.text(bot_text["protection"]), Button.text(bot_text["search"]),
             Button.text(bot_text["rules"])],
        ]
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
        keys = [
            [Button.text(bot_text["archive"], resize=True)],
            [Button.text(bot_text["account"]), Button.text(bot_text["support"])],
            [Button.text(bot_text["protection"]), Button.text(bot_text["search"]),
             Button.text(bot_text["rules"])],
        ]
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
        async with bot.conversation(user_id, timeout=1000) as conv:
            await conv.send_message(bot_text["qualifying"])
            while True:
                qscore = await conv.get_response()
                qscore = qscore.raw_text
                check = config.check_number(qscore)
                if check:
                    break
                else:
                    await event.reply(bot_text["try_again"])
            await conv.send_message(bot_text["race"])
            while True:
                rscore = await conv.get_response()
                rscore = rscore.raw_text
                check = config.check_number(rscore)
                if check:
                    break
                else:
                    await event.reply(bot_text["try_again"])
            await conv.send_message(bot_text["car"])
            while True:
                cscore = await conv.get_response()
                cscore = cscore.raw_text
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
        if lang:
            text = """Average points registered for drivers {grand_name}👇 \n\n""".format(grand_name=find_grand[1])
        else:
            text = """میانگین امتیازات ثبت شده برای رانندگان {grand_name}👇 \n\n""".format(grand_name=find_grand[1])
        for driver in drivers:
            driver_name = drivers_translate[driver[1]]
            avg = driver[3]
            driver_text = f"{driver_name} : `{avg}`"
            text = text + driver_text + "\n\n"
        await event.reply(text)
bot.run_until_disconnected()
