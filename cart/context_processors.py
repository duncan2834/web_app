from .cart import Cart

def cart(request):
    return {'cart': Cart(request)}  # dựa trên request thì trả về đối tượng tương ứng với data.(tạo đối tượng từ cái cart.py)