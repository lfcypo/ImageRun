import os
import sqlite3

from config.getConfig import getConfig

savePath = getConfig("IMAGERUN_FILE_SAVEPATH")
if not savePath.endswith("/"):
    savePath += "/"
savePath += "/db"
if not os.path.exists(savePath):
    os.makedirs(savePath)
savePathName = savePath + "/ImageRun.db"
conn = sqlite3.connect(savePathName)


def addData(name: str, imageHash: str, time: int, user: str):
    c = conn.cursor()
    try:
        c.execute('insert into info(name, hash, time, user) values(?,?,?,?)', (name, imageHash, time, user))
        conn.commit()
    except sqlite3.OperationalError:
        try:
            makeTable = """
            CREATE TABLE info ( name VARCHAR(255), hash VARCHAR(255), time BIGINT, user VARCHAR(255));
            """
            c.execute(makeTable)
            conn.commit()
            c.execute('insert into info(name, hash, time, user) values(?,?,?,?)', (name, imageHash, time, user))
            conn.commit()
        except sqlite3.OperationalError:
            return
