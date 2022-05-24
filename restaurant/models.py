from enum import Flag
from django.contrib.auth.models import AbstractUser, AnonymousUser
from django.core.validators import RegexValidator, integer_validator
from django.db import models
from django.db.models.fields import CharField, DateTimeField, IntegerField
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from django.db import models
import uuid
from django.db.models import Sum
from inventory.models import InventoryItem

# Create your models here.
class CookingStation(models.Model):
    
    station_name = models.CharField(primary_key=True,unique=True,verbose_name=_("Station Name"), max_length=50)

    class Meta:
        ordering = ['station_name']

    def __str__(self):
        return self.station_name

class Catagory(models.Model):


    title = models.CharField(primary_key=True,unique=True,verbose_name='Title',max_length=50)
    is_indoor = models.BooleanField(default = False, verbose_name= "Indoor")
    is_outdoor = models.BooleanField(default = False, verbose_name= "Outdoor")

    class Meta:
        ordering = ['title']
    def __str__(self):
        return self.title
        
class MenuItem(models.Model):

    
    RATING_CHOICES =( 
        ("1", "1"), 
        ("2", "2"), 
        ("3", "3"), 
        ("4", "4"), 
        ("5", "5"), 
    )
     
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=256)
    cooking_station = models.ForeignKey(CookingStation, verbose_name=_("Cooking Station"), on_delete=models.CASCADE, related_name= 'menu_items',null=True)
    price = models.IntegerField(verbose_name="Price")
    rating = models.CharField(verbose_name="Rating",max_length=50,choices = RATING_CHOICES)
    catagory_type = models.ForeignKey(Catagory, on_delete=models.CASCADE,verbose_name="Catagory",related_name='items')
    image = models.ImageField(upload_to='foodImages', height_field=None, width_field=None, max_length=None)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    

class Recipe(models.Model):
        
    menu_item = models.OneToOneField(MenuItem, verbose_name=_("Menu Item"), on_delete=models.CASCADE)
    
    
    class Meta:
        ordering = ['menu_item']
    def __str__(self):
        return self.menu_item.title

class RecipeItem(models.Model):
    
    recipe = models.ForeignKey(Recipe, verbose_name=_("Recipe"), on_delete=models.CASCADE, related_name= "recipe")
    ingredient = models.ForeignKey(InventoryItem, verbose_name=_("Ingredient"), on_delete=models.CASCADE, related_name="inventory_item")
    amount = models.PositiveIntegerField(_("Amount"),help_text='in grams')
    
    class Meta:
        ordering = ['recipe']
    def __str__(self):
        return self.recipe.menu_item.title


class UserType(models.Model):

    type = models.CharField(primary_key=True,unique=True,verbose_name=_("Type"), max_length=50)

    class Meta:
        ordering = ['type']
        
    def __str__(self):
        return self.type

   

class User(AbstractUser):

    username = models.CharField(unique=True,verbose_name=_("username"), max_length=30)
    user_type = models.ForeignKey(UserType, verbose_name=_("User Type"),related_name='users', on_delete=models.CASCADE,blank=True, null=True)
    cooking_station = models.ForeignKey(CookingStation, verbose_name=_("Cooking Station"), on_delete=models.CASCADE,related_name='users',blank=True, null=True)
    nid = models.PositiveIntegerField(blank=True,null=True)
    date_of_birth = models.DateField(verbose_name=_("Date of birth"), blank=True, null=True)
    address1 = models.CharField(verbose_name=_("Address line 1"), max_length=1024, blank=True, null=True)
    address2 = models.CharField(verbose_name=_("Address line 2"), max_length=1024, blank=True, null=True)
    zip_code = models.CharField(verbose_name=_("Postal Code"), max_length=12, blank=True, null=True)
    city = models.CharField(verbose_name=_("City"), max_length=1024, blank=True, null=True)
    country = CountryField(blank=True, null=True)
    phone_regex = RegexValidator(regex=r"^\+(?:[0-9]●?){6,14}[0-9]$", message=_("Enter a valid international mobile phone number starting with +(country code)"))
    mobile_phone = models.CharField(validators=[phone_regex], verbose_name=_("Mobile phone"), max_length=17, blank=True, null=True)
    additional_information = models.CharField(verbose_name=_("Additional information"), max_length=4096, blank=True, null=True)
    photo = models.ImageField(verbose_name=_("Photo"), upload_to='User photos/', default='photos/default-user-avatar.png')

    

    class Meta:
        ordering = ['username']

    def __str__(self):
        return self.username

# class Customer(models.Model):

#     username = models.CharField(unique=True,verbose_name=_("User Name"), max_length=30)
#     first_name = models.CharField(verbose_name=_("First Name"), max_length=128)
#     last_name = models.CharField(verbose_name=_("Last Name"), max_length=128)
#     email = models.EmailField(verbose_name="Email", max_length=254)
#     nid = models.PositiveIntegerField(blank=True,null=True)
#     date_of_birth = models.DateField(verbose_name=_("Date of birth"), blank=True, null=True)
#     address1 = models.CharField(verbose_name=_("Address line 1"), max_length=1024, blank=True, null=True)
#     address2 = models.CharField(verbose_name=_("Address line 2"), max_length=1024, blank=True, null=True)
#     zip_code = models.CharField(verbose_name=_("Postal Code"), max_length=12, blank=True, null=True)
#     city = models.CharField(verbose_name=_("City"), max_length=1024, blank=True, null=True)
#     country = CountryField(blank=True, null=True)
#     phone_regex = RegexValidator(regex=r"^\+(?:[0-9]●?){6,14}[0-9]$", message=_("Enter a valid international mobile phone number starting with +(country code)"))
#     mobile_phone = models.CharField(validators=[phone_regex], verbose_name=_("Mobile phone"), max_length=17, blank=True, null=True)
#     additional_information = models.CharField(verbose_name=_("Additional information"), max_length=4096, blank=True, null=True)
#     photo = models.ImageField(verbose_name=_("Photo"), upload_to='Customer photos/', default='photos/default-user-avatar.png')

#     def __str__(self):
#         return f"{self.username}: {self.first_name} {self.last_name}"

class Order(models.Model):


    customer_name = models.CharField(verbose_name=_("Customer Name"), max_length=128)
    server_name = models.CharField(verbose_name=_("Server Name"), max_length=128,blank=True,null=True)
    table_no = models.PositiveIntegerField(blank=False,null=False)
    is_pending = models.BooleanField(default=True)
    is_prepared = models.BooleanField(default=False)
    discount = models.PositiveIntegerField(verbose_name=_("Discount"),blank=True,null=True)
    vat = models.PositiveIntegerField(verbose_name=_("Vat"),blank=False,null=False)
    service_charge = models.PositiveIntegerField(verbose_name=_("Service Charge"),blank=False,null=False)
    bill = models.PositiveIntegerField(verbose_name=_("Bill"),blank=False,null=False)
    order_time = models.DateTimeField(verbose_name=_("Order Time"),auto_now_add=True)

    class Meta:
        ordering = ['order_time']


class OrderItem(models.Model):

    order_id = models.ForeignKey(Order, verbose_name=_("Order ID"), on_delete=models.CASCADE,related_name='ordered_items')
    item_name = models.CharField(verbose_name="Item Name", max_length=128)
    catagory = models.CharField(verbose_name="Catagory", max_length=128)
    cooking_station = models.CharField(verbose_name="Cooking Station", max_length=128)
    price = models.PositiveIntegerField()
    amount = models.PositiveIntegerField()
    is_prepared = models.BooleanField(default=False)


    class Meta:
        ordering = ['catagory']