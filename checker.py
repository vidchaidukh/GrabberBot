from datetime import datetime
import sqlite3
import time
import olx, izi

board_grabbbers = {'olx' : olx.catch, 'izi' : izi.catch}

def check():
    conn = sqlite3.connect('db/database.db', check_same_thread=False)
    while True:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM requests")
        requests = cursor.fetchall()
        cursor.close()
        for req in requests:
            cursor = conn.cursor()
            print(req)
            time_now = datetime.now()
            _ = board_grabbbers[req[3]](req[2], req[0], req[5])
            cursor.execute("UPDATE requests SET last_advert =? WHERE id = ?",
                           (time_now.strftime("%Y,%m,%d,%H,%M"), req[0]))
            cursor.close()
            conn.commit()
        time.sleep(80)





