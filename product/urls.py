from django.urls import path
from product.views import get_product,explore_product

urlpatterns = [
    path('<slug>/', get_product, name = "get_product"),
    path('explore/<slug>/', explore_product, name = "explore_product"),
    #path('add-to-cart/<slug>', add_to_cart, name = "add_to_cart")
]
