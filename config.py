from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch, InputChannel
import re


API_ID = 86576
API_HASH = "385886b58b21b7f3762e1cde2d651925"
ENV = 1
if ENV:
    BOT_TOKEN = "7185706687:AAEkVBiMGDh0IigJs0iJBSSL1i7U7mN1e2k"
    PROXY = False
    BOT_ID = "https://t.me/F1DataIQBot"
else:
    BOT_TOKEN = "6300653200:AAFK0BuvMPJ4kZV3gj_sbvXezciah_ga1B4"
    PROXY = True
    BOT_ID = "https://t.me/F1data_Test_bot"
PAY_TOKEN = "fced3227-3cf2-486f-95e7-52ee9e8fd77d"
SESSION_NAME = "bot"
PROXY_TYPE = "socks5"
PROXY_ADDRESS = "127.0.0.1"
PROXY_PORT = 10808
DB_NAME = "bot.db"
CHANNEL_ID = "https://t.me/F1DataOfficial"
CHANNEL_ID_PLUS = "https://t.me/RacePlusIran"
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

async def join_check_plus(user_id, cli):
    entity = await cli.get_entity(CHANNEL_ID_PLUS)
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


def check_number(num):
    try:
        # تبدیل ورودی به عدد اعشاری
        num = float(num)

        # بررسی عدد ۰.۵ به عنوان استثنا
        if num == 0.5:
            return True

        # بررسی محدوده عدد بین ۱ تا ۱۰
        if 1 <= num <= 10:
            # بررسی عدد صحیح
            if num.is_integer():
                return True
            # بررسی عدد اعشاری با قسمت اعشاری ۰.۵
            elif num - int(num) == 0.5:
                return True

        return False
    except ValueError:
        # اگر ورودی عدد نباشد
        return False


# bot texts
TEXT = {
    "EN_SELECTED": "زبان 🏴انگلیسی انتخاب شد",
    "FA_SELECTED": "زبان 🇮🇷فارسی انتخاب شد",
    "Membership_Confirmation": "تایید عضویت",
    "pls_join": "برای استفاده از ربات ابتدا در کانال زیر عضو شوید سپس دوباره استارت کنید",
    "big_heart": "قلب بزرگ",
    "rules": "تنظیمات",
    "rules_show": "قوانین فنی",
    "protection": "حمایت",
    "language": "زبان ربات",
    "rules_text": "متن قوانین",
    "coffee": "مهمان قهوه ات",
    "dinner": "شام آخر",
    "small_party": "جشن کوچک",
    "big_party": "جشن بزرگ",
    "you_pay": "تو پرداخت کن",
    "back": "بازگشت",
    "select": "یک دکمه را انتخاب کنید",
    "en": "English 🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "fa": "🇮🇷فارسی",
    "select_lang": "زبان ربات را انتخاب کنید",
    "archive": "صفحه اصلی",
    "account": "حساب کاربری",
    "support": "پشتیبانی",
    "search": "جستجو",
    "top_speed": "سرعت",
    "option": "شما قبلا از این آپشن استفاده کرده اید!",
    "enter_amount": "لطفا مبلغ را به ریال وارد کنید . حداقل مبلغ 1000 ریال و حداکثر مبلغ 500,000,000 ریال است",
    "small_amount": "مبلغ کمتر از حداقل مقدار است.لطفا مبلغ 1000 ریال یا بیشتر را وارد کنید:",
    "big_amount": "مبلغ بیشتر از حد مجاز است لطفا مبلغ کمتری وارد کنید:",
    "just_num": "فقط عدد وارد کنید",
    "name": "نام پرداخت کننده را وارد کنید: \n برای کنسل کردن در هر مرحله کلمه کنسل را ارسال کنید!",
    "dont_image": "پرداخت کنسل شد! لطفا دوباره دکمه را بزنید و مقادیر درست وارد کنید",
    "cancel": "کنسل",
    "select_year": "سال را انتخاب کنید:",
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
    "fantasy": "لیگ فانتزی",
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
    "loading": "درحال دریافت اطلاعات...",
    "statistics_text": "تعداد کاربران ربات: {users}",
    "try_again": "عدد شما درست نیست! مجدد تلاش کنید",
    "sub_link": "هر نفر که با لینک زیر ربات رو استارت کنه یک امتیاز زیر مجموعه گیری به شما داده میشود👇\n{link}",
    "timeout_error": "زمان پاسخگویی تمام شده است!\nلطفا مجدد تلاش کنید",
    "select_gp": "گرندپری را انتخاب کنید:",
    "select_session": "لطفا رویداد را انتخاب کنید:",
    "pls_join_plus": "لطفا برای استفاده از دکمه پاور رنکینگ در کانال زیر عضو شوید و سپس مجدد پاور رنکینگ را بزنید",
    "account_setup": "تنظیم اکانت",
    "bot_ping": "پینگ ربات",
    "coming_soon": "این بخش بزودی فعال خواهد شد",
    "getting_ping": "درحال دریافت پینگ...",
    "overtake": "سبقت گرفتن",
    "map_viz": "مپ ویز",
    "ask_driver": "راننده مورد نظر خود را انتخاب کنید:",
    "ask_state": "حالت پرسش مورد نظر را انتخاب کنید:\nحالت 1:تک سواله\nحالت 2:چند سواله",
    "ask_performance": "به عملکرد راننده از 1 تا 10 امتیاز بدهید:",
    "new_users": "کاربران جدید",
    "users_excel": "اکسل کاربران",
    "users_excel_caption": "فایل اکسل کاربران ربات",
    "dont_time": "مسابقه هنوز شروع نشده است!"
}

EN_TEXT = {
    "EN_SELECTED": "English 🏴󠁧󠁢󠁥󠁮󠁧󠁿 󠁧󠁢󠁥󠁮language was selected",
    "FA_SELECTED": "Persian 🇮🇷 language was selected",
    "Membership_Confirmation": "confirmation✅",
    "pls_join": "To use the robot, first subscribe to the following channel, then start again",
    "big_heart": "Big heart",
    "rules": "Settings",
    "rules_show": "Technical rules",
    "protection": "Protection",
    "language": "Bot language",
    "rules_text": "Rules text",
    "coffee": "Your coffee guest",
    "dinner": "The last supper",
    "small_party": "Small party",
    "big_party": "Big party",
    "you_pay": "You pay",
    "back": "Back",
    "select": "Select a button:",
    "en": "English 🏴󠁧󠁢󠁥󠁮󠁧󠁿󠁧󠁢󠁥󠁮󠁧󠁿",
    "fa": "🇮🇷فارسی",
    "select_lang": "Select the language of the bot",
    "archive": "Main page",
    "account": "Account",
    "support": "Support",
    "search": "Search",
    "option": "You have already used this option!",
    "enter_amount": "Please enter the amount in Rials. The minimum amount is 1000 Rials and the maximum amount is "
                    "500,000,000 Rials",
    "small_amount": "The amount is less than the minimum amount. Please enter the amount of 1000 rials or more:",
    "big_amount": "The amount is more than the limit, please enter a lower amount:",
    "just_num": "Just enter the number",
    "name": "Enter the name of the payer: \n To cancel at any stage, send the word cancel!",
    "dont_image": "Payment canceled! Please click the button again and enter the correct values",
    "cancel": "Cancel",
    "canceled": "Canceled successfully",
    "phone": "Enter the payer's phone number: \n To cancel, send the word cancel!",
    "email": "Enter the payer's email: \n To cancel, send the word cancel!",
    "desc": "Enter description: \n To cancel send the word cancel!",
    "success_pay": "Payment Done",
    "pay_link": """Your payment gateway has been created: \n
{}

**Note**: Please login to the robot no later than 10 minutes after payment and press the button below "Payment Done", 
otherwise the payment will not be confirmed and the money will be returned to your account.""",
    "pay_verified": "The payment was confirmed and the rewards that the employer says later were placed for you",
    "dont_pay": "Payment has not been made yet",
    "search_in_channel": "Search in channel",
    "search_in_bot": "Search in bot",
    "enter_hashtag": "Enter your desired hashtag to search the channel with or without # 👇",
    "not_found": "❗No results found❗",
    "select_year": "Select year:",
    "enter_button": "Enter the name of the button or part of it:",
    "panel": "Admin panel",
    "words": "Words",
    "add_word": "Add word",
    "show_words": "Show words",
    "enter_word": "Enter the name of the button:\n To cancel, send the word cancel",
    "saved": "Successfully registered✅",
    "welcome_show_words": "Registered words:",
    "delete_btn": "🗑",
    "edit_btn": "✏️ ",
    "top_speed": "Top speed",
    "word_text": "Button text",
    "word_tag": "Button tag",
    "come_next": "Paging button",
    "enter_new_text": "Enter new text:",
    "edited": "Changed successfully",
    "deleted": "Removed successfully",
    "underline": "To search in bot buttons, put _ or hyphen in your first phrase",
    "reply": "Replay",
    "fantasy": "Fantasy league",
    "data_archive": "Data archive",
    "soon": "Soon",
    "user_information": "User information",
    "personal_account": "Personal account",
    "sub_collection": "Sub collection",
    "first_start": "Start first",
    "grand": "Grand prix",
    "add_grand": "Add",
    "show_grand": "View",
    "enter_grand": "Enter the name of the Grand Prix in Farsi or English:",
    "enter_grand_num": "Enter the number of the round in which the race was held in this Grand Prix:\n "
                       "like China, which is round 5",
    "successfully": "Successfully registered",
    "welcome_show_grand": "Registered Grand Prix:",
    "close_grand": "🔐",
    "delete_grand": "🗑",
    "grand_round": "Grand prix round",
    "grand_name": "Grand prix name",
    "grand_not_found": "The Grand Prix has been removed❗",
    "grand_opened": "Opened successfully",
    "grand_closed": "Closed successfully",
    "scores": "Power ranking",
    "add_score": "Register points",
    "show_table": "View table",
    "grands_not_found": "The Grand Prix are not yet registered for voting❗",
    "select_grand": "Select the Grand Prix you want to vote for the drivers",
    "requesting_ergast": "Applying to Ergast... please wait",
    "grand_is_close": "Scoring has been stopped in this Grand Prix",
    "select_driver": "{gp} drivers of\n Select one of the drivers to rate",
    "qualifying": "Enter your desired score from 1 to 10 for the driver's lane marking performance:",
    "race": "Enter your desired score from 1 to 10 for the driver's performance in the race:",
    "car": "Enter your desired score from 1 to 10 for driver to car performance ratio:",
    "small_score": "The minimum score is 1",
    "big_score": "The maximum score is 10",
    "you_scored": "You have already rated this driver",
    "select_see_grand": "Select the desired grand prix to view the points recorded for the drivers👇",
    "successfully_scored": "Your score has been registered successfully✅",
    "name_already_exists": "A Grand Prix with this name already exists❗\n Please hit the add button again and try",
    "round_already_exists": "The Grand Prix is already available with this round❗"
                            "\n Please hit the add button again and try",
    "robot_statistics": "Bot statistics",
    "statistics_text": "Number of bot users: {users}",
    "try_again": "Your number is not correct! Try again",
    "sub_link": "Every person who starts the robot with the link below will be given a collection point 👇\n{link}",
    "timeout_error": "Response time is over!\nPlease try again",
    "select_gp": "Please select grand prix:",
    "select_session": "Please select event:",
    "loading": "Loading data...",
    "pls_join_plus": "Please subscribe to the channel below to use the power ranking button and then click power ranking again.",
    "account_setup": "Account setup",
    "bot_ping": "Bot ping",
    "coming_soon": "This section will be activated soon",
    "getting_ping": "Receiving ping...",
    "overtake": "Overtake",
    "map_viz": "Map viz",
    "ask_driver": "please select driver:",
    "ask_state": "Select the desired question mode:\nMode 1: Single question\nMode 2: Multiple questions",
    "ask_performance": "Give the driver's performance from 1 to 10 points:",
    "new_users": "New users",
    "users_excel": "Excel Users",
    "users_excel_caption": "Excel file of robot users",
    "dont_time": "The race has not started yet!"
}
