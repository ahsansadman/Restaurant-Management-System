from django.contrib.auth import models
from django.db.models import fields
from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from .models import InventoryItem
from .models import Catagory

class InventoryItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = InventoryItem
        fields = ('id', 'item_name', 'catagory_type', 'type', 'quantity')

# class OrderSerializer(WritableNestedModelSerializer):
    
#     order_items = OrderItemSerializer(many=True)

#     class Meta:
#         model = Order
#         fields =  ('id', 'customer_name', 'table_no', 'is_pending', 'is_prepared', 'order_items','bill')

    # def create(self, validated_data):
    #     item_data = validated_data.pop('order_items')
    #     order = Order.objects.create(**validated_data)
    #     for item in item_data:
    #         order.order_items.create(**item)
    #     return order