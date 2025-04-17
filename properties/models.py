# properties/models.py

from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User
from django.core.validators import MinValueValidator


class PropertyType(models.Model):
    """Типи нерухомості"""
    name = models.CharField(_('название'), max_length=50)

    class Meta:
        verbose_name = _('тип жилья')
        verbose_name_plural = _('типы жилья')

    def __str__(self):
        return self.name


class Location(models.Model):
    """Місцезнаходження нерухомості"""
    city = models.CharField(_('город'), max_length=100)
    district = models.CharField(_('район'), max_length=100, blank=True, null=True)
    address = models.CharField(_('адрес'), max_length=255, blank=True, null=True)
    postal_code = models.CharField(_('почтовый индекс'), max_length=10, blank=True, null=True)
    latitude = models.FloatField(_('широта'), blank=True, null=True)
    longitude = models.FloatField(_('долгота'), blank=True, null=True)

    class Meta:
        verbose_name = _('местоположение')
        verbose_name_plural = _('местоположения')

    def __str__(self):
        if self.district:
            return f"{self.city}, {self.district}"
        return self.city


class Property(models.Model):
    """Модель нерухомості (оголошення)"""
    STATUS_CHOICES = (
        ('active', _('Активно')),
        ('inactive', _('Неактивно')),
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties', verbose_name=_('владелец'))
    title = models.CharField(_('заголовок'), max_length=200)
    description = models.TextField(_('описание'))
    property_type = models.ForeignKey(PropertyType, on_delete=models.PROTECT, related_name='properties',
                                      verbose_name=_('тип жилья'))
    location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='properties',
                                 verbose_name=_('местоположение'))
    price = models.DecimalField(_('цена'), max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    rooms = models.PositiveSmallIntegerField(_('количество комнат'), validators=[MinValueValidator(1)])
    area = models.FloatField(_('площадь (кв.м.)'), validators=[MinValueValidator(1)])
    status = models.CharField(_('статус'), max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(_('дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('дата обновления'), auto_now=True)
    views_count = models.PositiveIntegerField(_('количество просмотров'), default=0)

    class Meta:
        verbose_name = _('объявление')
        verbose_name_plural = _('объявления')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.location.city} ({self.property_type})"


class PropertyImage(models.Model):
    """Зображення нерухомості"""
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images',
                                 verbose_name=_('объявление'))
    image = models.ImageField(_('изображение'), upload_to='property_images/')
    is_main = models.BooleanField(_('главное изображение'), default=False)
    created_at = models.DateTimeField(_('дата добавления'), auto_now_add=True)

    class Meta:
        verbose_name = _('изображение объявления')
        verbose_name_plural = _('изображения объявлений')

    def __str__(self):
        return f"Изображение для {self.property.title}"


from django.db import models

# Create your models here.
