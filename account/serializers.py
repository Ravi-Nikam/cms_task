# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from .models import Post, Like

User = get_user_model()

class UpdateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    date_of_birth = serializers.DateField(required=True)
    gender = serializers.CharField(required=True)
    
    class Meta:
        model = User
        exclude = ["email", "password"]

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.save()
        return instance

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    date_of_birth = serializers.DateField(required=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'phone', 'date_of_birth', 'gender', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            phone=validated_data['phone'],
            date_of_birth=validated_data['date_of_birth'],
            gender=validated_data['gender'],
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if user is None:
                raise serializers.ValidationError("Invalid email or password")
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'")

        data['user'] = user
        return data
    

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'content', 'creation_date', 'updation_date', 'owner', 'is_public']

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'post', 'user']