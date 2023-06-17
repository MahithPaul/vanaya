from django.shortcuts import render
from product.models import Product
# Create your views here.
def get_service(request):
    context = {'products' : Product.objects.all()}
    return render(request,'service/service.html', context)