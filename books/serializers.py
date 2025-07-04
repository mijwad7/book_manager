from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import Book, ReadingList, ReadingListItem

# Validator to prevent HTML tags and special characters
no_special_chars = RegexValidator(
    regex=r'^[^<>#&]*$',
    message='This field cannot contain HTML tags or special characters like #, <, >, &.'
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'},
                'required': False
            },
            'username': {'required': False},
            'email': {'required': False},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class BookSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255, validators=[no_special_chars])
    authors = serializers.CharField(max_length=255, validators=[no_special_chars])
    genre = serializers.CharField(max_length=100, validators=[no_special_chars])
    description = serializers.CharField(allow_blank=True, required=False, validators=[no_special_chars])

    class Meta:
        model = Book
        fields = ['id', 'title', 'authors', 'genre', 'publication_date', 'description', 'created_by', 'created_at']
        read_only_fields = ['created_by', 'created_at']


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

class ReadingListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255, validators=[no_special_chars])
    items = ReadingListItemSerializer(many=True, read_only=True)

    class Meta:
        model = ReadingList
        fields = ['id', 'name', 'user', 'created_at', 'items']
        read_only_fields = ['user', 'created_at', 'items']