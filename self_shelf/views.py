from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action

from .models import Book, Author, Genre, Favorite, Review
from .serializers import BookSerializer, AuthorSerializer, GenreSerializer, UserSerializer, FavoriteSerializer, ReviewSerializer, BookFileSerializer
from .permissions import IsOwnerOrReadOnly

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'author__first_name', 'author__last_name', 'genre__name', 'publication_year']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        elif self.action == 'download':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        book = self.get_object()
        if book.book_file:
            response = FileResponse(book.book_file, as_attachment=True)
            return response
        else:
            return Response({'detail': 'Файл книги отсутствует.'}, status=status.HTTP_404_NOT_FOUND)

class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        # Здесь можно добавить свою логику аутентификации, например, с использованием JWT
        # В этом примере просто возвращаем сообщение об успехе
        return Response({'message': 'Вход выполнен успешно'}, status=status.HTTP_200_OK)

class CurrentUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        book_id = self.kwargs['book_pk']
        return Review.objects.filter(book_id=book_id)

    def perform_create(self, serializer):
        book = get_object_or_404(Book, pk=self.kwargs['book_pk'])
        serializer.save(user=self.request.user, book=book)