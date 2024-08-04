from django.db import models
from django.urls import reverse

# Create your models here.

class Face(models.Model):
    face = models.ImageField(upload_to="images/")
    
    def __str__(self):
	    return str(self.face)
    
class Name(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
	    return str(self.name)
