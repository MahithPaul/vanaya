from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from .models import Profile
from product.models import *
from accounts.models import Cart, CartItems
from django.http import HttpResponseRedirect
from accounts.methods import *
from django.db.models import Sum
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from datetime import date

import razorpay 

#51:23
# Create your views here.
def login_page(request):
    if request.method=='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email)

        if not user_obj.exists():
            messages.warning(request,'Account Not Found')
            return HttpResponseRedirect(request.path_info)
        
        if not user_obj[0].profile.is_email_verified:
            messages.warning(request,'Your account is not verified!')
            return HttpResponseRedirect(request.path_info)

        user_obj = authenticate(username = email, password = password)
        if user_obj:
            login(request,user_obj)
            return redirect('index')

        messages.success(request, 'Invalid credentials')
        return HttpResponseRedirect(request.path_info)
    return render(request,'accounts/logIn.html')

def register_page(request):
    if request.method=='POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('confirmPass')
        if password!= cpassword:
            messages.warning(request,'Passwords do not match')
            return HttpResponseRedirect(request.path_info)
        user_obj = User.objects.filter(username = email)
        if user_obj.exists():
            messages.warning(request,'Email is already taken')
            return HttpResponseRedirect(request.path_info)
        user_obj = User.objects.create(first_name=first_name,last_name=last_name,email=email, username = email)
        user_obj.set_password(password)
        user_obj.save()
        messages.success(request, 'An Account Activation Email Has Been Sent To Your Email')
        return HttpResponseRedirect(request.path_info)
    return render(request,'accounts/signUp.html')

def activate_email(request,email_token):
    try:
        user = Profile.objects.get(email_token=email_token)
        user.is_email_verified=True
        user.save()
        print(user)
        return redirect('success')
    except Exception as e:
        return HttpResponse('Invalid Email Token')

def success(request):
    return render(request,'accounts/verify.html')

from django.conf import settings
def cart(request):
    try:
        cpage = Cart.objects.get(is_paid = False, user = request.user )
        citems = CartItems.objects.filter(cart=cpage)
        total_price_sum = citems.aggregate(total_price_sum=Sum('total_price')).get('total_price_sum')
        client = razorpay.Client(auth = (settings.KEY, settings.SECRET))
        payment = client.order.create({'amount':total_price_sum*100, 'currency':'INR', 'payment_capture':1})
        cpage.razor_pay_order_id=payment['id']
        cpage.save()
        print('*****')
        print(payment)
        print('*****')
        context = {'cart': cpage , 'items':citems, 'full_price':total_price_sum, 'payment':payment}
        return render(request, 'accounts/cart.html', context)

            
    except Exception as e:
        print(e)
        return render(request, 'accounts/empty.html')


def add_to_cart(request,uid):
    if request.method == 'POST':
        try:
            product = Product.objects.get(uid = uid)
            quant = request.POST.get('quant')
            dfrom = request.POST.get('dfrom')
            dto = request.POST.get('dto')
            nn = calculate_nights(dfrom, dto)
            updated_price = product.price * nn * int(quant)
            user = request.user
            cart, _ = Cart.objects.get_or_create(user = user, is_paid = False, user_first_name = user.first_name)
            cartitems = CartItems.objects.create(cart = cart, product = product, total_price = updated_price, ncottage = int(quant), dfrom = dconvert(dfrom), dto = dconvert(dto), nn = nn)
            cartitems.save()
            messages.warning(request,'Added to Checkout List')
            return HttpResponseRedirect(request.path_info)
        except Exception as e:
            print(e)
            messages.warning(request,'Please Sign In')
            return HttpResponseRedirect(request.path_info)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_cart(request, cart_item_uid):
    try:
        cart_item = CartItems.objects.get(uid=cart_item_uid)
        cart_item.delete()
        print("deleted")
    except Exception as e:
        print(e)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    

def pay_success(request):
    # Get the authenticated user's email
    email = request.user.email

    # Retrieve the paid cart and calculate the sum of total_price
    order_id = request.GET.get('order_id')
    cart = Cart.objects.get(razor_pay_order_id=order_id)
    cart.is_paid = True
    cart.paid_on = date.today()
    cart.save()

    total_price_sum = cart.cart_items.aggregate(total_price_sum=Sum('total_price'))['total_price_sum']

    # Prepare the email content
    subject = 'Payment Confirmation'
    context = {
        'cart': cart,
        'total_price_sum': total_price_sum,
        'cart_items': cart.cart_items.all()

    }
    html_message = render_to_string('email/payment_confirmation.html', context)
    plain_message = strip_tags(html_message)

    # Send the email
    send_mail(subject, plain_message, 'sender@example.com', [email], html_message=html_message)

    return render(request, 'accounts/payment.html')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
                # Generate unique token for password reset
            token = PasswordResetTokenGenerator().make_token(user)

                # Build the password reset activation link
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = f"{request.scheme}://{request.get_host()}/accounts/reset-password/{uid}/{token}/"

                # Send the password reset email
            subject = 'Password Reset'
            message = render_to_string('email/reset.html', {'reset_url': reset_url})
            plain_message = strip_tags(message)
            send_mail(subject, plain_message, 'sender@example.com', [email], html_message=message)

            # Show a success message
        messages.success(request, 'Please check your email for password reset instructions.')
        return redirect('login')
    else:
        return render(request, 'accounts/forgot.html')

    return render(request, 'accounts/forgot.html')

def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and PasswordResetTokenGenerator().check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST['new_password']
            print(new_password)
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Your password has been reset successfully. You can now log in with your new password.')
            return redirect('login')
    else:
        messages.error(request, 'Invalid password reset link.')

    return render(request, 'accounts/password.html')

def user_carts(request):
    # Get the currently logged-in user
    user = request.user

    # Retrieve carts and calculate the sum of total_price for each cart
    carts = Cart.objects.filter(user=user)
    carts_with_sum = carts.annotate(total_price_sum=Sum('cart_items__total_price'))
    print(carts_with_sum)
    # Pass the carts with the sum to the template
    context = {'carts': carts_with_sum}
    return render(request, 'accounts/user_carts.html', context)