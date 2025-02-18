from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Meal

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  
        fields = ['id', 'username', 'password']
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  
        fields = ['weight', 'height']

    def update(self, instance, validated_data):
        instance.weight = validated_data.get("weight", instance.weight)
        instance.height = validated_data.get("height", instance.height)
        instance.save()
        return instance


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal  
        fields = ['id', 'user', 'name', 'calories', 'date']

        extra_kwargs = {'user': {'read_only': True}}