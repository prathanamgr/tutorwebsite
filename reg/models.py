from django.conf import settings
from django.db import models

# Create your models here.
class userModel(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ph=models.CharField(max_length=20)
    gender=models.CharField(max_length=20)
    status=models.CharField(max_length=40)
    address=models.CharField(max_length=60)
    experience=models.CharField(max_length=60)
    prefer=models.CharField(max_length=60)
    online=models.BooleanField()
    profile=models.FileField()
    subject=models.CharField(max_length=60)

class meetings(models.Model):
    student=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='std')
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher')
    message=models.TextField()
    date=models.DateField()
    date2=models.DateTimeField()