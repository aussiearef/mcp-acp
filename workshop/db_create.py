# server.py
import sqlite3

conn = sqlite3.connect("mcp-a2a.db")
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS numbers (number TEXT PRIMARY KEY, status TEXT NOT NULL)")
cur.execute("INSERT INTO numbers (number, status) VALUES ('0412345678', 'active')")
cur.execute("INSERT INTO numbers (number, status) VALUES ('0498765432', 'inactive')")
conn.commit()
conn.close()
