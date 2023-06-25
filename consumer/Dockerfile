# basic python image
FROM python:3.7

# install pika to access rabbitmq
RUN pip install pika
RUN pip install requests
RUN pip install Pillow
RUN pip install prisma
# Without this setting, Python never prints anything out.
ENV PYTHONUNBUFFERED=1

# declare the source directory
WORKDIR /usr/src/app/consumer

# copy the file
COPY consumer.py .

# start command
CMD [ "python", "consumer.py" ]