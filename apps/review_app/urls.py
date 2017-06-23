from django.conf.urls import url

from . import views

app_name="review_app"
urlpatterns=[
    url(r'^$', views.index, name="index"),
    url(r'^(?P<id>\d+)$', views.show_book, name="show_book"),
    url(r'^create$', views.create, name="create"),
    url(r'^add$', views.add, name="add"),

]
