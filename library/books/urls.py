from django.urls import path

from . import views

urlpatterns = [
    path('books/<int:pk>', views.BookDetail.as_view(), name='detail'),
    path('books/', views.BookList.as_view(), name="list"),
    path('db/', views.LibrarySave.as_view(), name="save_books"),
]
