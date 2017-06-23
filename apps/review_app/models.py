# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..login.models import User

# Create your models here.
class ReviewManager(models.Manager):
    def create_review(self, data, user_id):
        print data, '<><><><>' ,user_id
        errors = []
        if len(data['title']) < 2:
            errors.append('title is too short')

        if errors:
            return (False, errors)
        else:
            user = User.objects.get(id=user_id)
            new_author = Author(
                first_name=data['new_author_first'],
                last_name=data['new_author_last']
            )
            new_author.save()
            print new_author
            new_book = Book(
                title=data['title'],
            )
            new_book.save()
            new_book.authors.add(new_author)
            new_review = Review.objects.create(
                rating=data['rating'],
                content=data['review'],
                book=new_book,
                rater=user
            )
            print new_review
            return (True, new_review)
        

class Author(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    #books

    def __str__(self):
        return self.first_name + " " + self.last_name

class Book(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author, related_name='books')
    #review

    def __str__(self):
        return self.title

class Review(models.Model):
    rating = models.IntegerField()
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rater = models.ForeignKey(User, related_name="reviews")
    book = models.ForeignKey(Book, related_name='review')
    objects = ReviewManager()

#User
    #reviews
