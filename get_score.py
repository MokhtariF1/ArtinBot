import sqlite3
from datetime import datetime, timedelta
# اتصال به دیتابیس
conn = sqlite3.connect('bot.db')
cursor = conn.cursor()
# گرفتن زمان حال
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# پیدا کردن کاربرانی که score_date آن ها کوچک تر یا مساوی زمان حال است
cursor.execute("SELECT id, score, score_date FROM users WHERE score_date <= ?", (now,))
users = cursor.fetchall()

# حلقه زدن در کاربران و به روز رسانی امتیاز و score_date
for user in users:
    user_id, score, score_date = user
    new_score = score + 1
    new_score_date = datetime.strptime(score_date, '%Y-%m-%d %H:%M:%S') + timedelta(days=1)
    
    # به روز رسانی امتیاز و score_date در دیتابیس
    cursor.execute("UPDATE users SET score = ?, score_date = ? WHERE id = ?", (new_score, new_score_date, user_id))
# ذخیره تغییرات و بستن اتصال
conn.commit()
conn.close()
