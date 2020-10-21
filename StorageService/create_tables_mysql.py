import mysql.connector
import yaml

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())['datastore']

conn = mysql.connector.connect(host=app_config['hostname'], database=app_config['db'], user=app_config['user'], password=app_config['password'])

c = conn.cursor()
c.execute('''
          CREATE TABLE food_and_water_readings
          (id INTEGER NOT NULL AUTO_INCREMENT, 
           name VARCHAR(250) NOT NULL,
           date_created DATETIME NOT NULL,
           var1_name VARCHAR(250),
           var1_value VARCHAR(250),
           var2_name VARCHAR(250),
           var2_value VARCHAR(250),
           var3_name VARCHAR(250),
           var3_value VARCHAR(250),
           var4_name VARCHAR(250),
           var4_value VARCHAR(250),
           var5_name VARCHAR(250),
           var5_value VARCHAR(250),
           CONSTRAINT food_and_water_reading_pk PRIMARY KEY (id))
          ''')

c.execute('''
          CREATE TABLE cage_readings
          (id INTEGER NOT NULL AUTO_INCREMENT, 
           temperature INTEGER,
           humidity_percentage INT(3),
           air_quality_percentage INT(3),
           lux FLOAT,
           date_created DATETIME NOT NULL,
           dropping_buildup_percentage INT(3),
           bird_locations VARCHAR(500),
           CONSTRAINT food_and_water_reading_pk PRIMARY KEY (id))
          ''')

conn.commit()
conn.close()
