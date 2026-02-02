from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UploadedDataset

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedDataset
        fields = '__all__'