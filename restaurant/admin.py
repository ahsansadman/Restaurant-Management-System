
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import *

# from .models import Beverage



class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ['username','id', 'email', 'first_name', 'last_name','user_type','cooking_station','is_active']
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'first_name', 'last_name','user_type', 'cooking_station','nid', 'date_of_birth', 'address1', 'address2', 'zip_code', 'city', 'country', 'mobile_phone', 'additional_information', 'photo',)}),
    )
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type','cooking_station','nid','date_of_birth', 'address1', 'address2', 'zip_code', 'city', 'country', 'mobile_phone', 'additional_information', 'photo',)}),
    )

class MenuItemInline(admin.TabularInline):
    model = MenuItem

class CatagoryAdmin(admin.ModelAdmin):
    inlines = [MenuItemInline,]
    list_display = ['title','is_indoor', 'is_outdoor']

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'rating', 'catagory_type']

# class BeverageAdmin(admin.ModelAdmin):
#     list_display = ['title', 'price', 'rating', 'catagory_type']

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'email','mobile_phone']

class OrderItemInline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline,]
    list_display = ['customer_name','table_no', 'is_pending', 'is_prepared','order_time']

class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_id', 'item_name', 'item_type', 'price', 'amount']

class RecipeItemInline(admin.TabularInline):
    model = RecipeItem

class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeItemInline,]


admin.site.register(User, CustomUserAdmin)
admin.site.register(Catagory,CatagoryAdmin)
admin.site.register(CookingStation)
admin.site.register(UserType)
admin.site.register(MenuItem,MenuItemAdmin)
# admin.site.register(Beverage,BeverageAdmin)
# admin.site.register(Customer,CustomerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Recipe,RecipeAdmin)
# admin.site.register(RecipeItem)
# admin.site.register(Item,ItemAdmin)


