from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to='images/product/%Y/%m/%d')
    size = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    types = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id']
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
