from django.db import models
# Для кастомеров
from django.contrib.auth import get_user_model
# Для Спецификаций товаров (см CartProduct)
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


User = get_user_model()


#     PLAN:
#******************
# 1. Category
# 2. Product
# 3. CartProduct
# 4. Cart
# 5. Order
#******************
# 6. Customer
# 7. Specification
#******************


class Category(models.Model):

    name = models.CharField(max_length = 255, verbose_name = 'Имя категории')
    slug = models.SlugField(unique = True)

    def __str__(self):
        return self.name


class Product(models.Model):

    class Meta:
        abstract = True

    category = models.ForeignKey(Category, verbose_name = 'Категория', on_delete = models.CASCADE)
    title = models.CharField(max_length = 255, verbose_name = 'Наименование')
    slug = models.SlugField(unique = True)
    image = models.ImageField(verbose_name = 'Изображение')
    description = models.TextField(verbose_name = 'Описание', null = True)
    price = models.DecimalField(max_digits = 9, decimal_places = 2, verbose_name = 'Цена')

    def __str__(self):
        return self.title


class CartProduct(models.Model):

    user = models.ForeignKey('Customer', verbose_name = 'Покупатель', on_delete = models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name = 'Корзина', on_delete = models.CASCADE, related_name = 'related_products')
    #***********************************************************************************************
    # product = NotebookProduct.objects.get(pk = 1)
    # cart_product = CartProduct.objects.create(content_object = product)
    # Сам продукт (NotebookProduct) заносится в content_type, а его pk в object_id
    content_type = models.ForeignKey(ContentType, on_delete = models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    #***********************************************************************************************
    qty = models.PositiveIntegerField(default = 1)
    final_price = models.DecimalField(max_digits = 9, decimal_places = 2, verbose_name = 'Общая цена')

    def __str__(self):
        return 'Продукт: {} (для корзины)'.format(self.product.title)


class Cart(models.Model):

    owner = models.ForeignKey('Customer', verbose_name = 'Владелец корзины', on_delete = models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank = True, related_name = 'related_cart')
    total_products = models.PositiveIntegerField(default = 0)
    final_price = models.DecimalField(max_digits = 9, decimal_places = 2, verbose_name = 'Общая цена')

    def __str__(self):
        return str(self.id)


class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name = 'Пользователь', on_delete = models.CASCADE)
    phone = models.CharField(max_length = 20, verbose_name = 'Номер телефона')
    address = models.CharField(max_length = 255, verbose_name = 'Адрес')

    def __str__(self):
        return 'Пользователь: {} {}'.format(self.user.first_name, self.user.last_name)
