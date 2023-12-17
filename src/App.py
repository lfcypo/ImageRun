import base64
import random

from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from gevent.pywsgi import WSGIServer

from config.getConfig import getConfig
from file import fileManger

app = Flask(__name__ + str(random.randint(1, 114514)) + "ImageRun")
CORS(app)

savePath = getConfig("IMAGERUN_FILE_SAVEPATH")
if not savePath.endswith("/"):
    savePath += "/"
savePath += "/images/"


@app.route('/healthy')
def healthy():
    return jsonify({
        "code": 200,
        "msg": "我很好",
        "data": "谢谢关心～"
    })


@app.route('/api/upload', methods=['POST'])
def upload():
    """
    上传文件
    Method: POST
    data - Base64编码后二进制图像数据
    name - Base64编码后文件名
    :return:
    """
    requests = request.get_json()
    try:
        data = requests['data']
        name = requests['name']
    except KeyError as e:
        return jsonify({
            "code": 400,
            "msg": "参数错误-键错误",
            "data": str(e)
        })
    # Base64解码
    try:
        data = base64.b64decode(data)
        name = base64.b64decode(name).decode("utf-8").replace(" ", "")
    except Exception as e:
        return jsonify({
            "code": 402,
            "msg": "参数错误-解码错误",
            "data": str(e)
        })
    # 保存
    result = fileManger.saveFile(name, data)
    if result == -1 or result == -2:
        return jsonify({
            "code": 401,
            "msg": "保存失败",
            "data": str(result)
        })
    elif len(result) != 0:
        return jsonify({
            "code": 200,
            "msg": "保存成功",
            "data": str(result)
        })
    else:
        return jsonify({
            "code": 500,
            "msg": "未知错误",
            "data": str(result)
        })


@app.route("/images/<filename>")
def get_filename(filename):
    print(f"{savePath}/{filename}")
    with open(f"{savePath}/{filename}", 'rb') as f:
        fileas = f.read()
    res = make_response(fileas)
    res.headers['Content-Type'] = 'image/png'
    return res


if __name__ == '__main__':
    host = getConfig("IMAGERUN_HOST")
    port = int(getConfig("IMAGERUN_PORT"))
    http_server = WSGIServer((host, port), app)
    http_server.serve_forever()
