class MemberDAO:
    def __init__(self):
        self.__db = {}

    def insert_member(self, member):
        if member.get_member_id() in self.__db: return False 
        self.__db[member.get_member_id()] = member
        return True

    def select_member(self, member_id):
        return self.__db.get(member_id, None)

    def select_all_members(self):
        return self.__db

    def delete_member(self, member_id):
        if member_id in self.__db:
            del self.__db[member_id]
            return True
        return False