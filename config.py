from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch, InputChannel
import re


API_ID = 86576
API_HASH = "385886b58b21b7f3762e1cde2d651925"
ENV = 1
if ENV:
    BOT_TOKEN = "7185706687:AAEkVBiMGDh0IigJs0iJBSSL1i7U7mN1e2k"
else:
    BOT_TOKEN = "6300653200:AAFK0BuvMPJ4kZV3gj_sbvXezciah_ga1B4"
PAY_TOKEN = "fced3227-3cf2-486f-95e7-52ee9e8fd77d"
SESSION_NAME = "bot"
if ENV:
    PROXY = False
else:
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
    "select": "یک دکمه را انتخاب کنید",
    "en": "🏴󠁧󠁢󠁥󠁮󠁧󠁿انگلیسی",
    "fa": "🇮🇷فارسی",
    "select_lang": "زبان ربات را انتخاب کنید",
    "archive": "صفحه اصلی",
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
    "not_found": "❗نتیجه ای پیدا نشد❗",
    "enter_button": "اسم دکمه یا بخشی از آن را وارد کنید:",
    "panel": "پنل ادمین",
    "words": "کلمات",
    "add_word": "اضافه کردن کلمه",
    "show_words": "مشاهده کلمات",
    "enter_word": "نام دکمه را وارد کنید:\n برای کنسل کردن کلمه کنسل را ارسال کنید",
    "saved": "با موفقیت ثبت شد✅",
    "welcome_show_words": "کلمات ثبت شده:",
    "delete_btn": "🗑",
    "edit_btn": "✏️ ",
    "word_text": "متن دکمه",
    "word_tag": "تگ دکمه",
    "come_next": "دکمه صفحه بندی",
    "enter_new_text": "متن جدید را وارد کنید",
    "edited": "با موفقیت تغییر کرد",
    "deleted": "با موفقیت حذف شد",
    "underline": "برای جستجو در دکمه های ربات اول عبارت خود _ یا خط تیره بگذارید",
    "reply": "بازپخش",
    "fantasy": "فانتزی",
    "data_archive": "آرشیو دیتا",
    "soon": "به زودی",
    "user_information": "اطلاعات کاربری",
    "personal_account": "حساب شخصی",
    "sub_collection": "زیر مجموعه گیری",
    "first_start": "ابتدا استارت کنید",
    "grand": "گرندپری",
    "add_grand": "افزودن",
    "show_grand": "مشاهده",
    "enter_grand": "نام گرندپری را به فارسی یا انگلیسی وارد کنید:",
    "enter_grand_num": "شماره راندی که مسابفه در این گرندپری برگزار شده را وارد کنید:\n مثل چین که راند 5 هست",
    "successfully": "با موفقیت ثبت شد",
    "welcome_show_grand": "گرندپری های ثبت شده:",
    "close_grand": "🔐",
    "delete_grand": "🗑",
    "grand_round": "راند گرندپری",
    "grand_name": "نام گرندپری",
    "grand_not_found": "گرندپری حذف شده است❗",
    "grand_opened": "با موفقیت باز شد",
    "grand_closed": "با موفقیت بسته شد",
    "scores": "پاور رنکینگ",
    "add_score": "ثبت امتیاز",
    "show_table": "مشاهده جدول",
    "grands_not_found": "گرندپری ها هنوز برای رای دادن ثبت نشده اند❗",
    "select_grand": "گرندپری مورد نظر خود را که میخواهید به راننده ها آن رای بدهید انتخاب کنید",
    "requesting_ergast": "درحال درخواست به ایرگست... لطفا منتظر باشید",
    "grand_is_close": "امتیاز دهی در این گرندپری متوقف شده است",
    "select_driver": "راننده های {gp}\n یکی از راننده ها را برای امتیاز دهی انتخاب کنید",
    "qualifying": "امتیاز مورد نظر خود را از 1 تا 10 برای عملکرد راننده در تعیین خط وارد کنید:",
    "race": "امتیاز مورد نظر خود را از 1 تا 10 برای عملکرد راننده در مسابقه وارد کنید:",
    "car": "امتیاز مورد نظر خود را از 1 تا 10 برای نسبت عملکرد راننده به ماشین وارد کنید:",
    "small_score": "حداقل امتیاز 1 میباشد",
    "big_score": "حداکثر امتیاز 10 میباشد",
    "you_scored": "شما قبلا به این راننده امتیاز داده اید",
    "select_see_grand": "گرندپری مورد نظر برای مشاهده امتیازات ثبت شده برای رانندگان را انتخاب کنید👇",
    "successfully_scored": "امتیاز شما با موفقیت ثبت شد✅",
    "name_already_exists": "گرندپری با این نام از قبل موجود است❗\n لطفا دوباره دکمه افزودن را بزنید و امتحان کنید",
    "round_already_exists": "گرندپری با این راند از قبل موجود است❗\n لطفا دوباره دکمه افزودن را بزنید و امتحان کنید",
    "robot_statistics": "آمار ربات",
    "statistics_text": "تعداد کاربران ربات: {users}",
    "": "",
    "": "",
    "": "",
}
