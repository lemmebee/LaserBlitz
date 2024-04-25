from confluent_kafka import Consumer, KafkaError
import os
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')

def consume_data(topic, server):
    consumer_config = {
        'bootstrap.servers': server,
        'group.id': 'KafkaETLConsumerGroup',
        'auto.offset.reset': 'earliest'
    }

    consumer = Consumer(consumer_config)
    consumer.subscribe([topic])

    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    logging.error(json.dumps({"consumer_error": str(msg.error())}))
                    break
            data = json.loads(msg.value())
            if 'results' in data and isinstance(data['results'], list):
                for item in data['results']:
                        logging.info(json.dumps({
                            "country": item['country'],
                            "city": item['city'],
                            "latitude": item['coordinates']['latitude'],
                            "longitude": item['coordinates']['longitude'],
                            "measurements": item['measurements']
                            }))

    except KeyboardInterrupt:
        logging.info("Interrupted by user")
    finally:
        logging.info("Closing consumer...")
        consumer.close()

if __name__ == '__main__':
    topic = os.environ.get('KAFKA_TOPIC')
    kafka_server_address = os.environ.get('KAFKA_SERVER_ADDRESS')
    consume_data(topic, kafka_server_address)
