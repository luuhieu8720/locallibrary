from django.db import models
from django.urls import reverse 
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
import uuid
from datetime import date
# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=200, help_text=_('Enter a book genre (e.g. Science Fiction)'))

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text=_('Enter a brief description of the book'))
    isbn = models.CharField('ISBN', max_length=13, unique=True,
                             help_text=_('13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>'))
    genre = models.ManyToManyField(Genre, help_text=_('Select a genre for this book'))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'

class BookInstance(models.Model):
    class Meta:
        permissions = (("can_mark_returned", "Set book as returned"),)

    @property
    def is_overdue(self):
        return self.due_back and date.today() > self.due_back

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text=_('Unique ID for this particular book across whole library'))
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text=_('Book availability'),
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f'{self.id} ({self.book.title})'

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'
