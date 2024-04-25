FROM python:3.8-slim

WORKDIR /consumer

COPY consumer/consumer.py requirements.txt Makefile /consumer/

RUN pip install --no-cache-dir -r ./requirements.txt

CMD ["python", "./consumer.py"]
