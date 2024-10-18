from django.http import HttpResponseForbidden
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User, Profile
from .forms import *
from . models import *

import uuid

# Login view
def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, 'Both Username and Password are required')
            return redirect('login')

        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
        
        login(request, user)
        print('login successful')
        return redirect('Userprofile')

    return render(request, 'login.html')

# Register view
def Register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is taken.')
            return redirect('/register/')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is taken.')
            return redirect('/register/')

        user_obj = User.objects.create_user(username=username, email=email, password=password)
        Profile.objects.create(user=user_obj)

        messages.success(request, 'Registration successful. Please log in.')
        return redirect('/login/')

    return render(request, 'register.html')

# Logout view
def Logout(request):
    logout(request)
    return redirect('Userprofile')


@login_required
def Userprofile(request):
    user = request.user  
    print(user.username)
    obj = Company.objects.filter(comp_owner=user)
    print("Retrieved companies:", obj)
    context = {
        'obj': obj,
        'user': user
    }
    return render(request, 'show_profile.html', context)


@login_required
def comp_owner(request):
    user = request.user
    if user:
        messages.error(request, 'Only add a new Company!')
        return redirect('Userprofile')
    obj = User.objects.all()
    context = {
        'obj': obj,
        'user': user
    }
    return render(request, 'owner.html', context)

@login_required

def add_company(request, id):
    try:
        user = User.objects.get(id=id)  
    except User.DoesNotExist:
        messages.error(request, 'User does not exist.')
        return redirect('Userprofile')

    
    if  request.user.is_superuser:
        messages.error(request, 'admin cannot add companies for themselves.')
        return redirect('Userprofile')

    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.comp_owner = user 
            obj.save()
            messages.success(request, 'Company added successfully.')
            return redirect('Userprofile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CompanyForm()

    return render(request, 'add_company.html', {'form': form, 'user': user})

@login_required
def comp_detail(request, id):
    company = get_object_or_404(Company, id=id)

    if request.user.is_superuser or company.comp_owner == request.user:
        accounts = Account.objects.filter(company=company)
        employees = Employee.objects.filter(company=company)  
        return render(request, 'company_detail.html', {
            'company': company,
            'accounts': accounts,
            'employees': employees  
        })
    else:
        return HttpResponseForbidden("You are not authorized to view this page.")

    



@login_required
def company_list(request):
    if request.user.is_superuser:
        
        companies = Company.objects.all()
    elif request.user.is_authenticated:
        
        companies = Company.objects.filter(comp_owner=request.user)
    else:
       
        return HttpResponseForbidden("You are not authorized to view this page.")

    return render(request, 'company_list.html', {'companies': companies})
  
@login_required
def add_account(request):
    if  request.user.is_superuser:
        messages.error(request, 'You are admin')
        return redirect('Userprofile')
    company = Company.objects.filter(comp_owner=request.user).first()
    if company and request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.company = company
            account.save()
            return redirect('comp_detail', account.company.id)
    else:
        form = AccountForm()

    return render(request, 'add_account.html', {'form': form, 'company': company})



@login_required
def account_list(request):
    if request.user.is_superuser:
        accounts = Account.objects.all()
        companies = Company.objects.all()  
    else:
        accounts = Account.objects.filter(company__comp_owner=request.user)
        companies = Company.objects.filter(comp_owner=request.user) 

    return render(request, 'account_list.html', {'accounts': accounts, 'companies': companies})

@login_required
def account_detail(request, id):
    account = get_object_or_404(Account, id=id)
    if request.user.is_superuser or account.company.comp_owner == request.user:
        incomes = Income.objects.filter(account=account)
        company = account.company 
        expenses = Expense.objects.filter(account=account).order_by('-date') 
        approved_reports = Report.objects.filter(status='approved', owner=request.user)
        return render(request, 'account_detail.html', {'account': account,'incomes': incomes,'company': company,'expenses': expenses,'approved_reports': approved_reports})
    else:
        return HttpResponseForbidden("You are not authorized to view this page.")

    

@login_required
def add_employee(request):
    if request.user.is_superuser:
        messages.error(request, 'You are admin')
        return redirect('Userprofile')
    
    company = Company.objects.filter(comp_owner=request.user).first()
    
    if company and request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.company = company
            employee.save()
            messages.success(request, 'Employee added successfully.')
            return redirect('comp_detail', company.id)
    else:
        form = EmployeeForm()

    return render(request, 'add_employee.html', {'form': form, 'company': company})


@login_required
def employee_detail(request, id):
    employee = get_object_or_404(Employee, id=id)

    
    company = employee.company

    return render(request, 'employee_detail.html', {'employee': employee, 'company': company})

    
@login_required
def employee_list(request):
    if request.user.is_superuser:
        employees = Employee.objects.all()
        company = None  
    else:
        employees = Employee.objects.filter(company__comp_owner=request.user)
        company = employees.first().company if employees.exists() else None

    return render(request, 'employee_list.html', {'employees': employees, 'company': company})

@login_required
def add_income(request):
    if not request.user.is_superuser:
        messages.error(request, 'You are user')
        return redirect('Userprofile')
    company = Company.objects.filter(comp_owner=request.user).first()
    account = Account.objects.filter(company=company).first()
    
    
    if account and request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            acount = form.save(commit=False)
            acount.account =  account
            acount.save()
            return redirect('account_detail', id=account.id)
    else:
        form = IncomeForm()

    return render(request,  'add_income.html',  {'form': form,'account':account})



@login_required
def add_expense(request,account_id):
    account = get_object_or_404(Account, id=account_id)
    
    if request.user.is_superuser:
        messages.error(request, 'You are admin')
        return redirect('Userprofile')

    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.account = account
            expense.approved = False 
            expense.save()

            messages.success(request, f'Expense of {expense.amount} has been added and awaits approval!')
            return redirect('expense_list', account_id=account.id)   
        else:
            print(form.errors) 
    else:
        form = ExpenseForm()
    
    return render(request, 'add_expense.html', {'form': form, 'account': account})



@login_required
def expense_list(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    
    
    expenses = Expense.objects.filter(account=account).order_by('-date')  
    print("Expenses:", expenses)
    return render(request, 'expense_list.html', {'account': account, 'expenses': expenses})

@login_required
def approve_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)

 
    # if expense.account.company.comp_owner != request.user: 
    #     messages.error(request, 'You do not have permission to approve this expense.')
    #     return redirect('expense_list', account_id=expense.account.id)
    if not request.user.is_superuser: 
        messages.error(request, 'You do not have permission to approve this expense.')
        return redirect('expense_list', account_id=expense.account.id)

    if request.method == 'POST':
        if 'approve' in request.POST:
            expense.approved = True
            messages.success(request, f'Expense of {expense.amount} has been approved!')
        elif 'reject' in request.POST:
            expense.approved = False
            messages.error(request, f'Expense of {expense.amount} has been rejected.')

        expense.save()
        return redirect('expense_list', account_id=expense.account.id)

    return render(request, 'approve_expense.html', {'expense': expense})


@login_required
def create_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.owner = request.user 
            report.save()
            
            return redirect('report_list')  
    else:
        form = ReportForm()
    return render(request, 'create_report.html', {'form': form})

def review_reports(request):
    reports = Report.objects.filter(status='pending')
    return render(request, 'review_reports.html', {'reports': reports})


def approve_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    report.status = 'approved'
    report.save()
   
    return redirect('review_reports')

@login_required
def rejected_reports(request):
    rejected_reports = Report.objects.filter(status='rejected')
    return render(request, 'rejected_reports.html', {'reports': rejected_reports})

def reject_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    report.status = 'rejected'
    report.save()
    
    return redirect('review_reports')

@login_required
def report_list(request):
    approved_reports = Report.objects.filter(status='approved', owner=request.user)
    return render(request, 'report_list.html', {'reports': approved_reports})
