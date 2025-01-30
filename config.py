from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch, InputChannel
import re
import sqlite3

con = sqlite3.connect("bot.db")
cur = con.cursor()

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
PROXY_PORT = 2080
DB_NAME = "bot.db"
CHANNEL_ID = "https://t.me/F1DataOfficial"
ergast = True
try:
    CHANNEL_ID_PLUS = cur.execute(f"SELECT channel_id FROM join_channel WHERE senior = {True}").fetchone()[0]
except TypeError:
    CHANNEL_ID_PLUS = None
CALLBACK_URL = "https://f1datas.com/payment"
IDEALIZATION_CHANNEL = "https://t.me/+0OOAnBCTM-sxOTlk"
START_SCORE = 10
DAILY_COIN = 2
SUB_COIN = 10
DATA_MONEY = 2
REPLY_CHANNEL = 2475588093


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
    if CHANNEL_ID_PLUS is None:
        return True, None
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


def all_statistics(where, user_id):
    cur.execute(f"INSERT INTO statistics_all VALUES ('{where}', {user_id})")
    con.commit()
def small_statistics(where, user_id):
    find_user = cur.execute(f"SELECT * FROM statistics_small WHERE user_id = '{user_id}'").fetchone()
    print(find_user)
    if find_user is None:
        cur.execute(f"INSERT INTO statistics_small VALUES ('{where}', '{user_id}')")
        con.commit()
    else:
        return
# bot texts
TEXT = {
    "EN_SELECTED": "زبان 🏴انگلیسی انتخاب شد",
    "FA_SELECTED": "زبان 🇮🇷فارسی انتخاب شد",
    "Membership_Confirmation": "تایید عضویت",
    "pls_join": "برای استفاده از ربات ابتدا در کانال زیر عضو شوید سپس دوباره استارت کنید",
    "big_heart": "قلب بزرگ",
    "rules": "تنظیمات",
    "copy_right": "کپی رایت",
    "rules_show": "قوانین",
    "technical_rules": "قوانین فنی",
    "protection": "حمایت",
    "language": "زبان ربات",
    "rules_text": """💫 - کاربر گرامی به بخش قوانین ربات خوش آمدید.

❗️ قوانین فنی:

- خواهشمندیم به منظور جلوگیری از مشکلات فنی، قبلی اسپم و عدم سرعت مناسب پاسخگویی از ارسال تعداد زیادی درخواست به صورت خودکار خودداری می کنید.

- اطلاعات و دیتا ها به صورت خودکار از طریق، دیتا سنتر ها و API به ربات متصل می شود، پس درستی آن توسط خود کاربران می بایست تایید شود. ربات مسئولیتی در خصوص این موارد نخواهد داشت.

- از ارسال غیرقانونی، ناپسند یا نامناسب خودداری، در صورتی که فعالیت های مشکوک توسط ربات مسدود شد.

- از انتشار اطلاعات شخصی خود و دیگران در فضای ارتباطی، خودداری، این اطلاعات در ربات محفوظ می ماند. در صورت دیده شدن انتشار اطلاعات شخصی در مکانی به جزء ربات، باعث مسدود شدن شما می شود.

- از انتشار بدون ذکر منبع، خودداری می کنید. در صورت دیده شدن این موارد، توسط ربات مسدود شد.

- در صورت بروز مشکل یا نیاز به راهنمایی، با پشتیبانی ربات تماس بگیرید.

- در صورت دیدن هر گونه تخلف از قوانین، به مدیران گزارش می دهند تا انجام شود.

🆔 @F1DATAIQBOT""",
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
    "archive": "خانه دیتا",
    "account": "حساب کاربری",
    "support": "پشتیبانی",
    "search": "جستجو",
    "top_speed": "Top Speed / Speed Trap",
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
    "senior_channel": "⬆️",
    "word_text": "متن دکمه",
    "word_tag": "تگ دکمه",
    "come_next": "دکمه صفحه بندی",
    "enter_new_text": "متن جدید را وارد کنید",
    "edited": "با موفقیت تغییر کرد",
    "deleted": "با موفقیت حذف شد",
    "underline": "برای جستجو در دکمه های ربات اول عبارت خود _ یا خط تیره بگذارید",
    "reply": "بازپخش مسابقات",
    "fantasy": "لیگ فانتزی",
    "data_archive": "خانه دیتا",
    "soon": "به زودی",
    "user_information": "اطلاعات کاربری",
    "personal_account": "حساب شخصی",
    "sub_collection": "زیر مجموعه گیری",
    "first_start": "ابتدا استارت کنید",
    "grand": "مدیریت پاور رنکینگ",
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
    "show_table": "امتیازات",
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
    "robot_statistics": "آمار کاربران",
    "loading": "درحال دریافت اطلاعات...\nسال:{year}\nگرندپری:{gp}\nرویداد:{event}",
    "statistics_text": "تعداد کاربران ربات: {users}",
    "try_again": "عدد شما درست نیست! مجدد تلاش کنید",
    "sub_link": "🔹 با ورود هر کاربر از طریق لینک زیرمجموعه گیری، شما 10 سکه رایگان دریافت خواهید کرد.\n- لینک زیرمجموعه گیری شما:\n{link}",
    "timeout_error": "زمان پاسخگویی تمام شده است!\nلطفا مجدد تلاش کنید",
    "select_gp": "گرندپری را انتخاب کنید:",
    "select_session": "لطفا رویداد را انتخاب کنید:",
    "pls_join_plus": "لطفا برای استفاده از دکمه پاور رنکینگ در کانال زیر عضو شوید و سپس مجدد پاور رنکینگ را بزنید",
    "account_setup": "تنظیم اکانت",
    "bot_ping": "پینگ ربات",
    "coming_soon": "این بخش بزودی فعال خواهد شد",
    "getting_ping": "درحال دریافت پینگ...",
    "overtake": "Overtake",
    "map_viz": "Map Speed Viz",
    "ask_driver": "راننده مورد نظر خود را انتخاب کنید:",
    "ask_state": "حالت پرسش مورد نظر را انتخاب کنید:\nحالت 1:تک سواله\nحالت 2:چند سواله",
    "ask_performance": "به عملکرد راننده از 1 تا 10 امتیاز بدهید:",
    "new_users": "کاربران جدید",
    "users_excel": "اکسل کاربران",
    "users_excel_caption": "فایل اکسل کاربران ربات",
    "dont_time": "مسابقه هنوز شروع نشده است!",
    "idealization": "ایده پردازی",
    "connect_admin": "ارتباط با پشتیبانی",
    "question_image": "در صورت نیاز به تصویر ، تصویر را ارسال کنید(اگر به تصویر نیاز ندارید متن تیکت خود را ارسال کنید)"
                      "\n برای لغو عملیات ثبت تیکت **کنسل** را ارسال کنید❗",
    "question_text": "متن خود را وارد کنید:👇",
    "ticket_successfully": "تیکت با موفقیت ثبت شد✅\nدر اسرع وقت به تیکت پاسخ داده خواهد شد✅",
    "ticket_answer": "📮ثبت پاسخ📮",
    "admin_notification": "تیکت جدیدی ثبت شد❗\nمتن تیکت:{text}\nشماره تیکت:{num}\nآیدی عددی کاربر:`{id}`\nنام فرد درخواست کننده:{name}\nآیدی فرد درخواست کننده:{username}",
    "ticket_dl_error": "❗این تیکت حذف شده است❗",
    "close_error": "❗این تیکت بسته شده است❗",
    "question_image_answer": "در صورت نیاز به تصویر ، تصویر را ارسال کنید"
                             "(اگر به تصویر نیاز ندارید متن پاسخ خود را ارسال کنید)"
                             " \n برای لغو عملیات ثبت پاسخ **کنسل** را ارسال کنید❗",
    "ticket_answer_ad": "📮ثبت پاسخ برای ادمین📮",
    "answer_successfully": "پاسخ با موفقیت ثبت شد✅\nپاسخ به تیکت شماره:{num}",
    "user_notification":
        "پاسخی از طرف ادمین برای تیکت شما ارسال شد!\nمتن تیکت شما:{user_text}\n\n**پاسخ ادمین**:{admin_text}",
    "answer_successfully_user": "✅پاسخ با موفقیت برای ادمین ارسال شد✅",
    "admin_notification_answer": "پاسخ جدیدی از طرف کاربران ثبت شد❗"
                                 "\nمتن پاسخ:{text}\nبر روی تیکت شماره:{num}\nآیدی عددی کاربر:`{id}`\nنام فرد:{name}\nآیدی فرد:{username}",
    "question_image_idea": "درصورت نیاز به تصویر، تصویر خود را ارسال کنید:\nدر غیر این صورت متن ایده خود را ارسال کنید:",
    "question_text_idea": "متن ایده خود را ارسال کنید:\nبرای لغو کلمه *کنسل* را ارسال کنید",
    "management": "مدیریت عمومی",
    "users": "مدیریت کاربران",
    "data_management": "مدیریت دیتا",
    "tickets": "مشاهده تیکت",
    "welcome_show_tickets": "تیکت های ثبت شده:👇",
    "ticket_text": "📝متن تیکت:",
    "ticket_count": "🔄شماره تیکت:",
    "ticket_user_id": "آیدی عددی کاربر:",
    "close_ticket": "🔐بستن تیکت🔐",
    "ticket_not_found": "تیکت حذف شده است❗",
    "ticket_opened": "تیکت با موفقیت باز شد✅",
    "ticket_closed": "تیکت با موفقیت بسته شد✅",
    "rpm": "RPM Chart",
    "ask_driver_one": "راننده اول را انتخاب کنید:",
    "ask_driver_two": "راننده دوم را انتخاب کنید:",
    "map_break": "Map Brake Viz",
    "lap_times": "Plot Lap Times",
    "start_score": f"تعداد {START_SCORE} سکه به حساب کاربری شما اضافه شد",
    "daily_coin": f"مقدار {DAILY_COIN} سکه روزانه به حساب شما اضافه شد",
    "coin_management": "مدیریت سکه",
    "all_coin": "سکه برای همه",
    "one_coin": "سکه تکی",
    "ask_all_coin": "مقدار سکه را وارد کنید:",
    "coin_from_admin": "{coin} سکه از طرف ادمین به کاربران داده شد🎉",
    "adding_coin_to_users": "درحال افزودن/کم کردن سکه ها از حساب کاربران...",
    "coins_added": "سکه ها با موفقیت به حساب کاربران اضافه/کم شدند✅",
    "enter_user_id": "آیدی عددی کاربر را وارد کنید:",
    "enter_coin_amount": "مقدار سکه ای که میخواهید به حساب کاربر اضافه/کم شود را وارد کنید:",
    "loading_coin": "درحال افزودن/کم کردن سکه به حساب کاربر...",
    "coin_added": "سکه ها با موفقیت به حساب کاربر اضافه/کم شدند✅",
    "coin_added_notification": "تعداد {coin} امتیاز از طرف ادمین به شما داده شد",
    "coin_low_off": "تعداد {coin} امتیاز از سمت ادمین از حساب شما کم شد",
    "low_off": "کم کردن",
    "add_coin": "افزودن",
    "action_not_found": "حالت انتخابی شما معتبر نمیباشد❗",
    "down_force": "Downforce Configurations",
    "start_reaction": "Start Reaction",
    "grand_time": "مدیریت زمان مسابقات",
    "add_grand_time": "افزودن زمان",
    "show_grand_time": "مشاهده زمان ها",
    "ask_grand": "نام گرندپری را همان طوری که در ایرگست است وارد کنید:\nبرای مثال:\nBahrain Grand Prix\nSaudi Arabia Grand Prix",
    "ask_grand_event": "یکی از سشن های لیست زیر را وارد کنید:\nFP1\nFP2\nFP3\nSprint\nSprint_Shootout\nSprint_Qualifying\nQualifying\nRace",
    "ask_time": "زمان را مانند نمونه وارد کنید:\n16:30:00",
    "problem": "مشکلی پیش آمده!\nلطفا از طریق پشتیبانی به ادمین ربات اطلاع رسانی کنید ",
    "welcome_show_time": "زمان های ثبت شده:",
    "time_event": "رویداد:",
    "time": "زمان:",
    "time_not_found": "زمان حذف شده است!",
    "users_coin_gt": "امتیاز برتر",
    "users_sub_count": "زیر مجموعه برتر",
    "three_sub_count": "تبریک🎉\nتعداد زیر مجموعه های شما به 3 عدد رسید و 10 سکه رایگان دریافت کردید",
    "five_sub_count": "تبریک🎉\nتعداد زیر مجموعه های شما به 5 عدد رسید و 20 سکه رایگان دریافت کردید",
    "score_data": "سطح عضویت شما {level} هست و {coin} سکه از حساب شما برای دریافت دیتا کم شد!",
    "level_one": "برنزی",
    "level_two": "نقره ای",
    "level_three": "طلایی",
    "users_level": "تغییر سطح",
    "level_updated": "سطح کاربر با موفقیت تغییر کرد",
    "championship_calendar": "تقویم مسابقات",
    "coin_not_enough": """💫 - کاربر گرامی، امتیاز شما برای دریافت این دیتا کافی نمی باشد.

موجودی امتیاز شما {score} می باشد، برای دریافت امتیاز بیشتر می توانید با زیرمجموعه گیری و یا خرید سکه اقدام نمایید.""",
    "time_setup": "تنظیم زمان",
    "set_notifications": "اعلانات مسابقات",
    "join_channel_btn": "تنظیمات عضویت",
    "create_join_channel": "ایجاد جوین اجباری",
    "show_join_channel": "مشاهده چنل ها",
    "enter_channel_id": "آیدی یا لینک چنل را وارد کنید:",
    "channel_id": "آیدی چنل",
    "senior": "ارشد",
    "down_channel": "⬇️",
    "before_senior": "چنل از قبل ارشد میباشد!",
    "channel_up": "چنل با موفقیت به درجه ارشد ارتقا پیدا کرد!",
    "before_down": "چنل از قبل در حالت معمولی است!",
    "channel_down": "چنل با موفقیت به حالت عادی تغییر کرد!",
    "idealization_full": "کاربر عزیز، شما 2 فرصت ایده دادن خود را استفاده کرده اید و تا وقتی که ادمین این تعداد را ریست نکند شما نمیتوانید ایده ای بدهید!",
    "reset_success": "فرصت های ایده آل سازی با موفقیت بازنشانی شدند!",
    "yes": "بله",
    "no": "خیر",
    "ask_date": "تاریخ را وارد کنید:",
    "london_time": "زمان لندن",
    "iran_time": "زمان ایران",
    "select_time": "زمان را از دکمه های زیر انتخاب کنید:",
    "iran_time_set": "زمان ایران تنظیم شد!",
    "london_time_set": "زمان لندن تنظیم شد!",
    "select_notification": "آیا این زمان برای اعلانات تنظیم شود؟",
    "all": "Charts Data",
    "g_force": "G Force",
    "strategy": "Strategy",
    "driver": "Driver",
    "all_info": "All Info",
    "loading_one": "در حال دریافت اطلاعات ...\nسال: {year}\nگرندپری: {gp}\nرویداد: {event}\nراننده: {driver_one}",
    "loading_two": "در حال دریافت اطلاعات ...\nسال: {year}\nگرندپری: {gp}\nرویداد: {event}\nراننده اول: {driver_one}\nراننده دوم: {driver_two}",
    "down_all_coin": "کم کردن سکه(همه)",
    "enter_down_all_coin": "مقدار سکه ای که میخواهید از حساب کاربران کم شود را وارد کنید:",
    "all_down_su": "از تمام کاربران سکه کم شد✅",
    "statistics_data": "تعداد درخواست دیتا",
    "statistics_small": "تعداد درخواست کاربران",
    "statistics_all": "تعداد درخواست کل",
    "statistics": "آمار",
    "overtake_statistics": "Overtake Statistics",
    "map_viz_statistics": "Map Viz Statistics",
    "rpm_statistics": "Rpm Statistics",
    "downforce_statistics": "Down Force Statistics",
    "top_trap_statistics": "Top Speed Statistics",
    "start_reaction_statistics": "Start Reaction Statistics",
    "g_force_all_info": "All Info Statistics",
    "g_force_driver": "G force driver Statistics",
    "plot_lap_times": "Plot Lap Times Statistics",
    "map_break_statistics": "Map Break Statistics",
    "all_statistics": "All Statistics",
    "strategy_statistics": "Strategy Statistics",
    "enter_statistics": "دیتای مورد نظر خود را جهت مشاهده آمار انتخاب کنید:",
    "statistics_all_text": "تعداد کل درخواست ها در بخش {data} برابر است با {count} درخواست",
    "statistics_small_text": "تعداد کاربرانی که در بخش {data} درخواست زده اند مساوی با {count} است",
    "statistics_data_text": "تعداد کل درخواست دیتا ها مساوی با {count} است",
    "all_send": "ارسال همگانی",
    "all_send_text": "درصورت نیاز به تصویر، تصویر خود را ارسال کنید و در غیر این صورت متن مورد نظر خود را ارسال کنید:",
    "all_send_tx": ":متن را وارد کنید",
    "one_send": "ارسال پیام تکی",
    "data_to_pole": "Delta to Pole",
    "fia": "FIA Documents",
    "fia_tec": "قوانین فنی فیا",
    "fia_race_data": "دیتا مسابقه",
    "fia_info_management": "مدیریت اطلاعات فیا",
    "loading_fia": "در حال دریافت اطلاعات از فیا...",
    "cant_get_fia": "خطا در دریافت اطلاعات از فیا!\nلطفا به پشتیبانی ربات اطلاع دهید",
    "enter_pdf_files": "تمام فایل های مورد نظر برای نمایش در قوانین فنی فیا ارسال کنید:",
    "send_media": "لطفا رسانه ارسال کنید!",
    "enable_notifications": "فعال کردن اعلانات",
    "disable_notifications": "غیرفعال کردن اعلانات",
    "notifications_disabled": "اعلانات با موفقیت غیر فعال شد✅",
    "notifications_enabled": "اعلانات با موفقیت فعال شد✅",
    "lap_times_table": "Lap Times Table",
    "version": "1.4",
    "brake_configurations": "Brake Configurations",
    "composite_perfomance": "Composite Perfomance",
    "off_data": "تغییر وضعیت دیتا",
    "select_off_data": "دیتای مورد نظر را برای خاموش/روشن کردن انتخاب کنید:",
    "data_status": "نام دیتا: {name}\nوضعیت دیتا:‌ {status}",
    "on": "روشن کردن",
    "off": "خاموش کردن",
    "on_data_success": "دیتا با موفقیت روشن شد!",
    "off_data_success": "دیتا با موفقیت خاموش شد!",
    "data_is_off": "دیتای مورد نظر شما در حال حاضر خاموش میباشد!",
    "off_all": "خاموش کردن همه",
    "sure_off_all": "آیا از خاموش کردن کل دیتا ها مطمئن هستید؟",
    "sure_on_all": "آیا از روشن کردن کل دیتا ها مطمئن هستید؟",
    "on_all": "روشن کردن همه",
    "personal_report": "تعداد درخواست های شما در دیتای {data} مساوی با {count} عدد بوده است",
    "next_grand_prix": "گرندپری بعدی",
    "calender_by_year": "تقویم سال",
    "time_until": "زمان باقی مانده گرندپری آینده",
    "session_ended": "فصل به پایان رسیده است!",
    "sports_meeting": "دورهمی ورزشی",
    "page_one": "صفحه اول",
    "page_two": "صفحه دوم",
    "page_three": "صفحه سوم",
    "delete_account": "حذف اکانت",
    "upgrade_level": "ارتقا سطح عضویت",
    "forecast": "پیش بینی",
    "in_person_meeting": "دورهمی حضوری",
    "degradation_tyre": "Degradation Tyre",
    "weather_data": "Weather Data",
    "tyre_performance": "Tyre Performance",
    "forth_page": "صفحه چهارم",
    "ers_analysis": "ERS Analysis",
    "comparison_fastest_lap": "Comparison Fastest Lap",
    "efficiency_breakdown": "Efficiency Breakdown",
    "stress_index": "Stress Index",
    "now_plan": "سطح عضویت فعلی",
    "up_plan": "ارتقا سطح",
    "now_plan_text": """\nکاربر عزیز، سطح حساب شما {level} است\nسطح بعدی: {next_level}\nهزینه دیتا ها در سطح کاربری شما به شرح زیر میباشید:
    """,
    "level_two_up": "تبریک!\nتعداد زیر مجموعه شما به ۱۰ عدد رسید، سطح عضویت شما از برنزی به نقره ای ارتقا یافت!",
    "level_three_up": "تبریک!\nتعداد زیر مجموعه شما به ۲۰ عدد رسید، سطح عضویت شما از نقره ای به طلایی ارتقا یافت!",
    "sure_delete": "آیا از حذف اکانت خود اطمینان دارید؟\nتمام اطلاعات اکانت شما از جمله تعداد سکه، زیر مجموعه ها، سطح کاربری و... حذف خواهد شد!",
    "account_deleted": "اکانت شما با موفقیت حذف شد! جهت ایجاد مجدد اکانت \start را ارسال کنید",
    "delete_list": "لیست حذف اکانت",
    "delete_history": "تاریخچه حذف اکانت",
    "updating": "این قسمت در حال آپدیت می باشد. بزودی اطلاع رسانی خواهد شد.",
    "save_reply": "تنظیم بازپخش",
    "select_type": "آیا میخواهید فقط برای این رویداد لینک ثبت کنید یا برای رانندگان این رویداد؟",
    "event_drivers": "ثبت رانندگان",
    "event_select": "ثبت رویداد",
    "enter_link": "لینک ویدیو را وارد کنید:",
    "select_quality": "کیفیت را انتخاب کنید:",
    "summary": "خلاصه",
    "give_link": "ثبت لینک",
    "fastest_lap": "سریع ترین دور",
    "delete_video_warn": "توجه!❌\nاین ویدیو ۲۰ ثانیه دیگر حذف میشود، آن را جایی ذخیره کنید",
    "reply_count": "تعداد ویدیو های دریافت شده شما در بخش بازپخش: <blockquote>{count}</blockquote>"
}

EN_TEXT = {
    "EN_SELECTED": "English 🏴󠁧󠁢󠁥󠁮󠁧󠁿 󠁧󠁢󠁥󠁮language was selected",
    "FA_SELECTED": "Persian 🇮🇷 language was selected",
    "Membership_Confirmation": "confirmation✅",
    "pls_join": "To use the robot, first subscribe to the following channel, then start again",
    "big_heart": "Big heart",
    "rules": "Settings",
    "rules_show": "Rules",
    "technical_rules": "Technical rules",
    "copy_right": "Copy right",
    "protection": "Protection",
    "language": "Bot language",
    "rules_text": """💫 - Dear user, welcome to the robot rules section.

❗️ Technical rules:

- Please refrain from sending a large number of requests automatically in order to avoid technical problems, previous spam and lack of adequate response speed.

- Information and data are automatically connected to the robot through data centers and API, so its correctness must be confirmed by the users themselves. The robot will not be responsible for these cases.

- Do not post illegal, offensive or inappropriate content, in case of suspicious activities you will be blocked by the bot.

- Avoid publishing your personal information and that of others in communication spaces, this information will be kept in the robot. If you are seen publishing personal information in a place other than the robot, you will be blocked.

- Do not publish content without mentioning the source. If these things are seen, you will be blocked by the bot.

- If you have any problems or need help, contact the robot support.

- If you see any violation of the rules, report to the managers so that the necessary action can be taken.

🆔 @F1DATAIQBOT""",
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
    "archive": "Data home",
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
    "top_speed": "Top speed / Speed Trap",
    "word_text": "Button text",
    "word_tag": "Button tag",
    "come_next": "Paging button",
    "enter_new_text": "Enter new text:",
    "edited": "Changed successfully",
    "deleted": "Removed successfully",
    "underline": "To search in bot buttons, put _ or hyphen in your first phrase",
    "reply": "Replay of matches",
    "fantasy": "Fantasy league",
    "data_archive": "Data home",
    "soon": "Soon",
    "user_information": "User information",
    "personal_account": "Personal account",
    "sub_collection": "Sub collection",
    "first_start": "Start first",
    "grand": "Power Ranking Management",
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
    "robot_statistics": "Users Statistics",
    "statistics_text": "Number of bot users: {users}",
    "try_again": "Your number is not correct! Try again",
    "sub_link": "You will receive 10 free coins by entering each user through the sub-category link.\n- Your subcategory link:\n{link}",
    "timeout_error": "Response time is over!\nPlease try again",
    "select_gp": "Please select grand prix:",
    "select_session": "Please select event:",
    "loading": "Loading data...\nyear:{year}\ngp:{gp}\nevent:{event}",
    "loading_one": "Receiving information...\nYear: {year}\nGrand Prix: {gp}\nevent: {event}\nDriver: {driver_one}",
    "loading_two": "Receiving information...\nYear: {year}\nGrand Prix: {gp}\nevent: {event}\nDriver One: {driver_one}\nDriver two: {driver_two}",
    "pls_join_plus": "Please subscribe to the channel below to use the power ranking button and then click power ranking again.",
    "account_setup": "Account setup",
    "bot_ping": "Bot ping",
    "coming_soon": "This section will be activated soon",
    "getting_ping": "Receiving ping...",
    "overtake": "Overtake",
    "map_viz": "Map Speed Viz",
    "ask_driver": "please select driver:",
    "ask_state": "Select the desired question mode:\nMode 1: Single question\nMode 2: Multiple questions",
    "ask_performance": "Give the driver's performance from 1 to 10 points:",
    "new_users": "New users",
    "users_excel": "Excel Users",
    "users_excel_caption": "Excel file of robot users",
    "dont_time": "The race has not started yet!",
    "idealization": "Idealization",
    "connect_admin": "Communication with support",
    "question_image": "If you need an image, send the image (if you don't need an image, send the text of your ticket)\n To cancel the ticket registration operation, send **Cancel**❗",
    "question_text": "Enter your text:",
    "ticket_successfully": "Ticket successfully registered \n will answer the ticket as soon as possible",
    "ticket_answer": "📮register answer📮",
    "admin_notification": "A new ticket has been registered❗\nTicket text: {text}\nTicket number: {num}\nUser numeric ID: `{id}`\nUser Full Name:{name}\nUserName: {username}",
    "ticket_dl_error": "❗ This ticket has been removed.",
    "close_error": "❗ This ticket is closed.",
    "question_image_answer": "If you need an image, send the image (if you don't need an image, send your answer text)\n To cancel the registration operation, send **cancel**❗",
    "ticket_answer_ad": "📮 Answer for Admin📮",
    "answer_successfully": "Answer successfully registered \n Reply to Ticket Number: {Num}",
    "user_notification":
        "A response from the admin has been sent to your ticket!\nYour ticket text:{user_text}\n\n**Admin's response**:{admin_text}",
    "answer_successfully_user": "Submitted the answer successfully to the admin✅",
    "admin_notification_answer": "A new response was recorded by users"
                                 "\n Text Reply: {Text} \n on ATICATION NUMBER: {Num} \n User Numerical ID: `{ID}`\nUser Full Name: {name}\nUsername:{username}",
    "question_image_idea": "If you need an image, send the image\n otherwise, send the text of your idea",
    "question_text_idea": "Send the text of your idea:",
    "management": "Management",
    "users": "Users Management",
    "tickets": "View tickets",
    "welcome_show_tickets": "Registered tickets:👇",
    "ticket_text": "📝Ticket text:",
    "ticket_count": "🔄Ticket Number:",
    "ticket_user_id": "User Numerical ID:",
    "close_ticket": "🔐Close Ticket🔐",
    "ticket_not_found": "Ticket has been removed❗",
    "ticket_opened": "The ticket opened✅",
    "ticket_closed": "The ticket closed✅",
    "rpm": "RPM Chart",
    "ask_driver_one": "Choose the first driver:",
    "ask_driver_two": "Choose the second driver:",
    "map_break": "Map Brake Viz",
    "lap_times": "Plot Lap Times",
    "start_score": f"The number of {START_SCORE} coin was added to your account!",
    "daily_coin": f"{DAILY_COIN} coins are added to your account daily!",
    "coin_management": "Coin management",
    "all_coin": "Coin for all",
    "one_coin": "Single coin",
    "ask_all_coin": "Enter the amount of coin you want to add to all users:",
    "coin_from_admin": "{coin} coins were given to users from admin",
    "adding_coin_to_users": "Adding coins to users account ...",
    "coins_added": "The coins were successfully added to the users account✅",
    "enter_user_id": "Enter the Numerical ID of the user:",
    "enter_coin_amount": "Enter the amount of coin you want to add/low-off to the user's account:",
    "loading_coin": "Adding coins to the user's account ...",
    "coin_added": "The coins were successfully added/low-off to the user's account✅",
    "coin_added_notification": "{coin} Score was given to you by administration",
    "low_off": "Low-off",
    "add_coin": "Add",
    "action_not_found": "Your selected mode is not valid❗",
    "down_force": "Downforce Configurations",
    "start_reaction": "Start Reaction",
    "grand_time": "Event Time Management",
    "add_grand_time": "Add time",
    "show_grand_time": "View times",
    "ask_grand": "Enter the name of the Grand Prix as it is in the ergast: \n for example: \n Bahrain Grand Prix \n Saudi Arabia Grand Prix",
    "ask_grand_event": "Enter one of the following listings: \n FP1 \n FP2 \n FP3 \n Sprint \n Sprint_Shootout \n Sprint_Qualifying \n Qualifying \n Race",
    "ask_time": "Enter the time like the sample: \n 16:30:00",
    "problem": "There is a problem! \n Please notify the robot administrator via support",
    "welcome_show_time": "Registered times:",
    "time_event": "Event:",
    "time": "Time:",
    "time_not_found": "Time has been removed!",
    "users_coin_gt": "Top score",
    "users_sub_count": "Top subset",
    "three_sub_count": "Congratulations🎉 \n you got the number of subsets to 3 and 10 free coins received!",
    "five_sub_count": "Congratulations🎉 \n you got your subsets to 5 and 20 free coins received!",
    "score_data": "Your membership level is {level} and {coin} coins were deducted from your account to receive data!",
    "level_one": "Bronze",
    "level_two": "Silver",
    "level_three": "Golden",
    "users_level": "Changing Level",
    "level_updated": "The user level successfully changed",
    "championship_calendar": "Championship Calendar",
    "coin_not_enough": """💫 - Dear user, your score is not enough to receive this data.

Your points balance is {score}, to get more points, you can subcategory or buy coins.""",
    "time_setup": "Time setup",
    "set_notifications": "Set notifications",
    "join_channel_btn": "Join Settings",
    "create_join_channel": "create join channel",
    "show_join_channel": "show join channels",
    "enter_channel_id": "Enter channel id or link:",
    "channel_id": "Channel id",
    "senior": "Senior",
    "senior_channel": "⬆️",
    "down_channel": "⬇️",
    "before_senior": "Channel has already been a senior!",
    "channel_up": "Channel has successfully been promoted to Senior!",
    "before_down": "The channel is already in normal mode!",
    "channel_down": "The channel has successfully changed to normal!",
    "idealization_full": "Dear user, you have used 2 opportunities to give your idea and you cannot give an idea until the admin resets this number!",
    "reset_success": "The idealization opportunities have been reset successfully!",
    "yes": "Yes",
    "no": "No",
    "ask_date": "Enter the date in the format: YYYY-MM-DD:",
    "london_time": "London Time",
    "iran_time": "Iran Time",
    "select_time": "Select a time from the buttons below",
    "iran_time_set": "Iran time is set!",
    "london_time_set": "London time is set!",
    "select_notification": "Set this time for notifications?",
    "all": "Charts Data",
    "g_force": "G Force",
    "strategy": "Strategy",
    "driver": "Driver",
    "all_info": "All Info",
    "down_all_coin": "Subtract coins (all)",
    "enter_down_all_coin": "Enter the amount of coins you want to deduct from the user's account:",
    "all_down_su": "Coins were deducted from all users✅",
    "statistics_data": "Number of data requests",
    "statistics_small": "Number of user requests",
    "statistics_all": "Total number of requests",
    "statistics": "Statistics",
    "overtake_statistics": "Overtake Statistics",
    "map_viz_statistics": "Map Viz Statistics",
    "rpm_statistics": "Rpm Statistics",
    "downforce_statistics": "Down Force Statistics",
    "top_trap_statistics": "Top Speed Statistics",
    "start_reaction_statistics": "Start Reaction Statistics",
    "g_force_all_info": "All Info Statistics",
    "g_force_driver": "G force driver Statistics",
    "plot_lap_times": "Plot Lap Times Statistics",
    "map_break_statistics": "Map Break Statistics",
    "all_statistics": "All Statistics",
    "strategy_statistics": "Strategy Statistics",
    "enter_statistics": "Select the desired data to view statistics",
    "statistics_all_text": "The total number of requests in the {data} section is equal to {count} requests",
    "statistics_small_text": "The number of users who have applied in {data} is {count}",
    "statistics_data_text": "The total number of data requests is equal to {count}",
    "all_send": "Public Posting",
    "all_send_text": "If you need an image, send your image and otherwise send your desired text:",
    "all_send_tx": "Enter the text:",
    "one_send": "Single Shipment",
    "data_management": "Data Management",
    "data_to_pole": "Delta to Pole",
    "fia": "FIA Documents",
    "fia_tec": "Technical rules",
    "fia_race_data": "Race Data",
    "fia_info_management": "Fia Info Management",
    "loading_fia": "Getting data from fia ...",
    "cant_get_fia": "Error in get data from fia, please connect to bot support!",
    "enter_pdf_files": "Send all the desired files to be displayed in the FIA ​​technical rules:",
    "send_media": "please send media!",
    "enable_notifications": "Enable notifications",
    "disable_notifications": "Disable notifications",
    "lap_times_table": "Lap Times Table",
    "version": "1.4",
    "notifications_enabled": "Notifications have been activated successfully✅",
    "notifications_disabled": "Notifications have been successfully disabled✅",
    "brake_configurations": "Brake Configurations",
    "composite_perfomance": "Composite Perfomance",
    "off_data": "Change data status",
    "select_off_data": "Select data to on/off it status:",
    "data_status": "Data name: {name}\nData status: {status}",
    "on": "On data",
    "off": "Off data",
    "on_data_success": "Data turned on!",
    "off_data_success": "Data turned off!",
    "data_is_off": "Your desired data is currently off!",
    "off_all": "Turn off all",
    "sure_off_all": "Are you sure to turn off all data?",
    "sure_on_all": "Are you sure to turn on all data?",
    "on_all": "Turn on all",
    "personal_report": "The number of your requests in {data} is equal to {count} number",
    "next_grand_prix": "Next Grand prix",
    "calender_by_year": "Calender by year",
    "time_until": "Time until next Grand prix",
    "session_ended": "The season is over!",
    "sports_meeting": "Sports meeting",
    "page_one": "Page one",
    "page_two": "Page two",
    "page_three": "Page three",
    "delete_account": "Delete account",
    "upgrade_level": "Upgrade level",
    "forecast": "Forecast",
    "in_person_meeting": "In person meeting",
    "degradation_tyre": "Degradation Tyre",
    "weather_data": "Weather Data",
    "tyre_performance": "Tyre Performance",
    "forth_page": "Forth Page",
    "ers_analysis": "ERS Analysis",
    "comparison_fastest_lap": "Comparison Fastest Lap",
    "efficiency_breakdown": "Efficiency Breakdown",
    "stress_index": "Stress Index",
    "now_plan": "Current membership level",
    "up_plan": "Level Up",
    "now_plan_text": """Dear user, your account level is {level}\nNext level: {next_level}\nData charges at your user level are as follows:""",
    "level_two_up": "Congratulations!\nYour number of sub-groups has reached 10, your membership level has been upgraded from bronze to silver!",
    "level_three_up": "Congratulations!\nYour number of followers has reached 20, your membership level has been upgraded from Silver to Gold!",
    "sure_delete": "Are you sure you want to delete your account?\nAll your account information, including the number of coins, subcategories, user level, etc., will be deleted!",
    "account_deleted": "Your account has been successfully deleted! Submit \start to re-create your account.",
    "delete_list": "Account Delete List",
    "delete_history": "Delete Account History",
    "updating": "This section is being updated. Information will be provided soon.",
    "save_reply": "Config Reply",
    "select_type": "Do you want to register a link for the event only or for event drivers?",
    "event_drivers": "Event Drivers",
    "event_select": "Save Event",
    "enter_link": "Enter video link:",
    "select_quality": "Select the quality:",
    "summary": "Summary",
    "give_link": "Register Link",
    "fastest_lap": "Fastest Lap",
    "delete_video_warn": "Attention!❌\nThis video will be deleted in 20 seconds, save it somewhere",
    "reply_count": "Number of videos you have downloaded in the replay section: <blockquote>{count}</blockquote>"
}
