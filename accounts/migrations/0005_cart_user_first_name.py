# Generated by Django 4.0 on 2023-06-11 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_remove_cart_user_first_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='user_first_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
