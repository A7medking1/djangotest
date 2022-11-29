from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Category


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Favorite
        fields = ('id','isFavorite' , 'product')      
        depth=1

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('id', 'quantity', 'product')
        depth = 1


class CartItemAddSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ('quantity', 'product_id')
        extra_kwargs = {
            'quantity': {'required': True},
            'product_id': {'required': True},
        }

    def create(self, validated_data):
        user = User.objects.get(id=self.context['request'].user.id)
        product = get_object_or_404(Product, id=validated_data['product_id'])
             
        cart_item = CartItem.objects.create(
            product=product,
            user=user,
            quantity=validated_data['quantity']
            )
        cart_item.save()
        
        return cart_item

