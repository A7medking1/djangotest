from django.db import models

# Create your models here.


class Category(models.Model):

    title = models.CharField(max_length=30)
    image = models.ImageField(upload_to='media/category/')

    def __self__(self):
        return self.title
