from django.db import models
from menu_item.models import MenuItem
from django.contrib.auth.models import User
from decimal import Decimal


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('user', 'menu_item')

    def __str__(self):
        return f"Cart of {self.user.username}"

