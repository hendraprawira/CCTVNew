import sqlite3

conn = sqlite3.connect('database.db')
print ("Opened database successfully");

conn.execute('CREATE TABLE cctv (id INTEGER PRIMARY KEY AUTOINCREMENT, cctv_link TEXT, address TEXT)')
print ("Table created successfully");
conn.close()