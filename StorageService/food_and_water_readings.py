from sqlalchemy import Column, Integer, String
from base import Base
from datetime import datetime


class FoodAndWaterReadings(Base):
    """ Food and Water Readings Class """

    __tablename__ = "food_and_water_readings"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    var1_name = Column(String(250))
    var1_value = Column(String(250))
    var2_name = Column(String(250))
    var2_value = Column(String(250))
    var3_name = Column(String(250))
    var3_value = Column(String(250))
    var4_name = Column(String(250))
    var4_value = Column(String(250))
    var5_name = Column(String(250))
    var5_value = Column(String(250))
    date_created = Column(String(100), nullable=False)

    def __init__(self, name, var1_name, var1_value, var2_name, var2_value, var3_name, var3_value, var4_name, var4_value, var5_name, var5_value):
        """ Initializes a blood pressure reading """
        self.name = name
        self.var1_name = var1_name
        self.var1_value = var1_value
        self.var2_name = var2_name
        self.var2_value = var2_value
        self.var3_name = var3_name
        self.var3_value = var3_value
        self.var4_name = var4_name
        self.var4_value = var4_value
        self.var5_name = var5_name
        self.var5_value = var5_value
        self.date_created = datetime.now()

    def to_dict(self):
        """ Dictionary Representation of a blood pressure reading """
        return {
            'id': self.id,
            'name': self.name,
            'var1_name': self.var1_name,
            'var1_value': self.var1_value,
            'var2_name': self.var2_name,
            'var2_value': self.var2_value,
            'var3_name': self.var3_name,
            'var3_value': self.var3_value,
            'var4_name': self.var4_name,
            'var4_value': self.var4_value,
            'var5_name': self.var5_name,
            'var5_value': self.var5_value,
            'date_created': self.date_created
        }
