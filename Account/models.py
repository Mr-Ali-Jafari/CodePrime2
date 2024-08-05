from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from persiantools.jdatetime import JalaliDate

# Create your models here.

class Teacher(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=350)
    family = models.CharField(max_length=350)
    picture = models.ImageField(upload_to='teachers/picture/%Y/')
    birthday = models.DateField()
    biography = RichTextField()
    city = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.user} Owned This Profile | {self.name} - {self.family}"
    

class Participation(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=350)
    family = models.CharField(max_length=350)
    number = models.CharField(max_length=11)

    gender = models.CharField(max_length=1000,choices=[('زن','زن'),('مرد','مرد')])

    birthday = models.DateField()
    city = models.CharField(max_length=1000)
    participate_type = models.CharField(max_length=1000,choices=[("برنامه نویسی",'برنامه نویسی'),('بازاریابی','بازاریابی'),('ادیت','ادیت')])
    text = models.TextField()
    info_card = models.ImageField(upload_to="info/cards/")