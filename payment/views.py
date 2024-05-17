import stripe
import json
import os
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from orders.views import payment_confirmation
from django.views.generic.base import TemplateView
from django.conf import settings
# Create your views here.


def order_placed(request):
    cart = Cart(request)
    cart.clear()    # khi order xong thì xóa các item trong cart đi
    return render(request, 'payment/orderplaced.html')


class Error(TemplateView):
    template_name = 'payment/error.html'
    

@login_required
def CartView(request):
    cart = Cart(request)
    total = str(cart.get_total_price())
    total = total.replace('.', '')
    total = int(total)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    intent = stripe.PaymentIntent.create(    # tạo 1 paymentIntent để thu tiền
        amount=total,    # số tiền
        currency='gbp',   # mã tiền tệ, gbp là bảng Anh
        metadata={'userid': request.user.id}  # lấy id xem thằng nào là thằng pay(metadata là thông tin bổ sung vào)
    )
    return render(request, 'payment/payment_form.html', {'client_secret': intent.client_secret, 
                                                            'STRIPE_PUBLISHABLE_KEY': os.environ.get('STRIPE_PUBLISHABLE_KEY')})

# nhận và xử lí các sự kiện từ Stripe
@csrf_exempt   #  Bỏ qua kiểm tra CSRF (Cross-Site Request Forgery) cho hàm này vì webhook là một endpoint mà Stripe sẽ gửi yêu cầu POST đến từ bên ngoài.
def stripe_webhook(request):  # Định nghĩa hàm stripe_webhook nhận đối tượng request từ Django.
    payload = request.body  # Lấy nội dung của yêu cầu POST từ Stripe
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key   # Dùng Stripe SDK để xây dựng một đối tượng sự kiện từ JSON payload và khóa API của Stripe.
        )
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':   # khi thanh toán thành công
        print('gui di')
        payment_confirmation(event.data.object.client_secret)

    else:
        print('Unhandled event type {}'.format(event.type))   # in ra loại sự kiện không được xử lí

    return HttpResponse(status=200) 
