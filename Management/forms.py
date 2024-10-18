from django import forms
from .models import Account, Employee, Income, Expense,Company, Report

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('company','name', 'balance')

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('company','name', 'address','email','phone','pay')

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name','comp_owner']


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['account', 'amount']

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['account', 'amount','approved']
class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['company', 'date', 'data']