from django.db import models

# Create your models here.
class Product(models.Model):
    p_id = models.IntegerField()
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    colour = models.CharField(max_length=50)
    brand = models.CharField(max_length=100)
    img = models.URLField(max_length=500)
    description = models.TextField()
    
