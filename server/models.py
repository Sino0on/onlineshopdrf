from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    email = models.EmailField(blank=False, unique=True)
    mailings = models.BooleanField(default=False, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=123, blank=True, null=True)

    def __str__(self):
        return f'{self.username}'


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
