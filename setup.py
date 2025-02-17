import sqlite3
con = sqlite3.connect("bot.db")
cur = con.cursor()
import config
bot_text = config.TEXT
# cur.execute("DROP TABLE idealization")
# cur.execute("DROP TABLE users")
# cur.execute("DROP TABLE invite")
# cur.execute("DROP TABLE grand_time")
# cur.execute("DROP TABLE drivers")
# cur.execute("DROP TABLE driver_score")
# cur.execute("DROP TABLE data_status")
# cur.execute("DROP TABLE statistics_all")
cur.execute("CREATE TABLE IF NOT EXISTS users(id,lang,lastd,join_time,sub_count,score,fantasy,protection,validity,score_date,level,time_zone)")
cur.execute("CREATE TABLE IF NOT EXISTS deleted_accounts(id,lang,lastd,join_time,sub_count,score,fantasy,protection,validity,score_date,level,time_zone,delete_time)")
cur.execute("CREATE TABLE IF NOT EXISTS pay(user_id,pay_id,order_id,type)")
cur.execute("CREATE TABLE IF NOT EXISTS btn(tag,text)")
cur.execute("CREATE TABLE IF NOT EXISTS drivers(for_grand,name,driver_id,avg,avg_plus,avg_count)")
cur.execute("CREATE TABLE IF NOT EXISTS grand(num, name, close, state)")
cur.execute("CREATE TABLE IF NOT EXISTS driver_score(user_id,driver_id,for_grand)")
cur.execute("CREATE TABLE IF NOT EXISTS invite(user_id,invite_id)")
cur.execute("CREATE TABLE IF NOT EXISTS admins(_id)")
cur.execute("CREATE TABLE IF NOT EXISTS tickets(media,text,count,user_id,status)")
cur.execute("CREATE TABLE IF NOT EXISTS grand_time(grand, session_type, time, time_num, notifications, grand_date)")
cur.execute("CREATE TABLE IF NOT EXISTS join_channel(channel_id, senior, channel_num)")
cur.execute("CREATE TABLE IF NOT EXISTS idealization(user_id)")
cur.execute("CREATE TABLE IF NOT EXISTS statistics_all(data, user_id)")
cur.execute("CREATE TABLE IF NOT EXISTS statistics_small(data, user_id)")
cur.execute("CREATE TABLE IF NOT EXISTS data_status(data, status)")
# l = [bot_text["rpm"],bot_text["overtake"],bot_text["map_viz"],bot_text["down_force"],bot_text["top_speed"],
#      bot_text["start_reaction"],bot_text["all_info"],bot_text["driver"],bot_text["lap_times"],bot_text["map_break"],
#      bot_text["all"],bot_text["strategy"],bot_text["data_to_pole"],bot_text["lap_times_table"],
#      bot_text["brake_configurations"],bot_text["composite_perfomance"], bot_text["degradation_tyre"],
#      bot_text["weather_data"], bot_text["tyre_performance"], bot_text["ers_analysis"],
#      bot_text["comparison_fastest_lap"], bot_text["efficiency_breakdown"], bot_text["stress_index"]]
# l = [bot_text["degradation_tyre"]]
# for data in l:
#     cur.execute(f"INSERT INTO data_status VALUES ('{data}', 'on')")
#     con.commit()
# cur.execute("ALTER TABLE statistics_all ADD COLUMN user_id TEXT;")
# cur.execute("ALTER TABLE users ADD COLUMN notifications TEXT;")
# cur.execute(f"INSERT INTO admins VALUES (5415792594)")

# cur.execute(f"INSERT INTO join_channel VALUES ('https://t.me/RacePlusIran', {True}, {2020})")
# con.commit()
# con.commit()
# print(cur.execute("SELECT * FROM grand").fetchall())
