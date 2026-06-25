import time
import os
from service.member_service import MemberService
from service.store_service import StoreService
from service.race_service import RaceService

RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

class HorseConsole:
    def __init__(self):
        self.member_service = MemberService()
        self.store_service = StoreService()
        self.race_service = RaceService()

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def start(self):
        while True:
            self.clear_screen()
            print(f"{YELLOW}=== 🐴 말 육성 & 거래 스토어 입구 ==={RESET}")
            print("1. 로그인")
            print("2. 회원가입 (신규 마주)")
            print("0. 게임 종료")
            
            choice = input("\n선택: ")
            
            if choice == '1':
                uid = input("ID: ")
                upw = input("PW: ")
                if self.member_service.login(uid, upw) == "성공":
                    self.show_lobby()
                else:
                    print("\n❌ 로그인 실패! 아이디나 비밀번호를 확인하세요.")
                    input()
                    
            elif choice == '2':
                print("\n[ 신규 마주 가입 ]")
                uid = input("사용할 ID: ")
                upw = input("사용할 PW: ")
                name = input("마주 이름(닉네임): ")
                
                result = self.member_service.register(uid, upw, name)
                if result == "중복": 
                    print("\n❌ 이미 존재하는 ID입니다.")
                else: 
                    print("\n🎉 가입을 환영합니다! 초기 정착금 10,000원이 지급되었습니다.")
                input("엔터를 눌러 계속하세요...")
                
            elif choice == '0': 
                break

    def show_lobby(self):
        while True:
            self.clear_screen()
            member = self.member_service.login_member
            print(f"=== 🏟️ 스토어 로비 (접속자: {member.name}) ===")
            print(f"💰 잔액: {member.money}원 | 🐎 소유 말: {len(member.my_horses)}마리")
            print("-----------------------------------------")
            print("1. 말 거래소 (명마 입양하기)")
            print("2. 내 마구간 (보유 말 확인 및 출전)")
            
            if member.is_admin:
                print(f"{RED}99. [관리자 전용] 유저 관리 시스템{RESET}")
                
            print("3. 회원 탈퇴 (계정 영구 삭제)")
            print("0. 로그아웃")
            
            choice = input("\n선택: ")
            
            if choice == '1': 
                self.show_store()
            elif choice == '2': 
                self.show_my_stable()
            elif choice == '3':
                pw_check = input("\n정말 탈퇴하시겠습니까? 비밀번호를 입력하세요: ")
                if self.member_service.withdraw(pw_check) == "탈퇴완료":
                    print("😢 그동안 이용해주셔서 감사합니다. 계정이 삭제되었습니다.")
                    input()
                    break
                else:
                    print("❌ 비밀번호가 틀렸습니다. 탈퇴가 취소됩니다.")
                    input()
            elif choice == '99' and member.is_admin:
                self.show_admin_menu()
            elif choice == '0':
                self.member_service.login_member = None
                break

    def show_store(self):
        self.clear_screen()
        print(f"=== 🏪 말 거래소 ===")
        print("최고의 혈통을 자랑하는 명마들을 입양하세요!\n")
        
        horses_for_sale = [h for h in self.store_service.horse_dao.get_all_horses() if h.owner == "시스템"]
        
        for h in horses_for_sale:
            print(f"[{h.horse_id}] {h.color}{h.name}{RESET} | 가격: {h.price}원 | 타고난 스피드: {YELLOW}★{h.speed}{RESET}")
            
        t_id = input("\n입양할 말의 ID를 입력하세요 (취소: 엔터): ")
        if t_id != "":
            member = self.member_service.login_member
            result = self.store_service.buy_horse(t_id, member)
            
            if result == "구매성공": 
                print("\n🎉 입양 완료! 내 마구간에서 확인하세요.")
            elif result == "돈부족":
                print("\n❌ 잔액이 부족합니다.")
            else: 
                print("\n❌ 이미 팔렸거나 없는 말입니다.")
            input("엔터를 누르면 로비로 돌아갑니다...")

    def show_my_stable(self):
        self.clear_screen()
        member = self.member_service.login_member
        print(f"=== 🏠 {member.name}님의 마구간 ===")
        
        if len(member.my_horses) == 0:
            print("\n아직 소유한 말이 없습니다. 거래소에서 입양하세요!")
            input("\n엔터를 누르면 로비로 돌아갑니다...")
            return

        for i, h in enumerate(member.my_horses):
            print(f"{i+1}. [{h.color}{h.name}{RESET}] (ID: {h.horse_id} / 스피드: ★{h.speed})")
            
        print("\n-----------------------------------------")
        print("1. 친선 경마장 출전 (내 말들의 스피드 대결)")
        print("0. 로비로 돌아가기")
        
        choice = input("\n선택: ")
        if choice == '1':
            if len(member.my_horses) < 2:
                print("\n❌ 출전시키려면 최소 2마리 이상의 말이 필요합니다.")
                input()
            else:
                print(f"\n🏁 {member.name}님의 정예 말들이 출전합니다!")
                time.sleep(1)
                self.race_service.start_race(member.my_horses)

    def show_admin_menu(self):
        self.clear_screen()
        print(f"{RED}=== 👑 [관리자 전용] 유저 관리 시스템 ==={RESET}")
        print("현재 가입된 전체 유저 목록입니다:\n")
        
        all_users = self.member_service.dao.get_all_members()
        for u in all_users:
            role = "운영자" if u.is_admin else "일반유저"
            print(f"- ID: {u.user_id} | 닉네임: {u.name} | 잔액: {u.money}원 | 등급: [{role}]")
            
        print("\n강제로 삭제(영구정지)할 유저의 ID를 입력하세요.")
        target_id = input("(취소하려면 엔터): ")
        
        if target_id != "":
            if target_id == "admin":
                print("\n❌ 운영자 본인은 삭제할 수 없습니다!")
            else:
                self.member_service.dao.delete_member(target_id)
                print(f"\n🔨 [영구정지] {target_id} 유저의 계정이 삭제되었습니다.")
        input("\n엔터를 누르면 로비로 돌아갑니다...")

if __name__ == "__main__":
    app = HorseConsole()
    app.start()