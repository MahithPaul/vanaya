from django.db import models
from base.models import BaseModel
from django.utils.text import slugify
# Create your models here.
class Product(BaseModel):
    product_name = models.CharField(max_length = 100)
    slug = models.SlugField(unique = True, null = True, blank = True)
    price = models.IntegerField(null = True, blank = True)
    beds = models.IntegerField(null = True, blank = True)
    adults = models.IntegerField(null = True, blank = True)
    children = models.IntegerField(null = True, blank = True)
    area = models.IntegerField(null = True, blank = True)
    product_description = models.TextField(null = True, blank = True)
    explore_description = models.TextField(null = True, blank = True)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.product_name

class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_images")
    image = models.ImageField(upload_to="product")

class TitleImage(BaseModel):
    title = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="title_images")
    image = models.ImageField(upload_to="product")

