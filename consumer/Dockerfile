FROM python:3.7

RUN pip install pika
RUN pip install requests
RUN pip install prisma

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app/consumer

COPY consumer.py .

CMD [ "python", "consumer.py" ]