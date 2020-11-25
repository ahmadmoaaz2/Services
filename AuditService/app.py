import logging
import logging.config
import connexion
import yaml
from pykafka import KafkaClient
import json
from flask_cors import CORS, cross_origin
import os


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


def get_food_and_water(index):
    hostname: str = "%s:%d" % (app_config["events"]["hostname"],
                          app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[app_config["events"]["topic"]]
    # Here we reset the offset on start so that we retrieve
    # messages at the beginning of the message queue.
    # To prevent the for loop from blocking, we set the timeout to
    # 100ms. There is a risk that this loop never stops if the
    # index is large and messages are constantly being received!
    consumer = topic.get_simple_consumer(
        reset_offset_on_start=True,
        consumer_timeout_ms=500
    )
    logger.info("Retrieving food and water reading at index %d" % index)
    food_and_water = []
    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        if msg['type'] == "food_and_water":
            food_and_water.append(msg)

    if len(food_and_water) - 1 < index:
        logger.error("Could not find food and water reading at index %d" % index)
        return {"message": "Not Found. Reading does not exist at this index."}, 404
    return food_and_water[index]['payload'], 200


def get_cage_reading(index):
    hostname = "%s:%d" % (app_config["events"]["hostname"],
                          app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[app_config["events"]["topic"]]
    # Here we reset the offset on start so that we retrieve
    # messages at the beginning of the message queue.
    # To prevent the for loop from blocking, we set the timeout to
    # 100ms. There is a risk that this loop never stops if the
    # index is large and messages are constantly being received!
    consumer = topic.get_simple_consumer(reset_offset_on_start=True,
                                         consumer_timeout_ms=500)
    logger.info("Retrieving cage reading at index %d" % index)
    cage_readings = []
    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        if msg['type'] == "cage_reading":
            cage_readings.append(msg)

    if len(cage_readings) - 1 < index:
        logger.error("Could not find cage reading at index %d" % index)
        return {"message": "Not Found. Reading does not exist at this index."}, 404
    return cage_readings[index]['payload'], 200


app = connexion.FlaskApp(__name__, specification_dir="")
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api("openapi.yml", base_path="/audit_log", strict_validation=True, validate_responses=True)

if __name__ == '__main__':
    app.run(port=8110)
