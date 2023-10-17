FROM python:3.9-slim

WORKDIR /aurorabot

COPY . /aurorabot

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

ENV NAME World

CMD ["python", "aurora_bot/main.py"]