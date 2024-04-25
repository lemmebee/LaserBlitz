FROM python:3.8-slim

WORKDIR /producer

COPY producer/producer.py requirements.txt Makefile /producer/

RUN pip install --no-cache-dir -r ./requirements.txt

CMD ["python", "./producer.py"]
