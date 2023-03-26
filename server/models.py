from django.db import models


class Types(models.Model):
    title = models.CharField(max_length=123)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=123)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Color(models.Model):
    title = models.CharField(max_length=123)
    rgb = models.CharField(max_length=123)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Size(models.Model):
    title = models.CharField(max_length=123)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Productimages(models.Model):
    image = models.ImageField(upload_to='images/product/%Y/%m/%d')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='product_images')
    date = models.DateTimeField(auto_now_add=True)


class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='images/product/%Y/%m/%d')
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    types = models.ForeignKey(Types, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
