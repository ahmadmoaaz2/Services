from datetime import datetime
import os
import connexion
import yaml
import logging.config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from food_and_water_readings import FoodAndWaterReadings
from cage_readings import CageReadings
import json
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread


def extract_from_body(d, *keys):
    return [d[k] if k in d else None for k in keys]


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

[
    user,
    password,
    hostname,
    port,
    db
] = extract_from_body(app_config['datastore'], 'user', 'password', 'hostname', 'port', 'db')
DB_ENGINE = create_engine('mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, hostname, port, db))
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)


def log_event(event_name, unique_id):
    logger.debug("Stored event {} request with a unique id of {}".format(event_name, unique_id))


def test_food_and_water(body):
    session = DB_SESSION()
    logger.info("Connecting to DB. Hostname:{}, Port: {}".format(hostname, port))
    list_of_ids = []
    for reading in body:
        name = reading["name"]
        del reading["name"]
        keys = list(reading.keys())
        values = list(reading.values())
        while len(keys) < 5:
            keys.append(None)
            values.append(None)
        [
            var1_name,
            var2_name,
            var3_name,
            var4_name,
            var5_name,
        ] = keys
        [
            var1_value,
            var2_value,
            var3_value,
            var4_value,
            var5_value
        ] = values
        data_entry = FoodAndWaterReadings(name, var1_name, var1_value, var2_name, var2_value, var3_name, var3_value, var4_name, var4_value, var5_name, var5_value)
        session.add(data_entry)
        session.commit()
        session.flush()
        list_of_ids.append(data_entry.id)
    session.close()
    log_event("/foodAndWater", list_of_ids)


def test_cage_readings(body):
    session = DB_SESSION()
    logger.info("Connecting to DB. Hostname:{}, Port: {}".format(hostname, port))
    [
        temperature,
        humidity_percentage,
        air_quality_percentage,
        lux,
        dropping_buildup_percentage,
        bird_locations
    ] = extract_from_body(
        body,
        "temperature",
        "humidity_percentage",
        "air_quality_percentage",
        "lux",
        "dropping_buildup_percentage",
        "bird_locations"
    )
    data_entry = CageReadings(temperature, humidity_percentage, air_quality_percentage, lux, dropping_buildup_percentage, bird_locations)
    session.add(data_entry)
    session.commit()
    session.flush()
    data_id = data_entry.id
    session.close()
    log_event("/cageReadings", data_id)


def get_food_and_water(timestamp):
    session = DB_SESSION()
    logger.info("Connecting to DB. Hostname:{}, Port: {}".format(hostname, port))
    timestamp_datetime = datetime.strptime(timestamp, "%d/%m/%Y-%H:%M:%S")
    readings = session.query(FoodAndWaterReadings).filter(FoodAndWaterReadings.date_created >= timestamp_datetime)
    results_list = []
    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()
    logger.info("Query for Food and Water readings after %s returns %d results" % (timestamp, len(results_list)))
    return results_list, 200


def get_cage_readings(timestamp):
    session = DB_SESSION()
    logger.info("Connecting to DB. Hostname:{}, Port: {}".format(hostname, port))
    timestamp_datetime = datetime.strptime(timestamp, "%d/%m/%Y-%H:%M:%S")
    readings = session.query(CageReadings).filter(CageReadings.date_created >= timestamp_datetime)
    results_list = []
    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()
    logger.info("Query for Cage readings after %s returns %d results" % (timestamp, len(results_list)))
    return results_list, 200


app = connexion.FlaskApp(__name__, specification_dir="")
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)


def process_messages():
    """ Process event messages """
    hosts = "%s:%d" % (app_config['events']["hostname"],
                       app_config["events"]["port"])
    client = KafkaClient(hosts=hosts)
    topic = client.topics[app_config["events"]["topic"]]
    consumer = topic.get_simple_consumer(consumer_group='event_group',
                                         reset_offset_on_start=False,
                                         auto_offset_reset=OffsetType.LATEST)

    # This is blocking - it will wait for a new message
    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        logger.info("Message: %s" % msg)
        payload = msg["payload"]
        if msg["type"] == "food_and_water":
            test_food_and_water(payload)
        elif msg["type"] == "cage_reading":
            test_cage_readings(payload)

        # Commit the new message as being read
        consumer.commit_offsets()


if __name__ == '__main__':
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    app.run(port=8090)
