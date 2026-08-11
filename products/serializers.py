from rest_framework import serializers
from .models import Product, WristSize


class WristSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model  = WristSize
        fields = ['id', 'label', 'cm', 'inches']


class ProductSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)
    image_url = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model  = Product
        fields = [
            'id', 'name', 'slug',
            'price', 'price_10pc', 'price_50pc', 'price_100pc',
            'stone_type', 'material', 'bead_size', 'color',
            'gender', 'shape', 'size_info',
            'image_url', 'category', 'whatsapp_link', 'is_featured',
        ]
