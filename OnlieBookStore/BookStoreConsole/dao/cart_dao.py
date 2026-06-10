class CartDAO:
    def __init__(self):
        self.__db = {}

    def add_to_cart(self, member_id, cart_item):
        if member_id not in self.__db: self.__db[member_id] = []
        self.__db[member_id].append(cart_item)

    def get_cart_items(self, member_id):
        return self.__db.get(member_id, [])

    def remove_item(self, member_id, book_id):
        if member_id in self.__db:
            self.__db[member_id] = [item for item in self.__db[member_id] if item.get_book_id() != book_id]

    def clear_cart(self, member_id):
        self.__db[member_id] = []