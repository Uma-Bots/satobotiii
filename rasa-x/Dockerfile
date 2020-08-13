FROM python:3.7

WORKDIR /usr/src/app
RUN pip install rasa-x --extra-index-url https://pypi.rasa.com/simple
COPY ./global.yml /root/.config/rasa/global.yml
WORKDIR /usr/src/app/bot
CMD export RASA_X_PASSWORD="(boquito098)" && rasa x
EXPOSE 5002