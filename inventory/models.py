from django.core.validators import MinValueValidator
from django.db import models

from decimal import Decimal

# Create your models here.
class Catagory(models.Model):
    
    class Meta:
        ordering = ['title']

    title = models.CharField(primary_key=True,unique=True,max_length=50)

    def __str__(self):
        return self.title

class InventoryItem(models.Model):
    
    class Meta:
        ordering = ['item_name']
    
    CHOICES = (
        ('ltr', 'Liters'),
        ('kg', 'Kilograms'),
        ('pcs', 'Pieces'),
    )

    item_name = models.CharField(primary_key=True,unique=True,verbose_name="Item Name", max_length=128)
    catagory_type = models.ForeignKey(Catagory, on_delete=models.CASCADE,verbose_name="Catagory",related_name='inventory_items')
    type = models.CharField(verbose_name="Type",max_length=128, choices = CHOICES) 
    quantity = models.DecimalField(verbose_name="Quantity", max_digits=5, decimal_places=3, validators=[MinValueValidator(Decimal("0.00"))])

    def __str__(self):
        return self.item_name