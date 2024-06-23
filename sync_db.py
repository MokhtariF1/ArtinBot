import sqlite3
from datetime import timedelta, datetime
import config
con = sqlite3.connect("bot.db")
cur = con.cursor()
users = cur.execute("SELECT * FROM users").fetchall()
for user in users:
    currentDateAndTime = datetime.now()
    score_time = currentDateAndTime + timedelta(days=1)
    currentTime = score_time.strftime("%Y-%m-%d %H:%M:%S")
    user_score = user[5]
    user_score += config.START_SCORE if user_score == 0 else user_score
    user_score += config.DAILY_COIN
    cur.execute(f"UPDATE users SET score_date = '{currentTime}',score = {user_score},level = {1} WHERE id = {user[0]};")
    con.commit()