import sqlite3
con = sqlite3.connect("bot.db")
cur = con.cursor()
cur.execute("DROP TABLE pay")
cur.execute("DROP TABLE users")
cur.execute("CREATE TABLE users(id,lang,lastd)")
cur.execute("CREATE TABLE pay(user_id,pay_id,order_id,type)")
