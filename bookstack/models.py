from django.db import models

class Book(models.Model):
    id= models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)