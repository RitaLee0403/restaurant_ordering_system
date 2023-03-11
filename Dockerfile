FROM python:3.10.9



RUN mkdir -p /usr/src/app

COPY requirements.txt /usr/src/app/requirements.txt

RUN python3 -m pip install -r /usr/src/app/requirements.txt


WORKDIR /usr/src/app

COPY . /usr/src/app

EXPOSE 3000

CMD ["python3","app.py"]