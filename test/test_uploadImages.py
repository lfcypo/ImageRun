import base64
import json

import requests

url = "http://8.134.134.195:8090/api/upload"

headers = {
    "Content-Type": "application/json"
}


def readData():
    imageData = b""
    with open("./ikun.jpeg", "br") as f:
        for i in f.readlines():
            imageData = imageData + i
    imageData = base64.b64encode(imageData).decode("utf-8")
    return imageData


data = {
    "name": base64.b64encode("ikun.jpeg".encode("utf-8")).decode("utf-8"),
    "data": readData()
}

response = requests.post(url, data=json.dumps(data), headers=headers)
if response.status_code == 200:
    data = response.json()
    print(data)
