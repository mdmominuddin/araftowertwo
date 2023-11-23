from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import ExpenseDetails, Deposit

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        help_text="Required. Enter a valid email address."
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class ExpenseDetailsForm(forms.ModelForm):
    class Meta:
        model = ExpenseDetails
        fields = ['date', 'ex_detail', 'ex_head', 'amount', 'remark']

    def __init__(self, *args, **kwargs):
        super(ExpenseDetailsForm, self).__init__(*args, **kwargs)
        # You can customize the form widget or add additional logic if needed.

class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = ['date', 'team_member', 'amount', 'fund_head', 'remark']

    def __init__(self, *args, **kwargs):
        super(DepositForm, self).__init__(*args, **kwargs)
        # You can customize the form widget or add additional logic if needed.
