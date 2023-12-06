from django.db import models
from distutils.command.upload import upload

from django.contrib.auth.models import User

# Create your models here.
class Contact(models.Model):
    name=models.CharField(max_length=25)
    email=models.EmailField()
    phonenumber=models.CharField(max_length=12)
    description=models.TextField()

    def __str__(self):
        return self.email

class Enrollment(models.Model):        
    FullName=models.CharField(max_length=25)
    Email=models.EmailField()
    Gender=models.CharField(max_length=25)
    PhoneNumber=models.CharField(max_length=12)
    DOB=models.CharField(max_length=50)
    SelectMembershipplan=models.CharField(max_length=200)
    SelectTrainer=models.CharField(max_length=55)
    Reference=models.CharField(max_length=55)
    Address=models.TextField()
    paymentStatus=models.CharField(max_length=55,blank=True,null=True)
    Price=models.IntegerField(max_length=55,blank=True,null=True)
    DueDate=models.DateTimeField(blank=True,null=True)
    timeStamp=models.DateTimeField(auto_now_add=True,blank=True,)

    def __str__(self):
        return self.FullName

class Trainer(models.Model):
    name=models.CharField(max_length=55)
    gender=models.CharField(max_length=25)
    phone=models.CharField(max_length=25)
    salary=models.IntegerField(max_length=25)
    timeStamp=models.DateTimeField(auto_now_add=True,blank=True)
    img_link = models.FileField(upload_to='media/trainer',null=True)
    desc=models.TextField(null=True)
    facebook_link=models.URLField(null=True,blank=True)
    instagram_link=models.URLField(null=True,blank=True)
    def __str__(self):
        return self.name

class MembershipPlan(models.Model):
    plan=models.CharField(max_length=185)
    price=models.IntegerField(max_length=55)

    def __int__(self):
        return self.id


class Gallery(models.Model):
    title=models.CharField(max_length=100)
    img=models.ImageField(upload_to='gallery')
    timeStamp=models.DateTimeField(auto_now_add=True,blank=True)
    def __int__(self):
        return self.id


class Attendance(models.Model):
    Selectdate=models.DateTimeField(auto_now_add=True)
    phonenumber=models.CharField(max_length=15)
    Login=models.CharField(max_length=200)
    Logout=models.CharField(max_length=200)
    SelectWorkout=models.CharField(max_length=200)
    TrainedBy=models.CharField(max_length=200)
    def __int__(self):
        return self.id



class Service(models.Model):
    name = models.CharField(max_length=30)
    img_link = models.FileField(upload_to='media/service_images')
    description = models.TextField(null=True, blank=True)
    link=models.URLField(null=True,blank=True)


class Post(models.Model):
    title = models.CharField(max_length=255)
    img_link = models.FileField(upload_to='media/blog',blank=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Product(models.Model):
    img_link = models.FileField(upload_to='media/shop',blank=True)
    name = models.CharField(max_length=30)
    desc = models.TextField()
    price = models.IntegerField(default=0)

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_created=True, auto_now_add=True)
    status = models.BooleanField(default=False)
    address = models.TextField()