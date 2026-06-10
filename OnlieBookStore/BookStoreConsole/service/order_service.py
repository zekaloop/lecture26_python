from dto.order import Order

class OrderService:
    def __init__(self, order_dao, book_dao, cart_dao):
        self.__order_dao = order_dao
        self.__book_dao = book_dao
        self.__cart_dao = cart_dao

    def confirm_payment(self, member_id, items_info, total_price, address):
        for info in items_info:
            book_id, qty = info["book_id"], info["qty"]
            current_stock = self.__book_dao.select_book(book_id)["stock"]
            self.__book_dao.update_stock(book_id, current_stock - qty)

        new_order = Order(self.__order_dao.generate_order_id(), member_id, items_info, total_price, address)
        self.__order_dao.insert_order(new_order)
        print(f"\n[성공] 결제 완료! (주문번호: {new_order.get_order_id()})")

    def show_my_orders(self, member_id):
        orders = self.__order_dao.select_orders_by_member(member_id)
        print("\n--- 📦 내 주문 목록 ---")
        for o in orders: print(f"주문번호: {o.get_order_id()} | 결제금액: {o.get_total_price()}원")

    def show_all_orders(self):
        orders = self.__order_dao.select_all_orders()
        print("\n--- 📦 전체 주문 목록 (관리자용) ---")
        for o in orders: print(f"주문번호: {o.get_order_id()} | 주문자: {o.get_member_id()} | 결제금액: {o.get_total_price()}원")