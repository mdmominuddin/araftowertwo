from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Socity_member, MonthlySummary, Expense_head, Expense_details, Deposit

class SocityMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number')

admin.site.register(Socity_member, SocityMemberAdmin)

class MonthlySummaryAdmin(admin.ModelAdmin):
    list_display = ('month', 'total_deposits', 'total_expenses', 'balance')

admin.site.register(MonthlySummary, MonthlySummaryAdmin)

class ExpenseHeadAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Expense_head, ExpenseHeadAdmin)

class ExpenseDetailsAdmin(admin.ModelAdmin):
    list_display = ('date', 'expensedetail', 'category', 'amount')

admin.site.register(Expense_details, ExpenseDetailsAdmin)

class DepositAdmin(admin.ModelAdmin):
    list_display = ('date', 'team_member', 'amount', 'category')

admin.site.register(Deposit, DepositAdmin)
