from django.urls import path
from . import views

urlpatterns = [
    path('text', views.search_text_view, name='search')
]
