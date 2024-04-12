from telethon.sync import TelegramClient, events, Button
import requests
from random import randint
import string
import random
from telethon.tl.functions.channels import GetParticipantsRequest, GetFullChannelRequest
from telethon.tl.types import ChannelParticipantsSearch, InputChannel
from telethon.tl.types import PeerUser, PeerChat, PeerChannel

api_id = 86576
api_hash="385886b58b21b7f3762e1cde2d651925"
bot_token = '7185706687:AAEkVBiMGDh0IigJs0iJBSSL1i7U7mN1e2k'
pay_token = "fced3227-3cf2-486f-95e7-52ee9e8fd77d"
bot = TelegramClient('bot', api_id, api_hash)
# Create an instance of the TelegramClient
bot.start(bot_token=bot_token)
import sqlite3
con = sqlite3.connect("bot.db")
cur = con.cursor()

@bot.on(events.CallbackQuery())
async def call_handler(event):
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
    join_channel_id = "https://t.me/F1DataOfficial"
    entity = await bot.    get_entity(join_channel_id)
    access_hash = entity.access_hash
    channel_id = entity.id
    user = await bot.get_entity(user_id)
    username = user.username
    participants = await bot(GetParticipantsRequest(
                channel=InputChannel(channel_id, access_hash),
                filter=ChannelParticipantsSearch(''),
                offset=0,
                limit=1000000000,
                hash=0
            ))
    ps = False
    for p in participants.participants:
        if user_id == p.user_id:
            ps = True
    if ps:
        msg_id = event.original_update.msg_id
        if event.data == b'lang:en':
            en = 1
            up_en = cur.execute(f"UPDATE users SET lang = {en} WHERE id={user_id}")
            con.commit()
            en = "زبان 🏴󠁧󠁢󠁥󠁮󠁧󠁿انگلیسی انتخاب شد"
            await bot.delete_messages(user_id,msg_id)
            await bot.send_message(user_id, en)
        elif event.data == b'lang:fa':
                
                fa = 2
                up_fa = cur.execute(f"UPDATE users SET lang = {fa} WHERE id={user_id}")
                con.commit()
                fa = "زبان 🇮🇷فارسی انتخاب شد"
                await bot.delete_messages(user_id,msg_id)
                await bot.send_message(user_id, fa)
     
    else:
                            full_info = await bot(GetFullChannelRequest(entity))
                            chat_title = full_info.chats[0].title
                            channel_username = full_info.chats[0].username
                            if channel_username is None:
                                channel_username = full_info.full_chat.exported_invite.link
                            else:
                                channel_username = f'https://t.me/{channel_username}'
                                key = [
                                    Button.url(text=chat_title, url=channel_username)
                                ]
                                await event.reply("برای استفاده از ربات ابتدا در کانال زیر عضو شوید سپس دوباره استارت کنید", buttons=key)
@bot.on(events.NewMessage())
async def pay(event):
            user_id = event.sender_id
            text = event.raw_text
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
            join_channel_id = "https://t.me/F1DataOfficial"
            entity = await bot.    get_entity(join_channel_id)
            access_hash = entity.access_hash
            channel_id = entity.id
            user = await bot.get_entity(user_id)
            username = user.username
            participants = await bot(GetParticipantsRequest(
                channel=InputChannel(channel_id, access_hash),
                filter=ChannelParticipantsSearch(''),
                offset=0,
                limit=1000000000,
                hash=0
            ))
            ps = False
            for p in participants.participants:
                if user_id == p.user_id:
                    ps = True
            
            
            if ps == False:
                full_info = await bot(GetFullChannelRequest(entity))
                chat_title = full_info.chats[0].title
                channel_username = full_info.chats[0].username
                if channel_username is None:
                    channel_username = full_info.full_chat.exported_invite.link
                else:
                    channel_username = f'https://t.me/{channel_username}'
                key = [
                    Button.url(text=chat_title, url=channel_username)
                ]
                await event.reply("برای استفاده از ربات ابتدا در کانال زیر عضو شوید سپس دوباره استارت کنید", buttons=key)
            else:
                
                user = cur.execute(f"SELECT * FROM users WHERE id={user_id}").fetchone()
                text = event.raw_text
                amount = 0
                end = False
                you = False
                pay = False
                if text == "قلب بزرگ":
                    amount = 2000000
                    pay = True
                elif text == "قوانین":
                    await event.reply("متن قوانین")
                elif text == "حمایت":
                        
                        keys = [
    [Button.text("قلب بزرگ")],
    [Button.text("مهمان قهوه ات"),Button.text("شام آخر" )],
    [Button.text("جشن کوچک"),Button.text("جشن بزرگ"),Button.text("تو حساب کن",resize=True)]
    ]
                        await event.reply("یکی رو انتخاب کن:",buttons=keys)
                elif text == "/start":
                        
                        user = cur.execute(f"SELECT * FROM users WHERE id={user_id}").fetchone()
                        print(user)
                        if user is None:
                            data = [
                                (user_id, None,False)
                            ]
                            cur.executemany(f"INSERT INTO users VALUES (?,?,?)",data)
                            con.commit()
                            keys = [
                                [Button.           inline("🏴󠁧󠁢󠁥󠁮󠁧󠁿انگلیسی",b'lang:en'),
                                Button.inline("🇮🇷فارسی",                            b'lang:fa')
                                ]
                            ]
                            select = "زبان ربات را انتخاب کنید"
                            await event.reply(select, buttons=keys)
                        else:
                            lang = user[1]
                            if lang is None:
                    
                                keys = [
                                    [Button.      inline("🏴󠁧󠁢󠁥󠁮󠁧󠁿انگلیسی",b'lang:en'),
                                Button.inline("🇮🇷فارسی",b'lang:fa')
                                 ]
                                ]
                                select = "زبان ربات را انتخاب کنید"
                                await event.reply(select, buttons=keys)
                            else:
                                keys = [
                                [Button.text("آرشیو",resize=True)],
                                [Button.text("حساب کاربری"),Button.text("پشتیبانی")],
                                [Button.text("حمایت"),Button.text("جستجو"),Button.text("قوانین")]
                                ]
                                await event.reply(f"انتخاب کنید",buttons=keys)
                elif text == "مهمان قهوه ات":
                    amount = 100000
                    pay = True
                elif text == "جشن کوچک":
                    amount = 500000
                    pay = True
                elif text == "جشن بزرگ":
                    amount = 1000000
                    pay = True
                elif text == "تو حساب کن":
                    you = True
                    pay = True
                elif text == "شام آخر":
                    amount = 500000
                    end = True
                    pay = True
                if end == True:
                    user_end = user[2]
                    if user_end:
                        await event.reply("شما قبلا از این آپشن استفاده کرده اید!")
                        return
                if pay == True:
                        
                    print(amount / 10)
                    print(end)
                    print(you)
                    async with bot.conversation(user_id, timeout=1000) as conv:
                        
                        if you == True:
                            
                            await conv.send_message("لطفا مبلغ را به ریال وارد کنید . حداقل مبلغ 1000 ریال و حداکثر مبلغ 500,000,000 ریال است")
                            while True:
                                try:
                                    amount = await conv.get_response()
                                    amount = amount.raw_text
                                    if int(amount) < 1000:
                                        await conv.send_message("مبلغ کمتر از حداقل مقدار است.لطفا مبلغ 1000 ریال یا بیشتر را وارد کنید:" )
                                    elif int(amount) > 500000000:
                                        await conv.send_message("مبلغ بیشتر از حد مجاز است ‌ لطفا مبلغ کمتری وارد کنید:")
                                    else:
                                        break
                                except ValueError:
                                        
                                        
                                        await conv.send_message("فقط عدد وارد کنید")
                        await conv.send_message("نام پرداخت کننده را وارد کنید: \n برای کنسل کردن در هر مرحله کلمه کنسل را ارسال کنید!")
                        name = await conv.get_response()
                        if name.media is not None:
                           await conv.send_message("پرداخت کنسل شد! لطفا دوباره دکمه را بزنید و مقادیر درست وارد کنید")
                           return
                        if name.raw_text == "کنسل":
                            await conv.send_message("با موفقیت کنسل شد")
                            return
                        pay_num = randint(10000,99999)
                        await conv.send_message("شماره تلفن پرداخت کننده را وارد کنید: \n برای کنسل کردن کلمه کنسل را ارسال کنید!")
                        phone = await conv.get_response()
                        if phone.media is not None:
                            await conv.send_message("پرداخت کنسل شد! لطفا دوباره دکمه را بزنید و مقادیر درست وارد کنید")
                            return
                        if phone.raw_text == "کنسل":
                            await conv.send_message("با موفقیت کنسل شد")
                            return
                        await conv.send_message("ایمیل پرداخت کننده را وارد کنید: \n برای کنسل کردن کلمه کنسل را ارسال کنید!")
                        mail = await conv.get_response()
                        if mail.media is not None:
                            await conv.send_message("پرداخت کنسل شد! لطفا دوباره دکمه را بزنید و مقادیر درست وارد کنید")
                            return
                        if mail.raw_text == "کنسل":
                            await conv.send_message("با موفقیت کنسل شد")
                            return
                        await conv.send_message("توضیحات   را وارد کنید: \n برای کنسل کردن کلمه کنسل را ارسال کنید!")
                        desc = await conv.get_response()
                        if desc.media is not None:
                            await conv.send_message("پرداخت کنسل شد! لطفا دوباره دکمه را بزنید و مقادیر درست وارد کنید")
                            return
                        if desc.raw_text == "کنسل":
                            await conv.send_message("با موفقیت کنسل شد")
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
                             'callback': 'https://f1datas.com/',
                        }

                        response = requests.post('https://api.idpay.ir/v1.1/payment',headers=headers, json=json_data)
                        res = response.json()
                        print(response.json())
                        link = res["link"]
                        pay_id =res["id"]
                        data =[
                         (user_id, pay_id, pay_num, text)
                        ]
                        cur.executemany("INSERT INTO pay VALUES(?,?,?,?)", data)
                        print(data)
                        con.commit()
                        data = str.encode("pay_true:" + str(pay_num))
                        key = Button.inline("پرداخت انجام شد", data)
                        text = """"درگاه پرداخت شما ساخته شد: \n
{}
 
**توجه**: لطفا تا قبل از حداکثر ۱۰ دقیقه بعد از پرداخت وارد ربات شوید و دکمه زیر "پرداخت انجام شد" رو بزنید در‌ غیر این صورت پرداخت تایید نمیشود و پول به حساب شما باز می‌گردد """.format(link)
                        await event.reply(text, buttons=key)
                            
                            
@bot.on(events.CallbackQuery(pattern="pay_true:*"))
async def pay_hand(event):
    msg_id = event.original_update.msg_id
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
    join_channel_id = "https://t.me/F1DataOfficial"
    entity = await bot.    get_entity(join_channel_id)
    access_hash = entity.access_hash
    channel_id = entity.id
    user = await bot.get_entity(user_id)
    username = user.username
    participants = await bot(GetParticipantsRequest(
                channel=InputChannel(channel_id, access_hash),
                filter=ChannelParticipantsSearch(''),
                offset=0,
                limit=1000000000,
                hash=0
            ))
    ps = False
    for p in participants.participants:
        if user_id == p.user_id:
            ps = True
    if ps:
        order_id = event.data.decode().split(":")[1]
        pay = cur.execute(f"SELECT * FROM pay WHERE order_id={order_id}").fetchone()
        pay_id = pay[1]
        pay_num = pay[2]
        print(pay_id, pay_num)
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

                response_v = requests.post("https://api.idpay.ir/v1.1/payment/verify", headers=headers,json=json_data)
                print(response.json())
                if response_v.json()["status"] == 100:
                   await bot.delete_messages(user_id, msg_id)
                   if pay[3] == "شام آخر":
                       print("areh")
                       cur.execute(f"UPDATE users SET lastd = {True} WHERE id={user_id}")
                       con.commit()
                   await event.reply("پرداخت تایید شد و جایزه هایی که بعدا کارفرما میگه برای شما قرار داده شد")
                   return
        else:
          
              await event.reply("تا کنون پرداخت انجام نشده است")
              return
    else:
                        full_info = await bot(GetFullChannelRequest(entity))
                        chat_title = full_info.chats[0].title
                        channel_username = full_info.chats[0].username
                        if channel_username is None:
                            channel_username = full_info.full_chat.exported_invite.link
                        else:
                            channel_username = f'https://t.me/{channel_username}'
                            key = [
                            Button.url(text=chat_title, url=channel_username)
                            ]
                            await event.reply("برای استفاده از ربات ابتدا در کانال زیر عضو شوید سپس دوباره استارت کنید", buttons=key)
bot.run_until_disconnected()
