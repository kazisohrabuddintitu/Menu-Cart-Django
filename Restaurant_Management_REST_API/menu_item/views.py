from rest_framework.response import Response
from .models import MenuItem
from .serializers import MenuItemSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from permissions import IsManager
from rest_framework.throttling import UserRateThrottle
from custom_pagination import CustomPagination


class MenuItemList(APIView):
    authentication_classes = [TokenAuthentication]
    throttle_classes = [UserRateThrottle]
    
    def get(self, request):
        items = MenuItem.objects.select_related('category')
        category_name = request.query_params.get('category')
        l_price = request.query_params.get('l_price')
        r_price = request.query_params.get('r_price')
        ordering = request.query_params.get('ordering')
        if category_name:
            items = items.filter(category__title__icontains=category_name)
        if l_price:
            items = items.filter(price__gte=l_price)
        if r_price:
            items = items.filter(price__lte=r_price)
        if ordering:
            ordering_fields = ordering.split(",")
            items = items.order_by(*ordering_fields)
        # Paginate the queryset
        paginator = CustomPagination()
        paginated_items = paginator.paginate_queryset(items, request)
        serialized_items = MenuItemSerializer(paginated_items, many=True)
        paginated_response = paginator.get_paginated_response(serialized_items.data)
        return Response(paginated_response, status=status.HTTP_200_OK)
    
    def post(self, request):
        self.check_permissions(request)
        serialized_item = MenuItemSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status=status.HTTP_201_CREATED)
        
    def get_permissions(self):
        if self.request.method == 'POST':
            # Apply IsManager permission class only for POST method
            return [IsManager()]  # Add any other permission classes if needed
        else:
            # No permission classes for other methods
            return []
        
    

class MenuItemDetail(APIView):
    authentication_classes = [TokenAuthentication]
    throttle_classes = [UserRateThrottle]
    
    def get(self, request, pk):
        item = get_object_or_404(MenuItem, pk=pk)
        serialized_item = MenuItemSerializer(item)
        return Response(serialized_item.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        self.check_permissions(request)
        item = get_object_or_404(MenuItem, pk=pk)
        serialized_item = MenuItemSerializer(item, data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status=status.HTTP_200_OK)
    
    def patch(self, request, pk):
        self.check_permissions(request)
        item = get_object_or_404(MenuItem, pk=pk)
        serialized_item = MenuItemSerializer(item, data=request.data, partial=True)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        self.check_permissions(request)
        item = get_object_or_404(MenuItem, pk=pk)
        item.delete()
        return Response(status=status.HTTP_200_OK)
        
    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE', 'PATCH']:
            # Apply IsManager permission class only for POST method
            return [IsManager()]  # Add any other permission classes if needed
        else:
            # No permission classes for other methods
            return []