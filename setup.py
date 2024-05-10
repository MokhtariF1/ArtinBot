import sqlite3
con = sqlite3.connect("bot.db")
cur = con.cursor()
# cur.execute("DROP TABLE pay")
cur.execute("DROP TABLE users")
cur.execute("CREATE TABLE users(id,lang,lastd,join_time,sub_count,score,fantasy,protection,validity)")
# cur.execute("CREATE TABLE pay(user_id,pay_id,order_id,type)")
# cur.execute("CREATE TABLE btn(tag,text)")
