class MemberService:
    def __init__(self, member_dao): self.__member_dao = member_dao

    def register(self, member):
        if self.__member_dao.select_member(member.get_member_id()):
            print("[실패] 이미 사용 중인 아이디입니다.")
            return False
        if self.__member_dao.insert_member(member):
            print(f"[성공] 회원 가입 완료!")
            return True
        return False

    def login(self, member_id, password):
        member = self.__member_dao.select_member(member_id)
        if member and member.get_password() == password:
            return True
        print("[실패] 아이디 또는 비밀번호가 일치하지 않습니다.")
        return False

    def get_member_info(self, member_id): return self.__member_dao.select_member(member_id)

    def change_password(self, member_id, new_password):
        member = self.__member_dao.select_member(member_id)
        member.set_password(new_password)
        print("[성공] 비밀번호가 변경되었습니다.")

    def withdraw(self, member_id):
        self.__member_dao.delete_member(member_id)
        print("[성공] 회원 탈퇴가 완료되었습니다.")

    def show_all_members(self):
        members = self.__member_dao.select_all_members()
        print("\n--- 👥 회원 목록 ---")
        for m_id, m in members.items():
            role = "관리자" if m.get_is_admin() else "일반회원"
            
            print(f"[{m_id}] 이름: {m.get_name()} | 등급: {role}")
