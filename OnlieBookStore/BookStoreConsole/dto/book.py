class Book:
    def __init__(self, book_id, title, price, stock):
        self.__book_id = book_id
        self.__title = title
        self.__price = price
        self.__stock = stock

    def get_book_id(self): return self.__book_id
    def get_title(self): return self.__title
    def get_price(self): return self.__price
    def get_stock(self): return self.__stock