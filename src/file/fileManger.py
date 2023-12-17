import os
import random
import time

from config.getConfig import getConfig
from file.formatCorver import x2png
from sql.sqliteCon import addData

savePath = getConfig("IMAGERUN_FILE_SAVEPATH")
urlPrefix = getConfig("IMAGERUN_FILE_URLPREFIX")

if not savePath.endswith("/"):
    savePath += "/"
savePath += "/images/"

supportImageFormat = ["jpg", "jpeg", "png", "bmp", "webp"]


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
    # 取文件格式
    name = name.replace(".jpeg", ".jpg")
    imageFormat = name.split(".")[-1]
    # 判断是否符合格式
    if imageFormat not in supportImageFormat:
        return -1
    # 转换格式为png
    if imageFormat == "png":
        pass
    else:
        data = x2png(data)
        if data is None:
            return -1
    # 重命名文件
    # uploadName + timestamp + random + user = uuid = filename
    timeStamp = str(time.time())[0:10]
    name = name \
               .replace(".png", "") \
               .replace(".jpeg", "") \
               .replace(".jpg", "") \
               .replace(".bmp", "") \
               .replace(".webp", "") + \
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
    addData(name, name.replace(".png", ""), int(timeStamp), "root")
    return urlPrefix + "images/" + name
