# Generated by Django 4.0 on 2023-06-13 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_cart_razor_pay_order_id_cart_razor_pay_payment_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='paid_on',
            field=models.DateField(blank=True, null=True),
        ),
    ]