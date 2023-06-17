from django.urls import path
from django.contrib.auth import views as auth_views
from accounts.views import login_page,register_page,activate_email, success, cart, add_to_cart, remove_cart, pay_success, forgot_password, reset_password, user_carts
#from product.views import  add_to_cart

urlpatterns = [
    path('login', login_page, name = "login"),
    path('register', register_page, name = "register"),
    path('activate/<str:email_token>/',activate_email, name="activate_email"),
    path('success', success, name = "success"),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('cart/', cart, name = "cart"),
    path('add-to-cart/<uid>/', add_to_cart, name="add_to_cart"),
    path('remove_cart/<cart_item_uid>/', remove_cart , name = "remove_cart"),
    path('pay-successful/', pay_success, name = 'pay_success'),
    path('forgot-password/',forgot_password, name = "forgot_password"),
    path('reset-password/<str:uidb64>/<str:token>/', reset_password, name='reset_password'),
    path('previous-bookings/',user_carts, name = 'user_carts' ),
]