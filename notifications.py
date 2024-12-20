import datetime
import time
import pytz
import sqlite3
from config import *
import requests
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
}# Connect to the SQLite database
conn = sqlite3.connect('bot.db')
cursor = conn.cursor()
def main():
    get_notifications_time = cursor.execute('SELECT * FROM grand_time ORDER BY time ASC').fetchall()
    for notification in get_notifications_time:
        session_type = notification[1]
        grand_notification = notification[0]
        notification_status = notification[4]
        if session_type == "FP1" or session_type == "FP2" or session_type == "FP3" or notification_status == "no":
            continue
        else:
            notification_date = notification[5]
            notification_time = notification[2]
            # Specify the target date and time in Iran's timezone
            target_date_str = notification_date # Year-Month-Day
            target_time_str = notification_time     # HH:MM:SS

            # Combine date and time into a single datetime object
            target_datetime_str = f"{target_date_str} {target_time_str}"
            
            # Define the timezone for Iran
            iran_tz = pytz.timezone('Asia/Tehran')

            # Create a naive datetime object and localize it to Iran's timezone
            target_datetime_naive = datetime.datetime.strptime(target_datetime_str, "%Y-%m-%d %H:%M:%S")
            target_datetime = iran_tz.localize(target_datetime_naive)

            # Calculate the time to wait until ten minutes before the target time
            ten_minutes_before = target_datetime - datetime.timedelta(minutes=10)

            # Get the current time in Iran's timezone
            current_time = datetime.datetime.now(iran_tz)

            # Calculate the time to wait
            wait_time = (ten_minutes_before - current_time).total_seconds()

            if wait_time > 0:
                print(f"Waiting until {ten_minutes_before} (Iran time)...")
                time.sleep(wait_time)  # Wait until ten minutes before the target time
                users = cursor.execute('SELECT * FROM users').fetchall()
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
                for user in users:
                    user_id = user[0]
                    user_lang = user[1]
                    user_notifications = user[12]
                    if user_notifications == 'no':
                        continue
                    elif user_notifications is None:
                        continue
                    else:
                        pass
                    if user_lang == 1:
                        session = session_type
                        gp = grand_notification
                        full_text = "The {event} event in {gp} will start in ten minutes!".format(event=session, gp=gp)
                    else:
                        session = type_tr[session_type]
                        gp = country_tr[grand_notification.replace(" ", "_")]
                        full_text = "رویداد {event} ده دقیقه دیگر در {gp} شروع خواهد شد".format(event=session, gp=gp)
                    telegram_send_message_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={user_id}&text={full_text}"
                    response = requests.get(telegram_send_message_url)
            else:
                print("The specified time is already less than ten minutes away or has passed.")
                continue

if __name__ == "__main__":
    main()
