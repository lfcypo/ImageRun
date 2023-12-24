import os
import sqlite3
import hashlib
import io

from PIL import Image

from config.getConfig import getConfig

savePath = getConfig("IMAGERUN_FILE_SAVEPATH")
if not savePath.endswith("/"):
    savePath += "/"
savePath += "/db"
if not os.path.exists(savePath):
    os.makedirs(savePath)
savePathName = savePath + "/ImageRun.db"
conn = sqlite3.connect(savePathName)


def getSize(data: bytes):
    with Image.open(io.BytesIO(data)) as img:
        width, height = img.size
        return width, height


def addData(name: str, data: bytes, time: int, user: str):
    imageSHA1 = hashlib.sha1(data).hexdigest()
    imageMD5 = hashlib.md5(data).hexdigest()
    size = len(io.BytesIO(data).getbuffer())
    width, height = getSize(data)

    c = conn.cursor()
    try:
        c.execute('insert into images(name, size, md5, sha1, width, height, uploadTime, uploadUser) values(?,?,?,?,?,?,?,?)',
                  (name, size, imageMD5, imageSHA1, width, height, time, user))
        conn.commit()
    except sqlite3.OperationalError:
        try:
            makeTable = """
                CREATE TABLE IF NOT EXISTS images(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL DEFAULT "",
                size INTEGER NOT NULL DEFAULT 0,
                md5 TEXT NOT NULL DEFAULT "",
                sha1 TEXT NOT NULL DEFAULT "",
                width INTEGER NOT NULL DEFAULT 0,
                height INTEGER NOT NULL DEFAULT 0,
                uploadTime INTEGER NOT NULL DEFAULT 0,
                uploadUser TEXT NOT NULL DEFAULT ""
                );
            """
            c.execute(makeTable)
            conn.commit()
            c.execute('insert into images(name, size, md5, sha1, width, height, uploadTime, uploadUser) values(?,?,?,?,?,?,?,?)',
                      (name, size, imageMD5, imageSHA1, width, height, time, user))
            conn.commit()
        except sqlite3.OperationalError:
            return
