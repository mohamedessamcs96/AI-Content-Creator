from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from django.contrib.auth.hashers import make_password
from datetime import datetime,timedelta

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
    is_upgraded = models.BooleanField(default=False)
    last_execution_time = models.DateTimeField(default=datetime.now().date() - timedelta(days=8))
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


from django.dispatch import receiver
from django.db.models.signals import post_save
class UserPayment(models.Model):
    app_user=models.ForeignKey(UserAdmin,on_delete=models.CASCADE)
    payment_bool=models.BooleanField(default=False)
    stripe_checkout_id=models.CharField(max_length=500)


@receiver(post_save,sender=UserAdmin)
def create_user_payment(sender,instance,created,**kwargs):
    if created:UserPayment.objects.create(app_user=instance)




# class Plans(models.Model):
#     admin = models.ForeignKey(UserAdmin, on_delete=models.CASCADE, null=True)
#     monthly=models.IntegerField(default=0)
#     yearly=models.IntegerField(default=0)


# class Product(models.Model):
#     name = models.CharField(max_length=100)
#     stripe_product_id = models.CharField(max_length=100)
    
#     def __str__(self):
#         return self.name
    
 
# class Price(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     stripe_price_id = models.CharField(max_length=100)
#     price = models.IntegerField(default=0)  # cents
    
#     def get_display_price(self):
#         return "{0:.2f}".format(self.price / 100)