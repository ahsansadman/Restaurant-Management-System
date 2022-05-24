from django.shortcuts import render
from .custom_permissions import ActualDjangoModelPermissions
from .models import InventoryItem
from django.views import View
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from .serializers import *
# Create your views here.

class InventoryList(generics.ListAPIView):
    
    permission_classes = [IsAuthenticated,ActualDjangoModelPermissions]
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer

    def get(self,request):
        try:
            queryset = InventoryItem.objects.all()
            serializer = InventoryItemSerializer(queryset, context={'request': request}, many = True)
            return Response(serializer.data)
        except InventoryItem.DoesNotExist:
            raise Http404         


# class UpdateInventory(generics.RetrieveUpdateDestroyAPIView):

#     permission_classes = [ActualDjangoModelPermissions]
#     queryset = InventoryItem.objects.all()
#     serializer_class = InventoryItemSerializer

#     def get(self,request, pk, format=None):
#         try:
#             data = InventoryItem.objects.get(id=pk)
#             serializer = InventoryItemSerializer(data)
#             return Response(serializer.data)
#         except InventoryItem.DoesNotExist:
#             raise Http404   
    
#     def put(self, request, pk, format=None):
#         try:
#             order_data = Order.objects.get(id=pk)
#             serializer = OrderSerializer(order_data, data=request.data)
#             items = serializer.data.pop('order_items')
#             print(items)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Order.DoesNotExist:
#             raise Http404
