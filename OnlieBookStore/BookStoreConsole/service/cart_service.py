from dto.cart import CartItem

class CartService:
    def __init__(self, cart_dao, book_dao):
        self.__cart_dao = cart_dao
        self.__book_dao = book_dao

    def add_book_to_cart(self, member_id, book_id, quantity):
        book = self.__book_dao.select_book(book_id)
        if not book or book["stock"] < quantity:
            print("[실패] 도서가 없거나 재고가 부족합니다.")
            return False
        self.__cart_dao.add_to_cart(member_id, CartItem(book_id, quantity))
        print(f"[성공] 장바구니에 담았습니다.")
        return True

    def remove_book(self, member_id, book_id):
        self.__cart_dao.remove_item(member_id, book_id)
        print("[성공] 장바구니에서 삭제되었습니다.")

    def clear_cart(self, member_id):
        self.__cart_dao.clear_cart(member_id)
        print("[성공] 장바구니를 비웠습니다.")

    def view_cart_and_get_total(self, member_id):
        items = self.__cart_dao.get_cart_items(member_id)
        if not items:
            print("\n장바구니가 비어있습니다.")
            return 0
        print(f"\n--- 🛒 장바구니 ---")
        total = 0
        for item in items:
            book = self.__book_dao.select_book(item.get_book_id())
            subtotal = book['price'] * item.get_quantity()
            total += subtotal
            print(f"[{item.get_book_id()}] {book['title']} | {item.get_quantity()}권 | {subtotal}원")
        print(f"총 결제 금액: {total}원")
        return total