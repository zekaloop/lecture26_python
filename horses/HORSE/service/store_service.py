from dao.horse_dao import HorseDAO

class StoreService:
    def __init__(self):
        self.horse_dao = HorseDAO()
        
    def buy_horse(self, horse_id, member):
        horse = self.horse_dao.get_horse_by_id(horse_id)
        
        if horse == None or horse.owner != "시스템":
            return "없는말"
        if member.money < horse.price:
            return "돈부족"
            
        member.money -= horse.price
        horse.owner = member.name
        member.my_horses.append(horse)
        return "구매성공"