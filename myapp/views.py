from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .forms import UserRegistrationForm, UserLoginForm, ExpenseDetailsForm, DepositForm
from .models import MonthlySummary, ExpenseDetails, Deposit, SocityMember, ExpenseHead, DueDeposit
from datetime import datetime
from django.views import View
from django.http import HttpResponse

# Authentication Views
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful. You are now logged in.")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('homepage')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


# Homepage Views
@login_required
def home(request):
    return render(request, 'homepage.html')


def public_home(request):
    return render(request, 'home.html')


# Member Views
def Member(request):
    members = SocityMember.objects.all()
    context = {'members': members}
    return render(request, 'member_list.html', context)


# Deposit and Expense Views
@login_required
def create_deposit(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            deposit = form.save()
            messages.success(request, 'Deposit successfully added!')
            return redirect('monthly_summary')
        else:
            messages.error(request, 'Error: Please correct the form.')
    else:
        form = DepositForm()
    return render(request, 'create_deposit.html', {'form': form})


def create_expense(request):
    if request.method == 'POST':
        form = ExpenseDetailsForm(request.POST)
        if form.is_valid():
            expense = form.save()
            return redirect('monthly_summary')
    else:
        form = ExpenseDetailsForm()
    return render(request, 'create_expense.html', {'form': form})


# Monthly Summary Views
@login_required
def monthly_summary(request, year=None, month=None):
    if year and month:
        summaries = MonthlySummary.objects.filter(month__year=year, month__month=month)
        title = f"Monthly Summary for {month}/{year}"
    else:
        summaries = MonthlySummary.objects.all()
        title = "Overall Monthly Summary"

    context = {'title': title, 'summaries': summaries}
    return render(request, 'monthly_summary.html', context)


# Category-wise Summary Views
def category_wise_summary(request):
    categories = ExpenseHead.objects.all()
    category_summary = []

    for category in categories:
        total_deposits = Deposit.objects.filter(fund_head=category).aggregate(Sum('amount'))['amount__sum'] or 0
        total_expenses = ExpenseDetails.objects.filter(ex_head=category).aggregate(Sum('amount'))['amount__sum'] or 0
        balance = total_deposits - total_expenses
        if balance != 0:
            balance += balance

        category_summary.append({
            'category_name': category.name,
            'total_deposits': total_deposits,
            'total_expenses': total_expenses,
            'balance': balance,
        })

    grand_total_deposits = sum(item['total_deposits'] for item in category_summary)
    grand_total_expenses = sum(item['total_expenses'] for item in category_summary)
    grand_balance = grand_total_deposits - grand_total_expenses

    category_summary.append({
        'category_name': 'Grand Total',
        'total_deposits': grand_total_deposits,
        'total_expenses': grand_total_expenses,
        'balance': grand_balance,
    })

    return render(request, 'cat_summary.html', {'category_summary': category_summary})


# Expense Detail Views
def DetailExpens(request):
    detailexpense = ExpenseDetails.objects.all().order_by('date')
    total_amount = detailexpense.aggregate(total=Sum('amount'))['total']

    context = {'title': 'Expense Detail', 'detailexpense': detailexpense, 'total_amount': total_amount}
    return render(request, 'exdetail.html', context)


# Fund Detail Views
def DepositDetails(request):
    contributionfund = Deposit.objects.all().order_by('date')
    total_fund = contributionfund.aggregate(total=Sum("amount"))['total']
    contributions_by_member = Deposit.objects.values('team_member__name').annotate(total_contributions=Sum('amount'))

    context = {
        'title': 'Fund Detail',
        'contributionfund': contributionfund,
        'total_fund': total_fund,
        'contributions_by_member': contributions_by_member
    }
    return render(request, 'funddetail.html', context)


# Report Views
from django.db.models import Sum, F


# def report_view(request):
#     if request.method == 'GET':
#         from_date = request.GET.get('from_date')
#         to_date = request.GET.get('to_date')
#
#         if from_date and to_date:
#             from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
#             to_date = datetime.strptime(to_date, "%Y-%m-%d").date()
#             deposits = Deposit.objects.filter(date__range=(from_date, to_date))
#         else:
#             deposits = Deposit.objects.all()
#
#         members = SocityMember.objects.all()
#         contributions = []
#
#         total_contributions = 0
#
#         for member in members:
#             total_deposits = deposits.filter(team_member=member).aggregate(Sum('amount'))['amount__sum'] or 0
#             depositbymems = deposits.filter(team_member=member)
#
#             total_contributions += total_deposits
#             total_by f"{member}" += depositbymems
#
#             contribution = {
#                 'member': member,
#                 'total_deposits': total_deposits,
#                 'depositbymems': depositbymems,
#             }
#
#             contributions.append(contribution)
#
#         return render(request, 'report.html',
#                       {'contributions': contributions, 'total_contributions': total_contributions})
#
#     return HttpResponse("Invalid request method")

# def report_view(request):
#     if request.method == 'GET':
#         from_date = request.GET.get('from_date')
#         to_date = request.GET.get('to_date')
#
#         if from_date and to_date:
#             from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
#             to_date = datetime.strptime(to_date, "%Y-%m-%d").date()
#             deposits = Deposit.objects.filter(date__range=(from_date, to_date))
#         else:
#             deposits = Deposit.objects.all()
#
#         members = SocityMember.objects.all()
#         contributions = []
#
#         total_contributions = 0
#         total_by_member = {}
#
#         for member in members:
#             total_deposits = deposits.filter(team_member=member).aggregate(Sum('amount'))['amount__sum'] or 0
#             depositbymems = deposits.filter(team_member=member)
#
#             total_contributions += total_deposits
#             total_by_member[str(member)] = depositbymems  # Using the member name as the key
#
#             contribution = {
#                 'member': member,
#                 'total_deposits': total_deposits,
#                 'depositbymems': depositbymems,
#             }
#
#             contributions.append(contribution)
#
#         return render(request, 'report.html',
#                       {'contributions': contributions, 'total_contributions': total_contributions,
#                        'total_by_member': total_by_member})
#
#     return HttpResponse("Invalid request method")

from django.shortcuts import render, get_object_or_404
from django.views import View
from django.db.models import Sum
from datetime import datetime
from .models import SocityMember, Deposit, DueDeposit

class ReportView(View):
    template_name = 'report.html'
    individual_contributions_template = 'individual_contributions.html'

    def get(self, request):
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        member_id = request.GET.get('member_id')

        if member_id:
            return self.render_individual_contributions(request, member_id)

        deposits = self.get_filtered_deposits(from_date, to_date)
        members = SocityMember.objects.all()
        total_due_amount = DueDeposit.get_total_due_amount()

        total_contributions, total_by_member, contributions = self.calculate_totals(deposits, members)

        return render(request, self.template_name, {
            'contributions': contributions,
            'total_contributions': total_contributions,
            'total_by_member': total_by_member,
            'total_due_amount': total_due_amount
        })

    def render_individual_contributions(self, request, member_id):
        member = get_object_or_404(SocityMember, id=member_id)
        deposits = Deposit.objects.filter(team_member=member)

        context = {
            'member': member,
            'deposits': deposits,
        }

        return render(request, self.individual_contributions_template, context)

    def get_filtered_deposits(self, from_date, to_date):
        deposits = Deposit.objects.all()

        if from_date and to_date:
            from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
            to_date = datetime.strptime(to_date, "%Y-%m-%d").date()
            deposits = deposits.filter(date__range=(from_date, to_date))

        return deposits

    def calculate_totals(self, deposits, members):
        total_contributions = 0
        total_by_member = {}
        contributions = []
        total_due_amount = DueDeposit.get_total_due_amount()

        for member in members:
            member_deposits = deposits.filter(team_member=member)
            total_deposits = member_deposits.aggregate(Sum('amount'))['amount__sum'] or 0

            total_contributions += total_deposits
            total_by_member[str(member)] = member_deposits

            # Calculate the due after deposit
            due_after_deposit = total_due_amount - total_deposits

            contribution = {
                'member': member,
                'total_deposits': total_deposits,
                'depositbymems': member_deposits,
                'due_after_deposit': due_after_deposit,  # Add this line
            }

            contributions.append(contribution)

        return total_contributions, total_by_member, contributions


