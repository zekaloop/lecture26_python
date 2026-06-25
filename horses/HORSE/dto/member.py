class MemberDTO:
    def __init__(self, user_id, password, name, money, is_admin=False):
        self.user_id = user_id
        self.password = password
        self.name = name
        self.money = money
        self.my_horses = []
        self.is_admin = is_admin