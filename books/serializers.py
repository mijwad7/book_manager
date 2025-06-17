from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Book, ReadingList, ReadingListItem

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'},
                'required': False  # Allow partial updates without password
            },
            'username': {'required': False},  # Allow partial updates without username
            'email': {'required': False},  # Allow partial updates without email
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        # Handle password hashing during updates
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password is not None:
            instance.set_password(password)  # Hash the password
        instance.save()
        return instance


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'authors', 'genre', 'publication_date', 'description', 'created_by', 'created_at']
        read_only_fields = ['created_by', 'created_at']

class ReadingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingList
        fields = ['id', 'name', 'user', 'created_at']
        read_only_fields = ['user', 'created_at']

class ReadingListItemSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), source='book', write_only=True)
    reading_list = serializers.PrimaryKeyRelatedField(
        queryset=ReadingList.objects.none(),
        write_only=True
    )

    class Meta:
        model = ReadingListItem
        fields = ['id', 'reading_list', 'book', 'book_id', 'order', 'added_at']
        read_only_fields = ['added_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'request' in self.context:
            user = self.context['request'].user
            if user.is_authenticated:
                self.fields['reading_list'].queryset = ReadingList.objects.filter(user=user)

    def validate_reading_list(self, value):
        if value.user != self.context['request'].user:
            raise serializers.ValidationError("You can only add items to your own reading lists.")
        return value