from Member.member import Member
from Member.member_dao import MemberDAO
from Member.member_service import MemberService
from Account.account import Account
from Account.account_dao import AccountDAO
from Account.account_service import AccountService

class ConsoleBank:
    # 메뉴판 내용 채우기
    start_menu = ['종료', '로그인', '회원가입']
    banking_menu = ['로그아웃', '내 계좌 목록', '입금', '출금', '계좌 생성', '계좌 삭제', '내 정보']
    member_myinfo_menu = ['뒤로가기', '내 정보 보기', '비밀번호 변경', '회원 탈퇴']
    admin_menu = ['로그아웃', '회원 관리', '계좌 관리']
    admin_account_menu = ['뒤로가기', '전체 계좌 목록', '특정 회원 계좌 목록']
    admin_member_menu = ['뒤로가기', '전체 회원 목록', '회원 정보 보기', '회원 강제 탈퇴']

    def __init__(self):
        self.msv = MemberService(MemberDAO())
        self.asv = AccountService(AccountDAO())

    def main(self):
        self.show_welcome()
        self.run_start_menu()
        self.say_goodbye()

    def show_welcome(self):
        print('======== SinChangsup Console Bank ==========')

    def say_goodbye(self):
        print('>> SinChangsup Console Bank를 이용해 주셔서 감사합니다.')

    def select_menu(self, menu_list):
        print('\n-----------------------')
        for index in range(1, len(menu_list)):
            print(f'{index}. {menu_list[index]}')
        print(f'0. {menu_list[0]}')
        print('-----------------------')
        try:
            num = int(input("메뉴 번호: "))
            return num
        except ValueError:
            print("숫자만 입력해주세요!")
            return -1

    # ==========================================
    # 1. 시작 메뉴 (로그인 / 회원가입)
    # ==========================================
    def run_start_menu(self):
        while True:
            menu = self.select_menu(ConsoleBank.start_menu)
            if menu == 0: 
                break
            elif menu == 1:
                self.menu_login()
            elif menu == 2:
                self.menu_join()

    def menu_join(self):
        print('\n>>>> 회원가입 <<<<')
        user_id = input("사용할 ID: ")
        password = input("비밀번호: ")
        name = input("이름: ")
        
        # 새 손님 명찰(Member)을 만들어서 매니저(msv)에게 등록해달라고 합니다.
        new_member = Member(user_id, password, name)
        if self.msv.join(new_member):
            print("회원가입이 완료되었습니다!")
        else:
            print("이미 존재하는 ID입니다.")

    def menu_login(self):
        print('\n>>>> 로그인 <<<<')
        user_id = input("ID: ")
        password = input("비밀번호: ")
        
        # 매니저에게 신분증 검사를 맡깁니다.
        if self.msv.login(user_id, password):
            print("로그인 성공!")
            # 관리자(admin)인지 일반 손님인지에 따라 보여주는 메뉴판이 다릅니다.
            if self.msv.current_user == MemberService.ADMIN_ID:
                self.run_admin_menu()
            else:
                self.run_banking_menu()
        else:
            print("ID나 비밀번호가 틀렸습니다.")

    def menu_logout(self):
        self.msv.logout()
        print("안전하게 로그아웃 되었습니다.")

    # ==========================================
    # 2. 일반 손님 은행 업무 메뉴
    # ==========================================
    def run_banking_menu(self):
        while True:
            menu = self.select_menu(ConsoleBank.banking_menu)
            if menu == 0:
                self.menu_logout()
                break
            elif menu == 1: self.menu_list_my_accounts()
            elif menu == 2: self.menu_deposit()
            elif menu == 3: self.menu_withdraw()
            elif menu == 4: self.menu_create_account()
            elif menu == 5: self.menu_delete_account()
            elif menu == 6: self.run_my_info_menu()

    def menu_list_my_accounts(self):
        print('\n>>>> 내 계좌 목록 <<<<')
        my_id = self.msv.current_user
        accounts = self.asv.get_members_accounts(my_id)
        
        if accounts:
            for acc in accounts:
                print(acc)
        else:
            print("개설된 계좌가 없습니다.")

    def menu_deposit(self):
        print('\n>>>> 입금 <<<<')
        acc_no = input("입금할 계좌번호: ")
        amount = int(input("입금할 금액: "))
        
        if self.asv.deposit(acc_no, amount):
            print(f"{amount}원이 입금되었습니다.")
        else:
            print("계좌번호를 다시 확인해주세요.")

    def menu_withdraw(self):
        print('\n>>>> 출금 <<<<')
        acc_no = input("출금할 계좌번호: ")
        password = input("계좌 비밀번호: ")
        amount = int(input("출금할 금액: "))
        
        # 매니저(AccountService)가 깐깐하게 검사해서 에러를 던지면, 직원이 잘 받아줍니다.
        try:
            self.asv.withdraw(self.msv.current_user, acc_no, amount, password)
            print("출금이 완료되었습니다.")
        except LookupError:
            print("없는 계좌번호입니다.")
        except KeyError:
            print("비밀번호가 틀렸거나 본인 계좌가 아닙니다.")
        except ValueError:
            print("잔액이 부족합니다.")

    def menu_create_account(self):
        print('\n>>>> 계좌 생성 <<<<')
        password = input("새 통장에 쓸 비밀번호: ")
        first_deposit = int(input("초기 입금액: "))
        
        # 번호는 매니저가 자동으로 만드니까 0으로 넣고 넘깁니다.
        my_id = self.msv.current_user
        new_account = Account(0, my_id, first_deposit, password)
        
        if self.asv.create_account(new_account):
            print("새로운 계좌가 생성되었습니다!")
        else:
            print("계좌 생성에 실패했습니다.")

    def menu_delete_account(self):
        print('\n>>>> 계좌 삭제 <<<<')
        acc_no = input("삭제할 계좌번호: ")
        password = input("계좌 비밀번호: ")
        
        try:
            self.asv.delete_account(self.msv.current_user, acc_no, password)
            print("계좌가 정상적으로 해지되었습니다.")
        except LookupError:
            print("없는 계좌번호입니다.")
        except KeyError:
            print("비밀번호가 틀렸거나 본인 계좌가 아닙니다.")
        except ValueError:
            print("통장에 돈이 남아있어서 해지할 수 없습니다. 먼저 출금해주세요.")

    # ==========================================
    # 3. 내 정보 메뉴
    # ==========================================
    def run_my_info_menu(self):
        while True:
            menu = self.select_menu(ConsoleBank.member_myinfo_menu)
            if menu == 0: break
            elif menu == 1: self.menu_view_myinfo()
            elif menu == 2: self.menu_update_password()
            elif menu == 3: 
                # 회원 탈퇴를 하면 은행 메뉴에서도 나가야 하니 break로 끝내줍니다.
                if self.menu_delete_membership():
                    break

    def menu_view_myinfo(self):
        print('\n>>>> 내 정보 보기 <<<<')
        info = self.msv.view_member_info(self.msv.current_user)
        print(info)

    def menu_update_password(self):
        print('\n>>>> 비밀번호 변경 <<<<')
        org_pw = input("현재 비밀번호: ")
        new_pw = input("새로운 비밀번호: ")
        
        if self.msv.update_member_password(self.msv.current_user, org_pw, new_pw):
            print("비밀번호가 변경되었습니다.")
        else:
            print("비밀번호 변경에 실패했습니다.")

    def menu_delete_membership(self):
        print('\n>>>> 회원 탈퇴 <<<<')
        check = input("정말로 탈퇴하시겠습니까? (y/n): ")
        if check.lower() == 'y':
            self.msv.remove_member(self.msv.current_user)
            self.menu_logout()
            print("회원 탈퇴가 완료되었습니다.")
            return True
        return False

    # ==========================================
    # 4. 관리자 메뉴 (Admin)
    # ==========================================
    def run_admin_menu(self):
        while True:
            menu = self.select_menu(ConsoleBank.admin_menu)
            if menu == 0:
                self.menu_logout()
                break
            elif menu == 1: self.run_admin_member_menu()
            elif menu == 2: self.run_admin_account_menu()

    def run_admin_member_menu(self):
        while True:
            menu = self.select_menu(ConsoleBank.admin_member_menu)
            if menu == 0: break
            elif menu == 1:
                members = self.msv.list_members()
                for m in members: print(m)
            elif menu == 2:
                target_id = input("조회할 ID: ")
                print(self.msv.view_member_info(target_id))
            elif menu == 3:
                target_id = input("강제 탈퇴시킬 ID: ")
                self.msv.remove_member(target_id)
                print(f"{target_id} 회원을 강제 탈퇴시켰습니다.")

    def run_admin_account_menu(self):
        while True:
            menu = self.select_menu(ConsoleBank.admin_account_menu)
            if menu == 0: break
            elif menu == 1:
                accounts = self.asv.get_all_accounts()
                if accounts:
                    for acc in accounts: print(acc)
            elif menu == 2:
                target_id = input("조회할 회원 ID: ")
                accounts = self.asv.get_members_accounts(target_id)
                if accounts:
                    for acc in accounts: print(acc)
                else:
                    print("해당 회원의 계좌가 없습니다.")

if __name__ == '__main__':
    app = ConsoleBank()
    app.main()