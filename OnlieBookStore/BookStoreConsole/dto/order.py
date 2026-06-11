class Order:
    def __init__(self, order_id, member_id, items_info, total_price, address):
        self.__order_id = order_id  
        self.__member_id = member_id
        self.__items_info = items_info
        self.__total_price = total_price
        self.__address = address
        self.__status = "결제완료"

    # --- 기존 Getter 메서드 ---
    def get_order_id(self): return self.__order_id
    def get_member_id(self): return self.__member_id
    def get_total_price(self): return self.__total_price
    def get_items_info(self): return self.__items_info

    # --- 새롭게 정의한 Getter 메서드 ---
    def get_address(self): 
        return self.__address
        
    def get_status(self): 
        return self.__status

    # --- 값을 수정하기 위한 Setter 메서드 (선택 사항) ---
    def update_address(self, new_address):
        """배송지나 주소가 변경될 때 사용합니다."""
        self.__address = new_address

    def update_status(self, new_status):
        """주문 상태(예: 배송중, 구매확정 등)가 변경될 때 사용합니다."""
        self.__status = new_status
