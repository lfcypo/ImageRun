import os
import random
import time

from config.getConfig import getConfig
from file.formatCorver import x2png
from sql.sql import addData

savePath = getConfig("IMAGERUN_FILE_SAVEPATH")
urlPrefix = getConfig("IMAGERUN_FILE_URLPREFIX")

if not savePath.endswith("/"):
    savePath += "/"
savePath += "/images/"


def saveFile(name: str, data: bytes):
    """
    文件管理器
    :param name: 文件名
    :param data: 数据
    :return:
    """
    # 判断savePath是否存在
    if not os.path.exists(savePath):
        os.makedirs(savePath)
    # 转格式
    data = x2png(data)
    # 重命名文件
    # uploadName + timestamp + random + user = uuid = filename
    timeStamp = str(time.time())[0:10]
    name = name + \
           timeStamp + \
           str(random.randint(100000, 999999)) + \
           "root" + \
           ".png"
    # noinspection PyBroadException
    try:
        with open(savePath + name, "wb") as imageFileObject:
            imageFileObject.write(data)
    except Exception:
        return -2
    # SQL
    addData(name, data, timeStamp, "root")
    return urlPrefix + "images/" + name
