from django.db import models

# Create your models here.
class message(models.Model):
    name=models.CharField(max_length=525)
    email= models.EmailField( max_length=254)
    message=models.TextField()