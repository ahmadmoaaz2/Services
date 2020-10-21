import logging
import logging.config
import connexion
import yaml
from connexion import NoContent
import requests

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')


def test_food_and_water(body):
    logger.info("Received event /foodAndWater request")
    r = requests.post(app_config["eventstore1"]["url"], json=body)
    logger.info("Returned event %s response with the following unique ids %s and a status code of %s" %
                ("/foodAndWater", r.json(), r.status_code))
    return NoContent, r.status_code


def test_cage_readings(body):
    logger.info("Received event /cageReadings request")
    r = requests.post(app_config["eventstore2"]["url"], json=body)
    logger.info("Returned event %s response with the following unique ids %s and a status code of %s" %
                ("/cageReadings", r.json(), r.status_code))
    return NoContent, r.status_code


app = connexion.FlaskApp(__name__, specification_dir="")
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == '__main__':
    app.run(port=8080)
