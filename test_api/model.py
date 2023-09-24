import json
from datetime import datetime

class PirData:
    def __init__(self, sensor_id, status, value=0):
        self.sensor_id = sensor_id
        self.status = status
        self.value = value
        self.timestamp = datetime.now()

    def __str__(self):
        return f"{self.sensor} {self.status} {self.timestamp}"
    

class CameraData:
    def __init__(self, sensor_id, status, image_data=""):
        self.sensor_id = sensor_id
        self.status = status
        self.image_data = image_data
        self.timestamp = datetime.now()
    def __str__(self) -> str:
        return f"{self.sensor} {self.status} {self.timestamp} {self.image_data}"


class VanData:
    def __init__(self, van_id, status, image_data, driver_name, passenger, speed=80):
        self.van_id = van_id
        self.status = status
        self.image_data = image_data
        self.timestamp = datetime.now()
        self.driver_name = driver_name
        self.passenger = passenger
        self.created_at = datetime.now()
        self.speed = speed


    def __str__(self) -> str:
        return f"{self.van_id} {self.status} {self.timestamp} {self.image_data} {self.driver_name} {self.passenger} {self.speed}"