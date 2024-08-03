from django.urls import path
from . import views

urlpatterns = [
   path('', views.home, name="index"),
   path('faces-list/', views.faces_list, name="faces-list"),
   path('recall/', views.recall, name="recall"),
   path('results/', views.results, name="results"),

]
