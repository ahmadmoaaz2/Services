import mysql.connector
import yaml

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())['datastore']

conn = mysql.connector.connect(host=app_config['hostname'], database=app_config['db'], user=app_config['user'], password=app_config['password'])

c = conn.cursor()
c.execute('''DROP TABLE food_and_water_readings, cage_readings;''')

conn.commit()
conn.close()
