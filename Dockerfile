FROM python:3.10

WORKDIR /auth_app

ADD ./requirements.txt /auth_app/requirements.txt

RUN pip install -r requirements.txt

ADD . /auth_app