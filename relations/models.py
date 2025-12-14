from django.db import models
from django.conf import settings
from .validators import validate_no_special_chars, PriceRangeValidator, validate_phone_format
from django.db import models
from django.conf import settings

# 1. Модель Category (для связи один-ко-многим)
class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название категории', validators=[validate_no_special_chars])
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


# 2. Модель Tag (для связи многие-ко-многим)
class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name='Тег')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


# 3. Модель Product (с ДВУМЯ связями: ForeignKey и ManyToManyField)
class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название товара')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена', validators=[PriceRangeValidator(min_price=10, max_price=100000)])
    
    # Связь ОДИН-КО-МНОГИМ с Category
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория',
        related_name='products'
    )
    
    # Связь МНОГИЕ-КО-МНОГИМ с Tag
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='Теги')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


# 4. Модель UserProfile (для связи один-к-одному)
class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='profile'
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон', validators=[validate_phone_format])
    address = models.TextField(blank=True, verbose_name='Адрес')
    
    def __str__(self):
        return f'Профиль {self.user.username}'
    
    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

