from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch, InputChannel
import re


API_ID = 86576
API_HASH = "385886b58b21b7f3762e1cde2d651925"
BOT_TOKEN = "7185706687:AAEkVBiMGDh0IigJs0iJBSSL1i7U7mN1e2k"
PAY_TOKEN = "fced3227-3cf2-486f-95e7-52ee9e8fd77d"
SESSION_NAME = "bot"
PROXY = True
PROXY_TYPE = "socks5"
PROXY_ADDRESS = "127.0.0.1"
PROXY_PORT = 10808
DB_NAME = "bot.db"
CHANNEL_ID = "https://t.me/F1DataOfficial"
BOT_ID = "https://t.me/F1DataIQBot"
CALLBACK_URL = "https://f1datas.com/payment"


async def join_check(user_id, cli):
    entity = await cli.get_entity(CHANNEL_ID)
    access_hash = entity.access_hash
    channel_id = entity.id
    participants = await cli(GetParticipantsRequest(
        channel=InputChannel(channel_id, access_hash),
        filter=ChannelParticipantsSearch(''),
        offset=0,
        limit=1000000000,
        hash=0
    ))
    result = False
    for p in participants.participants:
        if user_id == p.user_id:
            result = True
    return result, entity


def extract_hashtags(text):
    # the regular expression
    regex = "#(\w+)"

    # extracting the hashtags
    hashtag_list = re.findall(regex, text)
    return hashtag_list
# bot texts
TEXT = {
    "EN_SELECTED": "زبان 🏴󠁧󠁢󠁥󠁮󠁧󠁿انگلیسی انتخاب شد",
    "FA_SELECTED": "زبان 🇮🇷فارسی انتخاب شد",
    "Membership_Confirmation": "تایید عضویت",
    "pls_join": "برای استفاده از ربات ابتدا در کانال زیر عضو شوید سپس دوباره استارت کنید",
    "big_heart": "قلب بزرگ",
    "rules": "قوانین",
    "protection": "حمایت",
    "rules_text": "متن قوانین",
    "coffee": "مهمان قهوه ات",
    "dinner": "شام آخر",
    "small_party": "جشن کوچک",
    "big_party": "جشن بزرگ",
    "you_pay": "تو پرداخت کن",
    "back": "بازگشت",
    "select": "یکی رو انتخاب کن:",
    "en": "🏴󠁧󠁢󠁥󠁮󠁧󠁿انگلیسی",
    "fa": "🇮🇷فارسی",
    "select_lang": "زبان ربات را انتخاب کنید",
    "archive": "آرشیو",
    "account": "حساب کاربری",
    "support": "پشتیبانی",
    "search": "جستجو",
    "option": "شما قبلا از این آپشن استفاده کرده اید!",
    "enter_amount": "لطفا مبلغ را به ریال وارد کنید . حداقل مبلغ 1000 ریال و حداکثر مبلغ 500,000,000 ریال است",
    "small_amount": "مبلغ کمتر از حداقل مقدار است.لطفا مبلغ 1000 ریال یا بیشتر را وارد کنید:",
    "big_amount": "مبلغ بیشتر از حد مجاز است لطفا مبلغ کمتری وارد کنید:",
    "just_num": "فقط عدد وارد کنید",
    "name": "نام پرداخت کننده را وارد کنید: \n برای کنسل کردن در هر مرحله کلمه کنسل را ارسال کنید!",
    "dont_image": "پرداخت کنسل شد! لطفا دوباره دکمه را بزنید و مقادیر درست وارد کنید",
    "cancel": "کنسل",
    "canceled": "با موفقیت کنسل شد",
    "phone": "شماره تلفن پرداخت کننده را وارد کنید: \n برای کنسل کردن کلمه کنسل را ارسال کنید!",
    "email": "ایمیل پرداخت کننده را وارد کنید: \n برای کنسل کردن کلمه کنسل را ارسال کنید!",
    "desc": "توضیحات را وارد کنید: \n برای کنسل کردن کلمه کنسل را ارسال کنید!",
    "success_pay": "پرداخت انجام شد",
    "pay_link": """درگاه پرداخت شما ساخته شد: \n
{}
 
**توجه**: لطفا تا قبل از حداکثر ۱۰ دقیقه بعد از پرداخت وارد ربات شوید و دکمه زیر "پرداخت انجام شد" رو بزنید در‌ غیر این صورت پرداخت تایید نمیشود و پول به حساب شما باز می‌گردد """,
    "pay_verified": "پرداخت تایید شد و جایزه هایی که بعدا کارفرما میگه برای شما قرار داده شد",
    "dont_pay": "تا کنون پرداخت انجام نشده است",
    "search_in_channel": "جستجو در کانال",
    "search_in_bot": "جستجو در ربات",
    "enter_hashtag": "هشتگ مورد نظر خود را برای جستجو در کانال با # یا بدون آن وارد کنید👇",
    "not_found": "❗نتیجه ای پیدا نشد❗"

}
