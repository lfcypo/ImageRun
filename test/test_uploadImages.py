import base64
import json

import requests

url = "http://127.0.0.1:8080/api/upload"

headers = {
    "Content-Type": "application/json"
}


def readData():
    imageData = b""
    with open("./截屏2023-12-17 15.02.25.png", "br") as f:
        for i in f.readlines():
            imageData = imageData + i
    imageData = base64.b64encode(imageData).decode("utf-8")
    return imageData




data = {
    "name": "截屏2023-12-17 15.02.25.png",
    "data": readData()
}
response = requests.post(url, data=json.dumps(data), headers=headers)
if response.status_code == 200:
    data = response.json()
    print(data)
