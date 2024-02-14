from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser, Comment
from django.core.validators import FileExtensionValidator




class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        # ...

        return token


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    # image = serializers.ImageField(validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),], required=False)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        if 'image' in attrs and attrs['image'] is not None and attrs['image'].size > 1024 * 1024:
            raise serializers.ValidationError(
                {"image": "The file size must be less than 1 MB."})

        return attrs

    def create(self, validated_data):
        # image = validated_data.get('image')
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
    )
        user.set_password(validated_data['password'])
        user.save()
        
        return user


class CommentSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Comment
        fields = ['id', 'body', 'user', 'commentator', 'created', 'updated']
        read_only_fields = ('user', 'created', 'updated')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().update(instance, validated_data)
    

class ProfileSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'username', 'bio', 'comments', 'image',)

    def to_internal_value(self, data):
        cleaned_data = {}
        for key, value in data.items():
            if isinstance(value, bytes):
                cleaned_data[key] = value.decode('utf-8', errors='replace')
            else:
                cleaned_data[key] = value
        return super().to_internal_value(cleaned_data)