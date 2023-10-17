import json
from datetime import datetime

class PirData:
    def __init__(self, sensor_id, status, van_id, value=0):
        self.sensor_id = sensor_id
        self.status = status
        self.value = value
        self.timestamp = datetime.now()
        self.van_id = van_id

    def __str__(self):
        return f"{self.sensor} {self.status} {self.timestamp}"
        
    

class CameraData:
    def __init__(self, sensor_id, status, van_id, image_data=""):
        self.sensor_id = sensor_id
        self.status = status
        self.image_data = image_data
        self.timestamp = datetime.now()
        self.van_id = van_id
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
        self.isOpenNotification = "1"
        self.speed = speed


    def __str__(self) -> str:
        return f"{self.van_id} {self.status} {self.timestamp} {self.image_data} {self.driver_name} {self.passenger} {self.speed}"
    
class SystemConfiguration:
    def __init__(self,id, status, IsOpenNotification, startTime, endTime, listDay):
        self.id = id
        self.status = status
        self.isOpenNotification = IsOpenNotification
        self.startTime = startTime
        self.endTime = endTime
        self.listDay = listDay
        self.timestamp = datetime.now()