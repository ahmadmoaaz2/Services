from datetime import datetime

import connexion
import yaml
import logging.config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from food_and_water_readings import FoodAndWaterReadings
from cage_readings import CageReadings


def extract_from_body(d, *keys):
    return [d[k] if k in d else None for k in keys]


with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())['datastore']
[
    user,
    password,
    hostname,
    port,
    db
] = extract_from_body(app_config, 'user', 'password', 'hostname', 'port', 'db')
DB_ENGINE = create_engine('mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, hostname, port, db))
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')


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
    return list_of_ids, 201


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
    return [data_id], 201


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

if __name__ == '__main__':
    app.run(port=8090)
