class Order:
    def __init__(self, order_id, member_id, items_info, total_price, address):
        self.__order_id = order_id  
        self.__member_id = member_id
        self.__items_info = items_info
        self.__total_price = total_price
        self.__address = address
        self.__status = "결제완료"

    def get_order_id(self): return self.__order_id
    def get_member_id(self): return self.__member_id
    def get_total_price(self): return self.__total_price
    def get_items_info(self): return self.__items_info