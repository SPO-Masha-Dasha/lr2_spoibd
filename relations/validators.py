# relations/validators.py
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
import re


# 1. ВАЛИДАТОР-ФУНКЦИЯ
def validate_no_special_chars(value):
    """
    Проверяет, что строка не содержит специальных символов (@#$%^&*).
    """
    if re.search(r'[@#$%^&*]', value):
        raise ValidationError(
            'Название не должно содержать специальные символы (@#$%^&*)',
            code='special_chars'
        )


# 2. ВАЛИДАТОР-КЛАСС (ИСПРАВЛЕННЫЙ - с декоратором @deconstructible)
@deconstructible
class PriceRangeValidator:
    """
    Проверяет, что цена находится в заданном диапазоне.
    Декоратор @deconstructible делает класс сериализуемым для миграций.
    """
    def __init__(self, min_price=0, max_price=1000000):
        self.min_price = min_price
        self.max_price = max_price
    
    def __call__(self, value):
        if value < self.min_price:
            raise ValidationError(
                f'Цена не может быть меньше {self.min_price}',
                code='price_too_low'
            )
        if value > self.max_price:
            raise ValidationError(
                f'Цена не может превышать {self.max_price}',
                code='price_too_high'
            )
    
    def __eq__(self, other):
        # Нужно для корректной работы миграций
        return (
            isinstance(other, PriceRangeValidator) and
            self.min_price == other.min_price and
            self.max_price == other.max_price
        )


# 3. ВАЛИДАТОР-ФУНКЦИЯ для телефона
def validate_phone_format(value):
    """
    Проверяет формат телефона: +7XXXXXXXXXX или 8XXXXXXXXXX
    """
    if value:  # Проверяем только если значение не пустое
        pattern = r'^(\+7|8)\d{10}$'
        if not re.match(pattern, value):
            raise ValidationError(
                'Телефон должен быть в формате: +7XXXXXXXXXX или 8XXXXXXXXXX',
                code='invalid_phone'
            )