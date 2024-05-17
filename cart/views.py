from django.shortcuts import render, get_object_or_404
from store.models import Product
from .cart import Cart
from django.http import JsonResponse

# Create your views here.

def cart_summary(request):
    cart = Cart(request)     # ini object => cart.py
    return render(request, 'cart/summary.html', {'cart': cart})

def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id= product_id)
        cart.add(product= product, qty= product_qty)
        cartqty = cart.__len__()
        response = JsonResponse({'qty': cartqty})   # lúc đầu để là 'qty': product_qty nên chỉ trả về qty của 1 product
        return response

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        cart.delete(product= product_id)
        cartqty = cart.__len__()  # tổng số item trong cart(sau khi delete do có lệnh delete phía trên rồi)
        carttotal = cart.get_total_price() # tổng tiền(sau khi delete)
        response = JsonResponse({'qty': cartqty, 'subtotal': carttotal})
        return response      # phải có return response ko là n ko cập nhật gì hết

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        cart.update(product= product_id, qty= product_qty)
        cartqty = cart.__len__()  # tổng số item trong cart(sau khi delete do có lệnh delete phía trên rồi)
        carttotal = cart.get_total_price() # tổng tiền(sau khi delete)
        response = JsonResponse({'qty': cartqty, 'subtotal': carttotal})
        return response      # phải có return response ko là n ko cập nhật gì hết