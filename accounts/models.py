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
    #data = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="media/product/")
    old_price = models.FloatField(default=0.0)
    new_price = models.FloatField(default=0.0)
    discount = models.BooleanField(default=False)
    description = models.TextField()

    def __str__(self):
        return self.title


class Favorite(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.Case)
    isFavorite = models.BooleanField(default=False)

    def __str__(self):
        return f"productID ={self.product.id}user={self.user.username}|ISFavorite={self.isFavorite}"



class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"productID => {self.product.id} user => {self.user.username} quantit =>{self.quantity}"