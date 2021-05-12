import sqlite3

from grove_sensor.moisture_sensor import MoistureSensor

MOISTURE_SENSOR_INPUT = 0  # A0
MOISTURE_SENSOR_MAX_VOLT = 670


def read():
    moisture_sensor = MoistureSensor(MOISTURE_SENSOR_INPUT, MOISTURE_SENSOR_MAX_VOLT)
    return moisture_sensor.read()


def setupDB():
    con = sqlite3.connect("file:/mnt/nasne/water_system.db", uri=True)
    cur = con.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS moistures(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            value INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )
    return con, cur


def saveToDB(con, cur, val):
    print(val)
    cur.execute("INSERT INTO moistures(value) values(?)", (val,))
    con.commit()


val = read()
con, cur = setupDB()
saveToDB(con, cur, val)
con.close()
