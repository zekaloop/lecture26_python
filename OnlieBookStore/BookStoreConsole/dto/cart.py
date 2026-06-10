class CartItem:
    def __init__(self, book_id, quantity):
        self.__book_id = book_id
        self.__quantity = quantity

    def get_book_id(self): return self.__book_id
    def get_quantity(self): return self.__quantity