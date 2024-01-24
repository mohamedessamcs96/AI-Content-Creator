from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from django.contrib.auth.hashers import make_password

# Create your models here.

GENDER_CHOICES = (
    ('m', 'male'),
    ('f', 'female')
)


# Create your models here.

class UserAdmin(AbstractUser):
    fname = models.CharField(max_length=18, default='')
    lname = models.CharField(max_length=18, default='')
    email = models.EmailField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birthdate = models.DateField(null=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    password1 = models.CharField(max_length=20)
    password2 = models.CharField(max_length=20)
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.fname + ' ' + self.lname


class HomeInfo(models.Model):
    admin = models.ForeignKey(UserAdmin, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=255)
    title_ar_field = models.CharField(max_length=200)
    description_ar_field = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images')
    background = models.ImageField(upload_to='images')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    


class TargetAudience(models.Model):
    admin = models.ForeignKey(UserAdmin, on_delete=models.CASCADE, null=True)
    target_audience=models.CharField(max_length=200)
    
    def __str__(self):
        return self.target_audience
    
class Style(models.Model):
    admin = models.ForeignKey(UserAdmin, on_delete=models.CASCADE, null=True)
    style=models.CharField(max_length=200)
    
    def __str__(self):
        return self.style


#influncer,socialmedia contentcreator,bloggers,video contentcreator    
class Types(models.Model):
    admin = models.ForeignKey(UserAdmin, on_delete=models.CASCADE, null=True)
    type=models.CharField(max_length=200)
    
    def __str__(self):
        return self.type



class ContentCreator(models.Model):
    admin = models.ForeignKey(UserAdmin, on_delete=models.CASCADE, null=True)
    subject=models.CharField(max_length=200)
    purpose=models.CharField(max_length=200)
    message=models.CharField(max_length=200)
    types=models.ForeignKey(Types,related_name='audiece',on_delete=models.CASCADE, null=True)
    word_count=models.IntegerField()
    target_audience = models.ForeignKey(TargetAudience,related_name='audiece_target_content',on_delete=models.CASCADE, null=True)
    style = models.ForeignKey(Style,related_name='style_of_content',on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

class ProjectManger(models.Model):
    admin = models.ForeignKey(UserAdmin, on_delete=models.CASCADE, null=True)
    task = models.ForeignKey(ContentCreator, on_delete=models.CASCADE, null=True)
    results=models.TextField()
    def __str__(self):
        return self.results


