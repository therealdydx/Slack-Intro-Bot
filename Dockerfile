# Dockerfile, Image, Container
FROM python:3.8

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

RUN pip3 install slackclient --upgrade

COPY . .

# CMD [ "python", "main.py"]

EXPOSE 5000

ENV FLASK_APP=app.py

CMD ["flask", "run", "--host", "0.0.0.0"]
