FROM python:3-alpine

RUN pip install gunicorn

ADD requirements.txt /
RUN pip install -r requirements.txt

ADD app.py /

CMD gunicorn -b 0.0.0.0 app:app
