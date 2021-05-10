import sqlite3

con = sqlite3.connect('file:/mnt/nasne/sample.db', uri=True)
cur = con.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS sample(id INTEGER PRIMARY KEY AUTOINCREMENT, name STRING)')
cur.execute('INSERT INTO sample(name) values("foo")')
con.commit()
con.close()

con = sqlite3.connect('file:/mnt/nasne/sample.db', uri=True)
cur = con.cursor()
cur.execute('SELECT * FROM sample')
print(cur.fetchall())
con.close()

