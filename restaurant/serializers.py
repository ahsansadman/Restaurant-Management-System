from django.contrib.auth import models
from django.db.models import fields
from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_auth.serializers import TokenSerializer
from django_countries.serializers import CountryFieldMixin
from drf_writable_nested.serializers import WritableNestedModelSerializer
from .models import *

class MenuItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = MenuItem 
        fields = ('id', 'title','cooking_station', 'description', 'price', 'rating', 'catagory_type', 'image')

class CatagoryFoodSerializer(serializers.ModelSerializer):
    
    items = MenuItemSerializer(many=True)
    
    class Meta:
        model = Catagory 
        fields = ('title','items')

class OrderItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OrderItem
        fields = ('id', 'item_name', 'catagory','cooking_station', 'price', 'amount','is_prepared')

class OrderSerializer(WritableNestedModelSerializer):
    
    ordered_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields =  ('id', 'customer_name','server_name','table_no', 'is_pending', 'is_prepared', 'discount','vat','service_charge','bill', 'order_time','ordered_items')

    # def create(self, validated_data):
    #     item_data = validated_data.pop('order_items')
    #     order = Order.objects.create(**validated_data)
    #     for item in item_data:
    #         order.order_items.create(**item)
    #     return order

class RegisterSerializer(CountryFieldMixin,serializers.ModelSerializer):

    password = serializers.CharField(style= {'input_type': 'password'}, write_only=True)
    confirm_password = serializers.CharField(style= {'input_type': 'password'}, write_only=True)

    class Meta:
        model = User 
        fields = ('username','first_name', 'last_name','email','password','confirm_password', 'date_of_birth', 'address1', 'address2', 'zip_code', 'city', 'country', 'mobile_phone', 'additional_information')


    def save(self,request):
        user = User(
            username = self.validated_data['username'],
            first_name = self.validated_data['first_name'],
            last_name = self.validated_data['last_name'],
            email = self.validated_data['email'],
            date_of_birth = self.validated_data['date_of_birth'],
            address1 = self.validated_data['address1'],
            address2 = self.validated_data['address2'],
            zip_code = self.validated_data['zip_code'],
            city = self.validated_data['city'],
            country = self.validated_data['country'],
            mobile_phone = self.validated_data['mobile_phone'],
            additional_information = self.validated_data['additional_information'],
            
        )
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']

        if password != confirm_password:
            raise serializers.ValidationError({'password' : 'Passwords do not match. '})
        
        user.set_password(password)
        user.save()
        group = Group.objects.get(name='Customer')
        user.groups.add(group)
        return user

class UserSerializer(CountryFieldMixin,serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name','email','password','user_type','cooking_station', 'date_of_birth', 'address1', 'address2', 'zip_code', 'city', 'country', 'mobile_phone', 'additional_information')


class CustomTokenSerializer(TokenSerializer):
    user = UserSerializer(read_only=True)

    class Meta(TokenSerializer.Meta):
        fields = ('key', 'user')

