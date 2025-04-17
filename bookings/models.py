# bookings/models.py

from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User
from properties.models import Property
from django.core.exceptions import ValidationError
from django.utils import timezone


class Booking(models.Model):
    """Модель бронювання нерухомості"""
    STATUS_CHOICES = (
        ('pending', _('Ожидает подтверждения')),
        ('confirmed', _('Подтверждено')),
        ('rejected', _('Отклонено')),
        ('canceled', _('Отменено')),
        ('completed', _('Завершено')),
    )

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='bookings',
                                 verbose_name=_('объявление'))
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings', verbose_name=_('арендатор'))
    check_in_date = models.DateField(_('дата заезда'))
    check_out_date = models.DateField(_('дата выезда'))
    guests_count = models.PositiveSmallIntegerField(_('количество гостей'), default=1)
    status = models.CharField(_('статус'), max_length=15, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(_('общая стоимость'), max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(_('дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('дата обновления'), auto_now=True)
    notes = models.TextField(_('примечания'), blank=True, null=True)

    class Meta:
        verbose_name = _('бронирование')
        verbose_name_plural = _('бронирования')
        ordering = ['-created_at']

    def __str__(self):
        return f"Бронирование {self.property.title} с {self.check_in_date} по {self.check_out_date}"

    def clean(self):
        # Перевірка, що дата виїзду пізніше за дату заїзду
        if self.check_out_date and self.check_in_date and self.check_out_date <= self.check_in_date:
            raise ValidationError({'check_out_date': _('Дата выезда должна быть позже даты заезда')})

        # Перевірка, що дата заїзду не в минулому
        if self.check_in_date and self.check_in_date < timezone.now().date():
            raise ValidationError({'check_in_date': _('Дата заезда не может быть в прошлом')})

        # Перевірка на перетин з іншими бронюваннями
        overlapping_bookings = Booking.objects.filter(
            property=self.property,
            status__in=['pending', 'confirmed'],
            check_in_date__lt=self.check_out_date,
            check_out_date__gt=self.check_in_date
        )

        # Виключаємо поточне бронювання при перевірці (для оновлення існуючого)
        if self.pk:
            overlapping_bookings = overlapping_bookings.exclude(pk=self.pk)

        if overlapping_bookings.exists():
            raise ValidationError(_('Выбранные даты уже забронированы'))

    def save(self, *args, **kwargs):
        # Виклик валідаторів перед збереженням
        self.clean()
        self.calculate_total_price()
        super().save(*args, **kwargs)

    def calculate_total_price(self):
        count = (self.check_out_date - self.check_in_date).days
        self.total_price = count * self.property.price


class BookingCancellationPolicy(models.Model):
    """Політика скасування бронювання"""
    name = models.CharField(_('название'), max_length=100)
    days_before_checkin = models.PositiveIntegerField(_('дней до заезда'), help_text=_(
        'За сколько дней до заезда можно отменить бронирование без штрафа'))
    cancellation_fee_percentage = models.PositiveIntegerField(_('процент штрафа'), help_text=_(
        'Процент от общей стоимости, который взимается при отмене бронирования позже указанного срока'))

    class Meta:
        verbose_name = _('политика отмены')
        verbose_name_plural = _('политики отмены')

    def __str__(self):
        return self.name


from django.db import models

# Create your models here.
