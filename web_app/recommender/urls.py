from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # Ana sayfa
    path('recommend/', views.recommend, name='recommend'), # Öneri butonu basıldığında gidecek yol
]