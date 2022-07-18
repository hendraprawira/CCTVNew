import sqlite3
conn = sqlite3.connect('database.db')
cur = conn.cursor()
cur.execute("SELECT * FROM cctv")
data = cur.fetchall()
# cur.execute("DELETE from cctv WHERE id LIKE '10'")
# conn.commit()
print(data)