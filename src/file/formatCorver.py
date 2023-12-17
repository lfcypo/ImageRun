from io import BytesIO

from PIL import Image


def x2png(data):
    """
    将输入的图像数据转换为PNG格式字节流。

    :param data: 用于转换的图像原始字节流
    :return: 转换后的PNG格式字节流，若转换失败则返回None
    """
    # noinspection PyBroadException
    try:
        image = Image.open(BytesIO(data))
        png_bytes = BytesIO()
        image.save(png_bytes, format='PNG')
        return png_bytes.getvalue()
    except Exception:
        return None
