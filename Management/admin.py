from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','forget_password_token','created_at']

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name','comp_owner')
    

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('account', 'amount', 'date')
   

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('account', 'amount', 'date', 'approved')

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('company', 'name', 'balance')
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display= ('company','name', 'address','email','phone','pay')

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('company', 'data', 'date')
    

   
