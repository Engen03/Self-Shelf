from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import BookViewSet, AuthorViewSet, GenreViewSet, UserRegistrationView, UserLoginView, CurrentUserView, FavoriteViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'favorites', FavoriteViewSet, basename='favorite')

books_router = routers.NestedSimpleRouter(router, r'books', lookup='book')
books_router.register(r'reviews', ReviewViewSet, basename='book-reviews')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(books_router.urls)),
    path('users/register/', UserRegistrationView.as_view(), name='user-register'),
    path('users/login/', UserLoginView.as_view(), name='user-login'),
    path('users/me/', CurrentUserView.as_view(), name='current-user'),
]