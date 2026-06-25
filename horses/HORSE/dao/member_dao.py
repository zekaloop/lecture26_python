from dto.member import MemberDTO

class MemberDAO:
    def __init__(self):
        self.members = [
            MemberDTO("admin", "9999", "운영자", 100000000, is_admin=True),
            MemberDTO("user1", "1234", "초보마주", 10000)
        ]
        
    def get_all_members(self):
        return self.members
        
    def get_member_by_id(self, user_id):
        for m in self.members:
            if m.user_id == user_id:
                return m
        return None
        
    def add_member(self, new_member):
        self.members.append(new_member)
        
    def delete_member(self, user_id):
        self.members = [m for m in self.members if m.user_id != user_id]