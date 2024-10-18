from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User, on_delete= models.CASCADE)
    forget_password_token=models.CharField(max_length=100)
    created_at =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
class Company(models.Model):
    name = models.CharField(max_length=255)
    comp_owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Account(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=10, decimal_places=3)

class Employee(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    pay = models.IntegerField()
    

class Income(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=3)
    date = models.DateField(auto_now_add=True)

class Expense(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=10, decimal_places=3)
    date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

class Report(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    date = models.DateField()
    data = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending') 

   