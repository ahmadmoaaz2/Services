import json
import logging
import logging.config
import os
from datetime import datetime, date
from flask_cors import CORS, cross_origin
import connexion
import yaml
from apscheduler.schedulers.background import BackgroundScheduler
from connexion import NoContent
import requests

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


def populate_stats():
    logger.info("Periodic processing has started")
    stats = {
        'num_of_readings': 0,
        'num_of_cage_readings': 0,
        'num_of_food_and_water_readings': 0,
        'last_requested': "01/01/2000-01:01:01"
    }
    if os.path.isfile(app_config['datastore']['filename']):
        with open(app_config['datastore']['filename'], 'r') as file:
            stats = json.loads(file.read())
    food_and_water_stats_request = requests.get("{}/foodAndWater?timestamp={}".format(app_config['eventstore']['url'], stats['last_requested']))
    cage_stats_request = requests.get("{}/cageReadings?timestamp={}".format(app_config['eventstore']['url'], stats['last_requested']))
    stats['last_requested'] = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    if food_and_water_stats_request.status_code != 200:
        logger.error("Food and water stats request with url '{}' failed with response code '{}' and response body '{}'".format(
            food_and_water_stats_request.url, food_and_water_stats_request.status_code, food_and_water_stats_request.text
        ))
    else:
        logger.info("Food and water stats request succeeded with url '{}' and a response length of {}".format(food_and_water_stats_request.url, len(food_and_water_stats_request.json())))
        stats['num_of_food_and_water_readings'] += len(food_and_water_stats_request.json())
        stats['num_of_readings'] += len(food_and_water_stats_request.json())

    if cage_stats_request.status_code != 200:
        logger.error("Cage stats request with url '{}' failed with response code '{}' and response body '{}'".format(cage_stats_request.url, cage_stats_request.status_code, cage_stats_request.text))
    else:
        logger.info("Cage stats request succeeded with url '{}' and a response length of {}".format(cage_stats_request.url, len(cage_stats_request.json())))
        stats['num_of_cage_readings'] += len(cage_stats_request.json())
        stats['num_of_readings'] += len(cage_stats_request.json())

    with open(app_config['datastore']['filename'], 'w') as file:
        file.write(json.dumps(stats))
    logger.debug("Updated data.json stats. New stats: {}".format(json.dumps(stats)))
    logger.info("Periodic processing service has stopped")


def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats,
                  'interval',
                  seconds=app_config['scheduler']['period_sec'])
    sched.start()


def get_stats():
    logger.info("Get stats request has been called")
    if os.path.isfile(app_config['datastore']['filename']):
        with open(app_config['datastore']['filename']) as file:
            stats = json.loads(file.read())
            logger.debug("Read stats from file: {}".format(file.read()))
    else:
        logger.error("Statistics do not exist")
        return {'message': "Statistics do not exist"}, 404
    del stats['last_requested']
    logger.info("Get stats successfully exited")
    return stats, 200


app = connexion.FlaskApp(__name__, specification_dir="")
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api("openapi.yml", base_path="/processing", strict_validation=True, validate_responses=True)

if __name__ == '__main__':
    init_scheduler()
    app.run(port=8100)
