import sqlite3
conn = sqlite3.connect('database.db')

sql = ''' INSERT INTO cctv(cctv_link,address)
              VALUES(?,?) '''
project = ('rtsp://admin:f4tahkoM@192.168.18.17/Streaming/Channels/302', 'Jakarta Timur');
cur = conn.cursor()
cur.execute(sql, project)
conn.commit()