from django.http.response import HttpResponse
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
# from rest_framework.authtoken.models import Token
from django.http import Http404
from decimal import Decimal
from .models import *
from .serializers import *
from inventory.models import InventoryItem
from .custom_permissions import ActualDjangoModelPermissions


from django.shortcuts import render
from django.template.context import RequestContext

def home(request):
    context =    {'request': request,
                 'user': request.user}
    print(request.META)
    return render(request,'home.html',
                             context=context)

class Register(generics.ListCreateAPIView):

    permission_classes = []
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    def post(self,request):
        try:
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(request)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
        except User.DoesNotExist:
            raise Http404   


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
 
    permission_classes = [IsAuthenticated,ActualDjangoModelPermissions]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get(self,request, format=None):
        try:
            user = User.objects.get(username=request.user)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            raise Http404        
         

    def put(self, request, format=None):
        try:
            user = User.objects.get(username=request.user)
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            raise Http404

class MenuList(generics.ListAPIView):
    # authentication_classes = [TokenAuthentication]
    permission_classes = []
    queryset = Catagory.objects.all()
    serializer_class = CatagoryFoodSerializer


# class OutdoorMenuList(generics.ListAPIView):
    
#     # permission_classes = [ActualDjangoModelPermissions]
#     queryset = Catagory.objects.filter(is_outdoor=True)
#     serializer_class = CatagoryFoodSerializer
    
# class IndoorMenuList(generics.ListAPIView):
    
#     # permission_classes = [ActualDjangoModelPermissions]
#     queryset = Catagory.objects.filter(is_indoor=True)
#     serializer_class = CatagoryFoodSerializer
    

class OrderList(generics.ListCreateAPIView):

    permission_classes = [IsAuthenticated,ActualDjangoModelPermissions]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self,request):
        try:
            queryset = Order.objects.filter(is_prepared=False)
            serializer = OrderSerializer(queryset, context={'request': request}, many = True)
            return Response(serializer.data)
        except Order.DoesNotExist:
            raise Http404          
    def post(self,request):
        try:
            serializer = OrderSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
        except Order.DoesNotExist:
            raise Http404   
    
class CookingStationOrderList(generics.ListAPIView):

    permission_classes = [IsAuthenticated,ActualDjangoModelPermissions]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    def get(self,request,station):
        user = User.objects.get(username=request.user.username)
        if str(user.cooking_station).casefold() == station.casefold():
            try:
                queryset = Order.objects.distinct().filter(is_prepared=False).filter(ordered_items__cooking_station=station)
                serializer = OrderSerializer(queryset, context={'request': request}, many = True)
                return Response(serializer.data)
            except Order.DoesNotExist:
                raise Http404
        else:
            return Response({ 'message': 'You do not have authorization to view this page.'})      

class OrderDetail(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAuthenticated,ActualDjangoModelPermissions]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    def get(self,request, pk, format=None):
        try:
            data = Order.objects.get(id=pk)
            serializer = OrderSerializer(data)
            return Response(serializer.data)
        except Order.DoesNotExist:
            raise Http404        

    def put(self, request, pk, format=None):
        try:
            data = Order.objects.get(id=pk)
            temp = Order.objects.get(id=pk)
            serializer = OrderSerializer(data, data=request.data)
            if serializer.is_valid():
                serializer.save()
                update_inventory(serializer.data, temp)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        try:
            data = Order.objects.get(id=pk)
            data.delete()
            return Response(status=status.HTTP_204_NO_CONTENT) 
        except Order.DoesNotExist:
            raise Http404       

class OrderItemDetail(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAuthenticated,ActualDjangoModelPermissions]
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    
    def get(self,request, pk, format=None):
        try:
            data = OrderItem.objects.get(id=pk)
            serializer = OrderItemSerializer(data)
            return Response(serializer.data)
        except OrderItem.DoesNotExist:
            raise Http404        

    def put(self, request, pk, format=None):
        try:
            data = OrderItem.objects.get(id=pk)
            serializer = OrderItemSerializer(data, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except OrderItem.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        try:
            data = OrderItem.objects.get(id=pk)
            data.delete()
            return Response(status=status.HTTP_204_NO_CONTENT) 
        except OrderItem.DoesNotExist:
            raise Http404


def update_inventory(data, temp):
    print(data["is_prepared"])
    print(temp.is_prepared)
    if data["is_prepared"] == True and temp.is_prepared == False:
        ordered_items = data.pop('ordered_items')
        try:
            for ordered_item in ordered_items:            
                menu_item = MenuItem.objects.get(title = ordered_item["item_name"])
                recipe = Recipe.objects.get(menu_item = menu_item)
                recipe_items = RecipeItem.objects.filter(recipe = recipe)
                for recipe_item in recipe_items:
                    inventory_item =InventoryItem.objects.get(pk = recipe_item.ingredient.pk)
                    deduct = round((Decimal((recipe_item.amount*0.001)*ordered_item["amount"])),3)
                    updated_quantity = inventory_item.quantity - deduct
                    inventory_item.quantity = updated_quantity
                    inventory_item.save()
                    print(inventory_item.quantity)
                    print(deduct)
        except MenuItem.DoesNotExist:
                print("MenuItem doesn't exist.")
        except Recipe.DoesNotExist:
                print("Recipe doesn't exist.")
        except RecipeItem.DoesNotExist:
                print("RecipeItem doesn't exist.")
        except InventoryItem.DoesNotExist:
                print("InventoryItem doesn't exist.")