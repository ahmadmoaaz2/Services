import sqlite3

conn = sqlite3.connect('readings.sqlite')

c = conn.cursor()
c.execute('''DROP TABLE food_and_water_readings;''')
c.execute('''DROP TABLE cage_readings;''')

conn.commit()
conn.close()
