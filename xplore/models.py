from django.db import models

class Users(models.Model):
    username = models.CharField(max_length=50, null=True)
    password = models.CharField(max_length=65,null=True)
    email = models.CharField(max_length=100,null=True)
    accountActive = models.BooleanField(null=True)

# class Interests(models.Model):
#     topic = models.TextField(max_length=50,null=True)
#     users = models.ForeignKey(Users,on_delete=models.CASCADE)

class Course(models.Model):
    coursename = models.CharField(max_length=50,null=True)
    courseplatform = models.CharField(max_length=50,null=True)
    imageurl = models.TextField(null=True)
    courseurl = models.TextField(null=True)
    rating = models.IntegerField(null=True)
    # subscribers = models.IntegerField(null=True)
    details = models.TextField(null=True)    
    status = models.CharField(max_length=10,null=True)
