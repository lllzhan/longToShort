from django.db import models

# Create your models here.
class url(models.Model):
    shortUrl = models.CharField(max_length=20)
    longUrl = models.CharField(max_length=200)
    createAt = models.DateTimeField(auto_now_add=True)