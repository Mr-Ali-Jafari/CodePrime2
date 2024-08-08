from django.db import models
from ckeditor.fields import RichTextField
from persiantools.jdatetime import JalaliDate

from django.contrib.auth.models import User
# Create your models here.

class PrimeCast(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    slug = models.SlugField()
    banner = models.ImageField(upload_to="prime_cast/banner/%Y/")
    desc = RichTextField()
    voice = models.FileField(upload_to="prime_cast/voice/%Y/")
    date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"Title: {self.title} - Who Published: {self.user.username} - date: {JalaliDate(self.date)} - Active ? {self.is_active}"
   


class CommentCast(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField()
    primecast = models.ForeignKey(PrimeCast,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.primecast.title} - Active?{self.is_active}"






class ReplyCast(models.Model):    
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField()
    key = models.ForeignKey(CommentCast,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.key.primecast.title}"