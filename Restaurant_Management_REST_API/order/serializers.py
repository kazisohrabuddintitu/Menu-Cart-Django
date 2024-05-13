from rest_framework import serializers
from .models import Order, OrderItem
from menu_item.serializers import MenuItemSerializer
from user.serializers import UserSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ("quantity", "menu_item")


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(read_only=True, many=True, source='orderitem_set')
    delivery_crew = UserSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ('id', 'items', 'status', 'total', 'date', 'delivery_crew')

    