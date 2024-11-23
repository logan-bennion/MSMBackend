from django.core.exceptions import ValidationError
from django.db import models

class ShopHours(models.Model):
    def clean(self):
        if self.closing_time <= self.opening_time:
            raise ValidationError("Closing time must be after opening time")
        
        # Check for overlapping hours on the same day
        overlapping = ShopHours.objects.filter(
            shop=self.shop,
            day=self.day,
            opening_time__lt=self.closing_time,
            closing_time__gt=self.opening_time
        ).exclude(pk=self.pk)
        
        if overlapping.exists():
            raise ValidationError("Operating hours overlap with existing hours")
