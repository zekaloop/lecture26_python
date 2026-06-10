class BookDAO:
    def __init__(self):
        self.__db = {
            "B001": {"title": "파이썬 자료구조", "price": 25000, "stock": 10},
            "B002": {"title": "인공지능의 이해", "price": 30000, "stock": 5}
        }

    def insert_book(self, book_id, title, price, stock):
        self.__db[book_id] = {"title": title, "price": price, "stock": stock}
        return True

    def select_all_books(self): return self.__db
    def select_book(self, book_id): return self.__db.get(book_id, None)

    def update_book(self, book_id, title, price, stock):
        if book_id in self.__db:
            self.__db[book_id] = {"title": title, "price": price, "stock": stock}
            return True
        return False

    def delete_book(self, book_id):
        if book_id in self.__db:
            del self.__db[book_id]
            return True
        return False

    def update_stock(self, book_id, new_stock):
        if book_id in self.__db:
            self.__db[book_id]["stock"] = new_stock
            return True
        return False