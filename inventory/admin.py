from django.contrib import admin
from django.contrib.admin.decorators import register
from .models import InventoryItem
from .models import Catagory
# Register your models here.

class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ['item_name', 'quantity', 'type']

admin.site.register(InventoryItem,InventoryItemAdmin)
admin.site.register(Catagory)