from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True)
    publication_year = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)
    book_file = models.FileField(upload_to='book_files/', null=True, blank=True)

    def __str__(self):
        return str(self.title)

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)]) # Оценка от 1 до 5
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title} - {self.rating}"