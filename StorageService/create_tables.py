import sqlite3

conn = sqlite3.connect('readings.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE food_and_water_readings
          (id INTEGER PRIMARY KEY ASC, 
           name VARCHAR(250) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           var1_name VARCHAR(250),
           var1_value VARCHAR(250),
           var2_name VARCHAR(250),
           var2_value VARCHAR(250),
           var3_name VARCHAR(250),
           var3_value VARCHAR(250),
           var4_name VARCHAR(250),
           var4_value VARCHAR(250),
           var5_name VARCHAR(250),
           var5_value VARCHAR(250))
          ''')

c.execute('''
          CREATE TABLE cage_readings
          (id INTEGER PRIMARY KEY ASC, 
           temperature INTEGER,
           humidity_percentage INT(3),
           air_quality_percentage INT(3),
           lux FLOAT,
           date_created VARCHAR(100) NOT NULL,
           dropping_buildup_percentage INT(3),
           bird_locations VARCHAR(500))
          ''')

conn.commit()
conn.close()
