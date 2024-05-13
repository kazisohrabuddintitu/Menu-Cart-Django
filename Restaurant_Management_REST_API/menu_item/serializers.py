from rest_framework import serializers
from .models import MenuItem, Category
from rest_framework.validators import UniqueTogetherValidator


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','slug', 'title']
    
    

class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category', 'category_id']
        extra_kwargs = {
            'price':{'min_value': 0},
        }
        validators = [
            UniqueTogetherValidator(
                queryset=MenuItem.objects.all(),
                fields=['title', 'category_id']
            )
        ]