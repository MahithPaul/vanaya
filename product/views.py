from django.shortcuts import render, HttpResponse, redirect
from product.models import Product


# Create your views here.
def get_product(request, slug):
    try:
        product = Product.objects.get(slug = slug)
        return render(request,'product/booking.html', context = {'product':product})
    except Exception as e:
        print(e)
        return HttpResponse("An error occurred")

def explore_product(request,slug):
    try:
        product = Product.objects.get(slug = slug)
        return render(request, 'product/explore.html',context = {'product':product})
    except Exception as e:
        print(e)
        return HttpResponse("An error occurred")




