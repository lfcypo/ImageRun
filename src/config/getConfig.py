import os


def selectEnvValue(key: str):
    """
    取系统环境变量
    :param key: 变量名
    :return: 变量值
    """
    return str(os.environ.get(key))


def getConfig(key: str):
    """
    获取配置项
    :param key: 配置项
    :return: 配置项的值
    """
    return selectEnvValue(key)


def getBanner():
    """
    获取banner
    :return: banner
    """
    return """
  _____                       _____                  
 |_   _|                     |  __ \                 
   | |    _ __ ___     __ _  | |__) |  _   _   _ __  
   | |   | '_ ` _ \   / _` | |  _  /  | | | | | '_ \ 
  _| |_  | | | | | | | (_| | | | \ \  | |_| | | | | |
 |_____| |_| |_| |_|  \__, | |_|  \_\  \__,_| |_| |_|
                       __/ |                         
                      |___/    """
