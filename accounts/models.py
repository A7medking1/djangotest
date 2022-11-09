from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):

    title = models.CharField(max_length=30)
    image = models.ImageField(upload_to='media/category/')
    def __self__(self):
        return self.title



class Product(models.Model):
    title = models.CharField(max_length=100)
    data = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="media/product/")
    marcket_price = models.PositiveIntegerField()
    selling_price = models.PositiveIntegerField()
    description = models.TextField()

    def __str__(self):
        return self.title


class Favorite(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.Case)
    isFavorit = models.BooleanField(default=False)

    def __str__(self):
        return f"productID ={self.product.id}user={self.user.username}|ISFavorite={self.isFavorit}"
