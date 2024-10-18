from django.urls import path
from .views import *


urlpatterns = [
   
    path('login/', Login, name='login'),
    path('register/', Register, name='register'),
    path('logout/', Logout, name='logout'),
    path('userprofile/', Userprofile, name='Userprofile'),
    path('comp_owner/', comp_owner, name='comp_owner'),
    path('add_company/<int:id>/', add_company, name='add_company'),
    path('comp_detail/<int:id>/', comp_detail, name='comp_detail'),
    path('companies/', company_list, name='company_list'),
    path('add_account/', add_account, name='add_account'),
    path('accounts/', account_list, name='account_list'),
    path('add_employee/', add_employee, name='add_employee'),
    path('account_detail/<int:id>/', account_detail, name='account_detail'),
    path('employee_detail/<int:id>/', employee_detail, name='employee_detail'),
    path('employees/', employee_list, name='employee_list'),
    path('add_income/', add_income, name='add_income'),
    path('add_expense/<int:account_id>/', add_expense, name='add_expense'),  
    path('expense_list/<int:account_id>/', expense_list, name='expense_list'),
    path('approve_expense/<int:expense_id>/', approve_expense, name='approve_expense'),
    ##
    path('create/', create_report, name='create_report'),
    path('review/', review_reports, name='review_reports'),
    path('approve/<int:report_id>/', approve_report, name='approve_report'),
    path('reject/<int:report_id>/', reject_report, name='reject_report'),
    path('reports/', report_list , name='report_list'),
    path('reports/rejected/', rejected_reports, name='rejected_reports'),
]
