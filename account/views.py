from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib import messages
from orders.views import user_orders
from store.models import Product
from .forms import RegistrationForm, UserEditForm, UserAddressForm
from .models import Customer, Address
from .tokens import account_activation_token


@login_required
def wishlist(request):
    products = Product.objects.filter(users_wishlist=request.user)
    return render(request, "account/dashboard/user_wish_list.html", {"wishlist": products})


@login_required
def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    if product.users_wishlist.filter(id=request.user.id).exists():   # có sp đấy thì remove
        product.users_wishlist.remove(request.user)
        messages.success(request, product.title + " has been removed from your WishList")
    else:
        product.users_wishlist.add(request.user)  # ko có thì add
        messages.success(request, "Added " + product.title + " to your WishList")
    return HttpResponseRedirect(request.META["HTTP_REFERER"])

@login_required
def dashboard(request):    # hiện dashboard lên
    orders = user_orders(request)
    return render(request,
                  'account/dashboard/dashboard.html',
                  {'section': 'profile', 'orders': orders})


@login_required
def edit_details(request):
    if request.method == 'POST':    # có form để người dùng update POST sẽ thay đổi trong DB
        user_form = UserEditForm(instance=request.user, data=request.POST)    # UserEditForm được định nghĩa ở forms.py

        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request,
                  'account/dashboard/edit_details.html', {'user_form': user_form})   # render ra edit_details.html với data là user_form


@login_required
def delete_user(request):    # xóa tài khoản
    user = Customer.objects.get(user_name=request.user)   # khởi tạo đối tượng user với đk là user_name = request.user
    user.is_active = False   # set not active 
    user.save()
    logout(request)
    return redirect('account:delete_confirmation')   # confirm delete


def account_register(request):

    if request.user.is_authenticated:   # login rồi thì đưa về dashboard
        return redirect('account:dashboard')

    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('account/registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),  # bảo mật an toàn, mã hóa id người dùng
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return render(request, 'account/registration/register_email_confirm.html', {'form': registerForm})
    else:
        registerForm = RegistrationForm()
    return render(request, 'account/registration/register.html', {'form': registerForm})


def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request, 'account/registration/activation_invalid.html')
    
def logout_user(request):
    logout(request)
    return redirect('account:login')

# Addresses

@login_required
def view_address(request):
    addresses = Address.objects.filter(customer=request.user)
    return render(request, "account/dashboard/addresses.html", {"addresses": addresses})


@login_required
def add_address(request):
    if request.method == "POST":
        address_form = UserAddressForm(data=request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.customer = request.user
            address_form.save()
            return HttpResponseRedirect(reverse("account:addresses"))
    else:
        address_form = UserAddressForm()
    return render(request, "account/dashboard/edit_addresses.html", {"form": address_form})

@login_required
def edit_address(request, id):
    if request.method == "POST":
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            return HttpResponseRedirect(reverse("account:addresses"))
    else:
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address)
    return render(request, "account/dashboard/edit_addresses.html", {"form": address_form})

@login_required
def delete_address(request, id):
    address = Address.objects.filter(pk=id, customer=request.user).delete()
    return redirect("account:addresses")

@login_required
def set_default(request, id):   # đặt địa chỉ làm địa chỉ mặc định và tất cả địa chỉ khác ko còn là mặc định nữa
    Address.objects.filter(customer=request.user, default=True).update(default=False)
    Address.objects.filter(pk=id, customer=request.user).update(default=True)
    return redirect("account:addresses") 