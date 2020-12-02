import logging
import logging.config
import connexion
import yaml
from connexion import NoContent
import requests
import os
from datetime import datetime
from pykafka import KafkaClient
import json

if "TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test":
    print("In Test Environment")
    app_conf_file = "/config/app_conf.yml"
    log_conf_file = "/config/log_conf.yml"
else:
    print("In Dev Environment")
    app_conf_file = "app_conf.yml"
    log_conf_file = "log_conf.yml"

with open(app_conf_file, 'r') as f:
    app_config = yaml.safe_load(f.read())

# External Logging Configuration
with open(log_conf_file, 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')
logger.info("App Conf File: %s" % app_conf_file)
logger.info("Log Conf File: %s" % log_conf_file)

client = None
topic = None
producer = None


def test_food_and_water(body):
    global client, topic, producer
    if client is None or topic is None or producer is None:
        client = KafkaClient(hosts='{}:{}'.format(app_config['events']['hostname'], app_config['events']['port']))
        topic = client.topics[app_config['events']['topic']]
        producer = topic.get_sync_producer()
    logger.info("Received event /foodAndWater request")
    msg = {"type": "food_and_water",
           "datetime": datetime.now().strftime(
               "%d/%m/%Y-%H:%M:%S"),
           "payload": body}
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    return NoContent, 201


def test_cage_readings(body):
    global client, topic, producer
    if client is None or topic is None or producer is None:
        client = KafkaClient(hosts='{}:{}'.format(app_config['events']['hostname'], app_config['events']['port']))
        topic = client.topics[app_config['events']['topic']]
        producer = topic.get_sync_producer()
    logger.info("Received event /cageReadings request")
    msg = {"type": "cage_reading",
           "datetime": datetime.now().strftime(
               "%d/%m/%Y-%H:%M:%S"),
           "payload": body}
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    return NoContent, 201


app = connexion.FlaskApp(__name__, specification_dir="")
app.add_api("openapi.yml", base_path="/receiver", strict_validation=True, validate_responses=True)

if __name__ == '__main__':
    app.run(port=8080)
