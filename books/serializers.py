from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Book, ReadingList, ReadingListItem

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

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

    class Meta:
        model = ReadingListItem
        fields = ['id', 'reading_list', 'book', 'book_id', 'order', 'added_at']
        read_only_fields = ['added_at']