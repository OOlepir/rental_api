# users/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _


class User(AbstractUser, PermissionsMixin):
    """
    Розширена модель користувача для системи оренди житла
    """
    USER_TYPE_CHOICES = (
        ('landlord', _('Арендодатель')),
        ('tenant', _('Арендатор')),
    )

    email = models.EmailField(_('email address'), unique=True)
    user_type = models.CharField(_('тип пользователя'), max_length=10, choices=USER_TYPE_CHOICES, default='tenant')
    phone_number = models.CharField(_('номер телефона'), max_length=20, blank=True, null=True)
    profile_image = models.ImageField(_('изображение профиля'), upload_to='profile_images/', blank=True, null=True)

    # Використовуємо email як ідентифікатор для входу
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name']

    class Meta:
        verbose_name = _('пользователь')
        verbose_name_plural = _('пользователи')

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"