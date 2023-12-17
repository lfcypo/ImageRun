FROM alpine

RUN mkdir /app

COPY . /app

RUN echo "http://mirrors.aliyun.com/alpine/latest-stable/main" > /etc/apk/repositories && \
    echo "http://mirrors.aliyun.com/alpine/latest-stable/community" >> /etc/apk/repositories

# 安装Python
RUN apk update
RUN apk add python3
RUN apk add py-pip

RUN cd /app

RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"
RUN pip install flask flask_cors gevent pillow -i https://mirrors.aliyun.com/pypi/simple/


RUN mkdir /data

ENV IMAGERUN_FILE_SAVEPATH=/data
ENV IMAGERUN_HOST=0.0.0.0
ENV IMAGERUN_PORT=8080
ENV IMAGERUN_FILE_URLPREFIX=http://127.0.0.1:8080/

EXPOSE 8080
EXPOSE 80

CMD python3 /app/App.py
