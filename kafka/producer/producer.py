from confluent_kafka import Producer
import requests
import json
import time
import os

def fetch_latest_aq(endpoint_url):
    api_key = os.environ.get('API_KEY')
    headers = {
        'X-API-Key': api_key
    }
    response = requests.get(endpoint_url, headers=headers)
    response.raise_for_status()
    return response.json()

def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}')

def publish_data(producer, topic, data):
    producer.produce(topic, json.dumps(data).encode('utf-8'), callback=delivery_report)
    producer.flush()

def main():
    kafka_server_address = os.environ.get('KAFKA_SERVER_ADDRESS')
    topic = os.environ.get('KAFKA_TOPIC')
    api_endpoint = os.environ.get('API_ENDPOINT')

    kafka_config = {
    'bootstrap.servers': kafka_server_address,
    'client.id': 'KafkaETLProducer'
    }

    producer = Producer(kafka_config)

    while True:
        try:
            data = fetch_latest_aq(api_endpoint)
            publish_data(producer, topic, data)
        except Exception as e:
            print(f'An error occurred: {e}')
        time.sleep(1)

if __name__ == '__main__':
    main()
