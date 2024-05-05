import requests
from random import randint
from telethon.sync import TelegramClient, events, Button
from telethon.tl.functions.channels import GetParticipantsRequest, GetFullChannelRequest
from telethon.tl.types import ChannelParticipantsSearch, InputChannel
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
import config
import sqlite3
from navlib import paginate


api_id = config.API_ID
api_hash = config.API_HASH
bot_token = config.BOT_TOKEN
pay_token = config.PAY_TOKEN
session_name = config.SESSION_NAME
proxy = config.PROXY
bot_text = config.TEXT
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

def check_admin(user_id):
    is_admin = cur.execute(f"SELECT * FROM admins WHERE _id = {user_id}").fetchone()
    return True if is_admin is not None else False


@bot.on(events.CallbackQuery())
async def call_handler(event):
    user_id = event.sender_id
    msg_id = event.original_update.msg_id
    if event.data == b'lang:en':
        en = 1
        up_en = cur.execute(f"UPDATE users SET lang = {en} WHERE id={user_id}")
        con.commit()
        en = bot_text["EN_SELECTED"]
        await bot.delete_messages(user_id, msg_id)
        await bot.send_message(user_id, en)
    elif event.data == b'lang:fa':
        fa = 2
        up_fa = cur.execute(f"UPDATE users SET lang = {fa} WHERE id={user_id}")
        con.commit()
        fa = bot_text["FA_SELECTED"]
        await bot.delete_messages(user_id, msg_id)
        await bot.send_message(user_id, fa)

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
            await event.reply(bot_text["rules_text"])
        elif text == bot_text["archive"]:
            keys = [
                [
                    Button.text(bot_text["reply"],resize=True)
                ],
                [
                    Button.text(bot_text["fantasy"]),
                    Button.text(bot_text["data_archive"])
                ],
                [
                    Button.text(bot_text["soon"]),
                    Button.text(bot_text["soon"]),
                    Button.text(bot_text["soon"]),
                ],
                [
                    Button.text(bot_text["back"])
                ]
            ]
            await event.reply(bot_text["select"],buttons=keys)
        elif text == bot_text["account"]:
            keys = [
                [
                    Button.text(bot_text["user_information"]),
                    Button.text(bot_text["personal_account"]),
                ],
                [
                    Button.text(bot_text["sub_collection"],resize=1)
                ],
                [
                    Button.text(bot_text["back"])
                ]
            ]
            await event.reply(bot_text["select"], buttons=keys)
        elif text == bot_text["search"]:
            keys = [
                Button.text(bot_text["search_in_channel"]),
                Button.text(bot_text["search_in_bot"],resize=True)
            ]
            await event.reply(bot_text["select"], buttons=keys)
        elif text == bot_text["search_in_channel"]:
            async with bot.conversation(user_id, timeout=1000) as conv:
                await conv.send_message(bot_text["enter_hashtag"])
                hashtag = await conv.get_response()
                query = f"SELECT * FROM hashtag WHERE text LIKE '%{hashtag.raw_text}%'"
                search = cur.execute(query).fetchall()
                if len(search) == 0:
                    key = Button.text(bot_text["back"],resize=True)
                    await conv.send_message(bot_text["not_found"],buttons=key)
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
                    key = Button.text(bot_text["back"],resize=True)
                    await conv.send_message(bot_text["not_found"],buttons=key)
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
                [Button.text(bot_text["small_party"]), Button.text(bot_text["big_party"]), Button.text(bot_text["you_pay"], resize=True)],
                [Button.text(bot_text["back"])]
            ]
            await event.reply(bot_text["select"], buttons=keys)
        elif text.startswith("/start") or text == bot_text["back"]:
            user = cur.execute(f"SELECT * FROM users WHERE id={user_id}").fetchone()
            if user is None:
                data = [
                    (user_id, None, False)
                ]
                cur.executemany(f"INSERT INTO users VALUES (?,?,?)", data)
                con.commit()
                keys = [
                    [Button.inline(bot_text["en"], b'lang:en'),
                     Button.inline(bot_text["fa"], b'lang:fa')
                     ]
                ]
                select = bot_text["select_lang"]
                await event.reply(select, buttons=keys)
            else:
                lang = user[1]
                if lang is None:
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
                        [Button.text(bot_text["protection"]), Button.text(bot_text["search"]), Button.text(bot_text["rules"])],

                    ]
                    if is_admin is not None:
                        keys = [
                            [Button.text(bot_text["panel"],resize=True)],
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
                    [Button.text(bot_text["words"],resize=True)],
                    [Button.text(bot_text['back'])]
                ]
                await event.reply(bot_text["select"], buttons=keys)
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
                        Button.text(bot_text["show_words"],resize=True),
                    ],
                    [Button.text(bot_text['back'])],
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
                                    (tag_word[0],tag_word[1])
                                ]
                                cur.executemany(f"INSERT INTO btn VALUES (?,?)", data)
                                con.commit()
                            await conv.send_message(bot_text["saved"])
                            await conv.cancel_all()
                        else:
                            tag_word = word.raw_text.split("_")
                            data_m = [
                                (tag_word[0],tag_word[1])
                            ]
                            cur.executemany(f"INSERT INTO btn VALUES (?,?)", data_m)
                            con.commit()
                            await conv.send_message(bot_text["saved"])
                            await conv.cancel_all()

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


bot.run_until_disconnected()
