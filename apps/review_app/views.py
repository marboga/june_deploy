# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import Review, Book, Author

# Create your views here.
def index(request):
    print 'review index'
    context = {
        'recent_reviews': Review.objects.order_by('-created_at')[:5],
        'other_reviews': Review.objects.order_by('-created_at')[5:],
    }
    return render(request, 'review_app/index.html', context)

def show_book(request):
    return render(request, 'review_app/show.html')

def create(request):
    print 'creating'
    worked = Review.objects.create_review(request.POST, request.session['id'])
    print worked
    return redirect('review_app:index')        

def add(request):
    context = {
        'author_list': Author.objects.all(),
    }
    return render(request, 'review_app/add.html', context)