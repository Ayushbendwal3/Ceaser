from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='images',blank=True)

    def __str__(self):
        return self.user.username

class Document(models.Model):
    document_id = models.AutoField
    document_name = models.CharField(max_length=50, null=False, blank=False, default="")
    document_img = models.ImageField(upload_to='media', default="", blank=False, null=False)
    document_desc = models.CharField(max_length=500, default="", blank=False, null=False)
    document_date = models.DateField()

    def __str__(self):
        return self.document_name