from dao.member_dao import MemberDAO
from dto.member import MemberDTO

class MemberService:
    def __init__(self):
        self.dao = MemberDAO()
        self.login_member = None
        
    def login(self, uid, upw):
        member = self.dao.get_member_by_id(uid)
        if member and member.password == upw:
            self.login_member = member
            return "성공"
        return "실패"
        
    def register(self, uid, upw, name):
        if self.dao.get_member_by_id(uid) != None:
            return "중복" 
        new_member = MemberDTO(uid, upw, name, 10000)
        self.dao.add_member(new_member)
        return "가입완료"
        
    def withdraw(self, upw):
        if self.login_member.password == upw:
            self.dao.delete_member(self.login_member.user_id)
            self.login_member = None
            return "탈퇴완료"
        return "비번틀림"