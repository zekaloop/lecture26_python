class BookService:
    def __init__(self, book_dao): self.__book_dao = book_dao

    def show_all_books(self):
        books = self.__book_dao.select_all_books()
        print("\n--- 📚 도서 목록 ---")
        for b_id, info in books.items():
            print(f"[{b_id}] {info['title']} | {info['price']}원 | 재고: {info['stock']}권")

    def register_new_book(self, book_id, title, price, stock):
        if self.__book_dao.insert_book(book_id, title, price, stock):
            print("[성공] 도서가 등록되었습니다.")

    def update_book_info(self, book_id, title, price, stock):
        if self.__book_dao.update_book(book_id, title, price, stock):
            print("[성공] 도서 정보가 수정되었습니다.")
        else: print("[실패] 도서를 찾을 수 없습니다.")

    def delete_book(self, book_id):
        if self.__book_dao.delete_book(book_id): print("[성공] 도서가 삭제되었습니다.")
        else: print("[실패] 도서를 찾을 수 없습니다.")