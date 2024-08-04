from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
   path('', views.home, name="index"),
   path('faces-list/', views.faces_list, name="faces-list"),
   path('recall/', views.recall, name="recall"),
   path('results/', views.results, name="results"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
