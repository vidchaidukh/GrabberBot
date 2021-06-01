import sqlite3
import time
import olx, izi

board_grabbbers = {'olx' : olx.catch, 'izi' : izi.catch}

def check():
    conn = sqlite3.connect('db/database.db', check_same_thread=False)
    cursor = conn.cursor()
    while True:
        cursor.execute("SELECT * FROM requests")
        requests = cursor.fetchall()
        for req in requests:
            print(req)
            board_grabbbers[req[3]](req[2])
        time.sleep(5)



