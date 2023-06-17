from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from base.emails import send_account_activation_email
from product.models import Product
from django.contrib.humanize.templatetags.humanize import naturalday


# Create your models here.
class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = "profile")
    is_email_verified = models.BooleanField(default = False)
    email_token = models.CharField(max_length = 100, null = True, blank = True)


class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'carts')
    is_paid = models.BooleanField(default=False)
    user_first_name = models.CharField(max_length=255, blank=True, null=True)
    razor_pay_order_id = models.CharField(max_length=100, null=True, blank=True)
    razor_pay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razor_pay_payment_signature = models.CharField(max_length=100, null=True, blank=True)
    paid_on = models.DateField(null= True,blank = True)



class CartItems(BaseModel):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null= True,blank = True)
    total_price = models.IntegerField(null= True,blank = True)
    ncottage = models.IntegerField(null= True,blank = True)
    dfrom = models.DateField(null= True,blank = True)
    dto = models.DateField(null= True,blank = True)
    nn = models.IntegerField(null= True,blank = True)
    

    
@receiver(post_save, sender = User )
def send_email_token(sender, instance,created,**kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())
            Profile.objects.create(user = instance,email_token = email_token)
            email = instance.email
            send_account_activation_email(email,email_token)
    except Exception as e:
        print(e)
