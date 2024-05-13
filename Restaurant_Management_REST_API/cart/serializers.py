from .models import Cart
from menu_item.serializers import MenuItemSerializer
from rest_framework import serializers
from django.core.validators import MinValueValidator
from menu_item.models import MenuItem


class CartSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer(read_only=True)
    menu_item_id = serializers.IntegerField(write_only=True)
    quantity = serializers.IntegerField(min_value=1)

    class Meta:
        model = Cart
        fields = ('id', 'menu_item', 'menu_item_id', 'unit_price', 'quantity', 'price')
        read_only_fields = ('unit_price', 'price')

    def validate_menu_item_id(self, menu_item_id):
        try:
            menu_item = MenuItem.objects.get(id=menu_item_id)
        except MenuItem.DoesNotExist:
            raise serializers.ValidationError("Invalid menu_item_id")
        return menu_item_id
    
    def create(self, validated_data):
        menu_item_id = validated_data.pop('menu_item_id')
        menu_item = MenuItem.objects.get(id=menu_item_id)
        quantity = validated_data.pop('quantity')
        user = self.context['request'].user
        cart, created = Cart.objects.get_or_create(
            user=user, menu_item=menu_item,
            defaults={'quantity': quantity, 'unit_price': menu_item.price, 'price': menu_item.price * quantity}
        )
        if not created:
            cart.quantity += quantity
            cart.price = cart.quantity * cart.unit_price
            cart.save()
        return cart