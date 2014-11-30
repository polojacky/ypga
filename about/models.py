from django.db import models

# the model for sumbit form
class submitModel(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=50)
    institute = models.CharField(max_length=200)
    content = models.TextField()
    time = models.DateTimeField(auto_now=True, auto_now_add=True)

    class Meta:
        unique_together = (("name", "email","institute"),)

# the model for contact form
class contactModel(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    email = models.EmailField()
    time = models.DateTimeField(auto_now=True, auto_now_add=True)

class staticticsModel(models.Model):
    tableName = models.CharField(max_length=255)
    itemNumber = models.IntegerField()
    source = models.CharField(max_length=255)
    notes = models.CharField(max_length=255)
