from django.db import models
from django.core.exceptions import ValidationError

class Deal(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    deal_price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
    def clean(self):
        if self.deal_price >= self.original_price:
            raise ValidationError("Deal price must be less than original price")
        if self.end_date <= self.start_date:
            raise ValidationError("End date must be after start date")
