from dto.member import Member
from dao.member_dao import MemberDAO
from dao.book_dao import BookDAO
from dao.cart_dao import CartDAO
from dao.order_dao import OrderDAO
from service.member_service import MemberService
from service.book_service import BookService
from service.cart_service import CartService
from service.order_service import OrderService

class ConsoleApp:
    def __init__(self):
        self.member_dao = MemberDAO()
        self.book_dao = BookDAO()
        self.cart_dao = CartDAO()
        self.order_dao = OrderDAO()

        self.member_service = MemberService(self.member_dao)
        self.book_service = BookService(self.book_dao)
        self.cart_service = CartService(self.cart_dao, self.book_dao)
        self.order_service = OrderService(self.order_dao, self.book_dao, self.cart_dao)

        self.logged_in_user = None
        self.is_admin_mode = False

        self.member_dao.insert_member(Member("test", "1234", "일반회원", "서울"))
        self.member_dao.insert_member(Member("admin", "1234", "관리자", "본사", is_admin=True))

    def run(self):
        while True:
            if self.logged_in_user is None:
                self.show_start_menu()
            elif self.is_admin_mode:
                self.show_admin_menu()
            else:
                self.show_member_menu()

    # ==========================================
    # 1. 시작 메뉴
    # ==========================================
    def show_start_menu(self):
        print("\n[시작 메뉴] 1. 도서 목록  2. 로그인  3. 회원가입  0. 종료")
        choice = input("선택: ")
        if choice == '1': self.book_service.show_all_books()
        elif choice == '2':
            uid = input("ID: ")
            upw = input("PW: ")
            if self.member_service.login(uid, upw):
                self.logged_in_user = uid
                if self.member_service.get_member_info(uid).get_is_admin():
                    self.is_admin_mode = True
        elif choice == '3':
            uid = input("ID: ")
            upw = input("PW: ")
            name = input("이름: ")
            addr = input("주소: ")
            self.member_service.register(Member(uid, upw, name, addr))
        elif choice == '0': exit()

    # ==========================================
    # 2. 관리자 메뉴
    # ==========================================
    def show_admin_menu(self):
        print("\n[관리자 메뉴] 1.도서목록 2.도서등록 3.도서수정 4.도서삭제 5.회원목록 6.주문목록 9.로그아웃")
        choice = input("선택: ")
        if choice == '1': self.book_service.show_all_books()
        elif choice == '2':
            bid = input("도서번호: ")
            title = input("제목: ")
            price = int(input("가격: "))
            stock = int(input("재고: "))
            self.book_service.register_new_book(bid, title, price, stock)
        elif choice == '3':
            bid = input("수정할 도서번호: ")
            title = input("새 제목: ")
            price = int(input("새 가격: "))
            stock = int(input("새 재고: "))
            self.book_service.update_book_info(bid, title, price, stock)
        elif choice == '4':
            bid = input("삭제할 도서번호: ")
            self.book_service.delete_book(bid)
        elif choice == '5': self.member_service.show_all_members()
        elif choice == '6': self.order_service.show_all_orders()
        elif choice == '9': self.logout()

    # ==========================================
    # 3. 회원 메뉴
    # ==========================================
    def show_member_menu(self):
        print(f"\n[회원 메뉴 - {self.logged_in_user}님] 1.도서목록 2.도서주문(바로결제) 3.장바구니 담기 4.장바구니 보기 5.주문목록 6.내정보 9.로그아웃")
        choice = input("선택: ")
        if choice == '1': self.book_service.show_all_books()
        elif choice == '2':
            bid = input("주문할 도서번호: ")
            qty = int(input("수량: "))
            book = self.book_dao.select_book(bid)
            if book and book["stock"] >= qty:
                items_info = [{"book_id": bid, "qty": qty}]
                total = book["price"] * qty
                self.show_payment_screen(items_info, total, is_from_cart=False)
            else: print("[실패] 재고 부족 또는 없는 도서")
        elif choice == '3':
            bid = input("도서번호: ")
            qty = int(input("수량: "))
            self.cart_service.add_book_to_cart(self.logged_in_user, bid, qty)
        elif choice == '4': self.show_cart_menu()  # 장바구니 서브메뉴 진입
        elif choice == '5': self.order_service.show_my_orders(self.logged_in_user)
        elif choice == '6': self.show_my_info_menu() # 내 정보 서브메뉴 진입
        elif choice == '9': self.logout()

    # ==========================================
    # 4. 장바구니 메뉴 (서브메뉴)
    # ==========================================
    def show_cart_menu(self):
        while True:
            total = self.cart_service.view_cart_and_get_total(self.logged_in_user)
            print("\n[장바구니 메뉴] 1.도서주문(결제) 2.도서삭제 3.장바구니 비우기 0.돌아가기")
            choice = input("선택: ")
            if choice == '1':
                if total > 0:
                    items = self.cart_dao.get_cart_items(self.logged_in_user)
                    items_info = [{"book_id": i.get_book_id(), "qty": i.get_quantity()} for i in items]
                    self.show_payment_screen(items_info, total, is_from_cart=True)
                    break
            elif choice == '2':
                bid = input("삭제할 도서번호: ")
                self.cart_service.remove_book(self.logged_in_user, bid)
            elif choice == '3':
                self.cart_service.clear_cart(self.logged_in_user)
            elif choice == '0': break

    # ==========================================
    # 5. 내 정보 메뉴 (서브메뉴)
    # ==========================================
    def show_my_info_menu(self):
        while True:
            print("\n[내 정보 메뉴] 1.비밀번호 변경 2.회원 탈퇴 0.돌아가기")
            choice = input("선택: ")
            if choice == '1':
                new_pw = input("새 비밀번호: ")
                self.member_service.change_password(self.logged_in_user, new_pw)
            elif choice == '2':
                confirm = input("정말 탈퇴하시겠습니까? (Y/N): ")
                if confirm.upper() == 'Y':
                    self.member_service.withdraw(self.logged_in_user)
                    self.logout()
                    break
            elif choice == '0': break

    # ==========================================
    # 6. 주문 결제 화면
    # ==========================================
    def show_payment_screen(self, items_info, total_price, is_from_cart):
        print(f"\n--- 💳 주문 결제 화면 ---")
        print(f"총 결제 금액: {total_price}원")
        addr = input("배송주소 및 연락처 입력: ")
        print("결제 정보 확인 중...")
        
        confirm = input("결제를 진행하시겠습니까? (Y/cancel): ")
        if confirm.upper() == 'Y':
            self.order_service.confirm_payment(self.logged_in_user, items_info, total_price, addr)
            if is_from_cart:
                self.cart_service.clear_cart(self.logged_in_user)
        else:
            print("[안내] 결제가 취소되었습니다.")

    def logout(self):
        self.logged_in_user = None
        self.is_admin_mode = False

if __name__ == "__main__":
    app = ConsoleApp()
    app.run()

    def logout(self):
        self.logged_in_user = None
        self.is_admin_mode = False
        print("로그아웃 되었습니다.")

if __name__ == "__main__":
    app = ConsoleApp()
    app.run()