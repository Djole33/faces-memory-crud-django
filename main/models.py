from django.db import models
from django.urls import reverse

# Create your models here.

class Face(models.Model):
    face = models.ImageField(upload_to="images/")
    
    def __str__(self):
	    return self.face
