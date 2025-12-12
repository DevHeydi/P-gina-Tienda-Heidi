from django.db import models

class stores(models.Model):
    name=models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
       return self.name 

class products(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    store = models.ForeignKey(stores, 
    on_delete=models.CASCADE)
    sold = models.BooleanField(default=False)

    def __str__(self):
       return self.title 

