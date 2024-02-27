from django.db import models

class Student(models.Model):
    roll_no = models.IntegerField()
    fname = models.CharField(max_length = 45)
    lname = models.CharField(max_length = 45)
    emil = models.EmailField()
    address = models.TextField()
