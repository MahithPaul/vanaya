from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Profile)
class PaidCartModel(admin.ModelAdmin):
    '''list_display = ('user_first_name','user', 'is_paid', 'display_cart_items')
    readonly_fields = ('display_cart_items',)'''
    list_display = ('user_first_name', 'user', 'is_paid', 'display_cart_items')
    readonly_fields = ('display_cart_items',)
    search_fields = ['user__username', 'user_first_name','cart_items__dfrom']

    def display_cart_id(self, obj):
        return str(obj)

    display_cart_id.short_description = 'Cart'

    def display_cart_items(self, obj):
        cart_items = obj.cart_items.all().distinct()
        output = []
        for item in cart_items:
            item_data = f"Product: {item.product}\n\n Total Price: {item.total_price}\n\n Nights: {item.ncottage}\n\n From: {item.dfrom}\n\n To: {item.dto}\n\n Quantity: {item.nn}\n\n"
            output.append(item_data)
        return "\n".join(output)



    display_cart_items.short_description = 'Cart Items'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.fields = list(self.get_fields(request))
        self.readonly_fields = list(self.get_readonly_fields(request))
        self.readonly_fields.append('display_cart_items')
        return super().change_view(request, object_id, form_url, extra_context)

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        return fields

admin.site.register(Cart, PaidCartModel)
admin.site.register(CartItems)

'''class PaidCartModel(admin.ModelAdmin):
    list_display = ('user', 'is_paid', 'display_cart_items')  # Display the cart ID, is_paid, and the related cart_items

    def display_cart_id(self, obj):
        return obj.id

    def display_cart_items(self, obj):
        cart_items = obj.cart_items.all()
        return ", ".join([str(item) for item in cart_items])

    display_cart_items.short_description = 'Cart Items'
    display_cart_id.short_description = 'Cart ID'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.filter(is_paid=True)  # Filter the queryset to only include paid carts
        return queryset
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        # Retrieve the cart instance
        cart_instance = self.get_object(request, object_id)

        # Retrieve the related cart items
        cart_items = cart_instance.cart_items.all()

        # Pass the cart items to the template context
        extra_context = extra_context or {}
        extra_context['cart_items'] = cart_items

        return super().change_view(request, object_id, form_url=form_url, extra_context=extra_context)
'''

class CartAdmin(admin.ModelAdmin):
    list_filter = ['user_first_name', 'user', 'paid_on']  # Specify the attributes you want to search

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_search_button'] = True
        return super().change_view(request, object_id, form_url, extra_context=extra_context)