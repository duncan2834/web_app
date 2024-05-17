from store.models import Product 
from decimal import Decimal
from django.conf import settings


class Cart():
    """
    A base Cart class, providing some default bahaviors that can be inherited or overrided, as necessary.
    """
    
    def __init__(self, request):   # ini object(default)
        
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if settings.CART_SESSION_ID not in request.session:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        
    def add(self, product, qty):
        """
        Adding and updating the users cart session data
        """
        product_id = product.id
        
        if product_id not in self.cart:
            self.cart[product_id] = {'price': str(product.regular_price), 'qty': int(qty)}
        
        self.save()
        
    def delete(self, product):
        # delete item out of session
        product_id= str(product)   #biến là product nhưng mà giá trị truyền vào từ views chỗ gọi hàm là productID
        if product_id in self.cart:
            del self.cart[product_id]   
            self.save() 
            
    def update(self, product, qty):
        product_id = str(product)
        if product_id in self.cart:
            self.cart[product_id]['qty'] = qty
            self.save()       
            
        
    def __iter__(self):
        # lấy product_id từ session data rồi dùng để query database và return products
        product_ids = self.cart.keys()   # key trong dict, là product_id trong cái dict cart phía trên
        products = Product.objects.filter(id__in=product_ids)   # Product.objecst truy cập vô cái trường của Product, filter là sắp xếp theo id mà xuất hiện trong các id sp trong cart
        cart = self.cart.copy()   # copy cái cart bây giờ 
        
        for product in products:
            cart[str(product.id)]['product'] = product   # tạo 1 key product cho cái copy cart đấy rồi value là data của sản phẩm
             
        for item in cart.values():    # values là value của key trong dict
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item
            
    def __len__(self):
        # lấy data cart và cộng tổng item trong cart
        return sum(item['qty'] for item in self.cart.values())
    
    def get_subtotal_price(self):
        return sum(Decimal(item["price"]) * item["qty"] for item in self.cart.values())
    
    def get_total_price(self):
        subtotal = sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())   # lấy tổng tiền 
        if subtotal == 0:
            shipping = Decimal(0.00)
        else:
            shipping = Decimal(11.50)

        total = subtotal + Decimal(shipping)
        return total
    
    def save(self):
        self.session.modified = True 
        
    def clear(self):  # xóa cái cart khỏi session đi
        del self.session[settings.CART_SESSION_ID]
        self.save()
            