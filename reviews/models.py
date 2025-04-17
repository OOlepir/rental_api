# reviews/models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from properties.models import Property


class Review(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('property', 'user')


from django.db import models

# Create your models here.
