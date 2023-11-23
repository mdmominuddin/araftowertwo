from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserLoginForm, ExpenseDetailsForm, DepositForm
from .models import MonthlySummary, ExpenseDetails, Deposit, SocityMember, ExpenseHead
from django.contrib import messages
from django.db.models import Sum

# Create your views here.

@login_required
def home(request):
    return render(request, 'homepage.html')

def public_home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after registration
            login(request, user)

            # Add a success message
            messages.success(request, "Registration successful. You are now logged in.")

            return redirect('login')  # Redirect to your home page
    else:
        form = UserRegistrationForm()
    return render(request, 'registration.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('homepage')  # Redirect to your home page
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout

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

def monthly_summary(request, year=None, month=None):
    if year and month:
        summaries = MonthlySummary.objects.filter(month__year=year, month__month=month)
        title = f"Monthly Summary for {month}/{year}"
    else:
        summaries = MonthlySummary.objects.all()
        title = "Overall Monthly Summary"

    context = {
        'title': title,
        'summaries': summaries,
    }

    return render(request, 'monthly_summary.html', context)

def category_wise_summary(request):
    # Get all expense categories
    categories = ExpenseHead.objects.all()

    # Initialize an empty list to store the summary data
    category_summary = []

    for category in categories:
        # Calculate total deposits for the category
        total_deposits = Deposit.objects.filter(fund_head=category).aggregate(Sum('amount'))['amount__sum'] or 0
        # Calculate total expenses for the category
        total_expenses = ExpenseDetails.objects.filter(ex_head=category).aggregate(Sum('amount'))['amount__sum'] or 0
        # Calculate balance
        balance = total_deposits - total_expenses
        if balance != 0:
            balance += balance

        # Append the category-wise summary to the list
        category_summary.append({
            'category_name': category.name,
            'total_deposits': total_deposits,
            'total_expenses': total_expenses,
            'balance': balance,
        })

    # Calculate the grand total
    grand_total_deposits = sum(item['total_deposits'] for item in category_summary)
    grand_total_expenses = sum(item['total_expenses'] for item in category_summary)
    grand_balance = grand_total_deposits - grand_total_expenses

    # Append the grand total to the category-wise summary list
    category_summary.append({
        'category_name': 'Grand Total',
        'total_deposits': grand_total_deposits,
        'total_expenses': grand_total_expenses,
        'balance': grand_balance,
    })

    return render(request, 'cat_summary.html', {'category_summary': category_summary})

def DetailExpens(request):
    detailexpense = ExpenseDetails.objects.all().order_by('date')
    total_amount = detailexpense.aggregate(total=Sum('amount'))['total']

    context = {
        'title': 'Expense Detail',
        'detailexpense': detailexpense,
        'total_amount': total_amount,
    }

    return render(request, 'exdetail.html', context)

def DepositDetails(request):
    # Get all contributions and calculate the total fund
    contributionfund = Deposit.objects.all().order_by('date')
    total_fund = contributionfund.aggregate(total=Sum("amount"))['total']

    # Get contributions grouped by members and calculate their total contributions
    contributions_by_member = Deposit.objects.values('team_member__name').annotate(total_contributions=Sum('amount'))

    context = {
        'title': 'Fund Detail',
        'contributionfund': contributionfund,
        'total_fund': total_fund,
        'contributions_by_member': contributions_by
    }
    return render(request, 'funddetail.html', context)