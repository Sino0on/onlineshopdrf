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


class Order(models.Model):
    is_delivery = models.BooleanField()
    email = models.EmailField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    phone_number = models.IntegerField()
    full_name = models.CharField(blank=True, null=True, max_length=223)
    pay_with_card = models.BooleanField()
    gift = models.BooleanField(default=False)
    goods = models.ManyToManyField('OrderProduct')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order - {self.id}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_date']


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'PreOrder {self.product}'


