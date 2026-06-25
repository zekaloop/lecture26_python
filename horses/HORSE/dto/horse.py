import uuid
import random

class HorseDTO:
    def __init__(self, name, color, price):
        self.horse_id = str(uuid.uuid4())[:4]
        self.name = name
        self.color = color
        self.price = price
        self.owner = "시스템"
        self.speed = random.randint(2, 4)
        self.pos = 0