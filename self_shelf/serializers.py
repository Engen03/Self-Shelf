from rest_framework import serializers
from .models import Book, Author, Genre, Favorite, Review
from django.contrib.auth.models import User

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    genre = GenreSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), write_only=True, source='author', required=False)
    genre_id = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), write_only=True, source='genre', required=False)

    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ('cover_image', 'book_file')

class BookFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['book_file']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class FavoriteSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), write_only=True, source='book')

    class Meta:
        model = Favorite
        fields = ['id', 'book', 'book_id']

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True) # Отображаем username вместо id

    class Meta:
        model = Review
        fields = ['id', 'user', 'book', 'text', 'rating', 'created_at']
        read_only_fields = ('user', 'created_at')