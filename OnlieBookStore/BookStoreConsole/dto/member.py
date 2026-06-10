class Member:
    def __init__(self, member_id, password, name, address, is_admin=False):
        self.__member_id = member_id
        self.__password = password
        self.__name = name
        self.__address = address
        self.__is_admin = is_admin

    def get_member_id(self): return self.__member_id
    def get_password(self): return self.__password
    def get_name(self): return self.__name
    def get_address(self): return self.__address
    def get_is_admin(self): return self.__is_admin
    
    def set_password(self, password):
        self.__password = password