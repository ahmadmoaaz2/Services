import json
from sqlalchemy import Column, Integer, String, Float
from base import Base
from datetime import datetime


class CageReadings(Base):
    """ Heart Rate """

    __tablename__ = "cage_readings"

    id = Column(Integer, primary_key=True)
    temperature = Column(Integer)
    humidity_percentage = Column(Integer)
    air_quality_percentage = Column(Integer)
    lux = Column(Float)
    date_created = Column(String(100), nullable=False)
    dropping_buildup_percentage = Column(Integer)
    bird_locations = Column(String(500))

    def __init__(self, temperature, humidity_percentage, air_quality_percentage, lux, dropping_buildup_percentage, bird_locations):
        """ Initializes a heart rate reading """
        self.temperature = temperature
        self.humidity_percentage = humidity_percentage
        self.air_quality_percentage = air_quality_percentage
        self.lux = lux
        self.dropping_buildup_percentage = dropping_buildup_percentage
        self.bird_locations = json.dumps(bird_locations)
        self.date_created = datetime.now()

    def to_dict(self):
        """ Dictionary Representation of a heart rate reading """
        return {
            'id': self.id,
            'temperature': self.temperature,
            'humidity_percentage': self.humidity_percentage,
            'air_quality_percentage': self.air_quality_percentage,
            'lux': self.lux,
            'dropping_buildup_percentage': self.dropping_buildup_percentage,
            'bird_locations': self.bird_locations,
            'date_created': self.date_created
        }
