from django.contrib import admin
from .models import SocityMember, MonthlySummary, ExpenseHead, ExpenseDetails, Deposit, DueDeposit

class SocityMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number')

admin.site.register(SocityMember, SocityMemberAdmin)

class MonthlySummaryAdmin(admin.ModelAdmin):
    list_display = ('month', 'total_deposits', 'total_expenses', 'balance')

admin.site.register(MonthlySummary, MonthlySummaryAdmin)

class ExpenseHeadAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(ExpenseHead, ExpenseHeadAdmin)

class ExpenseDetailsAdmin(admin.ModelAdmin):
    list_display = ('date', 'ex_detail', 'ex_head_name', 'amount')

    def ex_head_name(self, obj):
        return obj.ex_head.name

    ex_head_name.short_description = 'Expense Head'

admin.site.register(ExpenseDetails, ExpenseDetailsAdmin)

class DepositAdmin(admin.ModelAdmin):
    list_display = ('date', 'team_member', 'amount', 'fund_head_name')

    def fund_head_name(self, obj):
        return obj.fund_head.name

    fund_head_name.short_description = 'Fund Head'

admin.site.register(Deposit, DepositAdmin)
admin.site.register(DueDeposit)