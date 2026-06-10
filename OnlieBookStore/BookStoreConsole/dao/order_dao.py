class OrderDAO:
    def __init__(self):
        self.__db = []
        self.__order_sequence = 1 

    def generate_order_id(self):
        new_id = f"ORD-{self.__order_sequence}"
        self.__order_sequence += 1
        return new_id

    def insert_order(self, order):
        self.__db.append(order)
        return True

    def select_all_orders(self):
        return self.__db

    def select_orders_by_member(self, member_id):
        return [order for order in self.__db if order.get_member_id() == member_id]