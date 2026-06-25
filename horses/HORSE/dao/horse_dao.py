from dto.horse import HorseDTO

RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'

class HorseDAO:
    def __init__(self):
        self.all_horses = [
            HorseDTO("적토마", RED, 5000),
            HorseDTO("흑왕비", BLUE, 4000),
            HorseDTO("백마탄", GREEN, 3500),
            HorseDTO("황금마", YELLOW, 8000)
        ]
        
    def get_all_horses(self):
        return self.all_horses

    def get_horse_by_id(self, horse_id):
        for h in self.all_horses:
            if h.horse_id == horse_id:
                return h
        return None