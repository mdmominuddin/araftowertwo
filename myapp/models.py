from django.db import models
from datetime import date
from datetime import datetime
from django.contrib.auth.models import User

class Socity_member(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)

    # Add other relevant fields for team members.
    def __str__(self):
        return self.name


class MonthlySummary(models.Model):
    month = models.DateField(default=date.today, unique=True)
    total_deposits = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_expenses = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.month


class Expense_head(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
    # You can add more fields for description, sub-categories, etc.


class Expense_details(models.Model):
    # Other fields
    date = models.DateField()
    expensedetail = models.CharField(max_length=200)
    category = models.ForeignKey(Expense_head, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update the corresponding MonthlySummary
        summary, created = MonthlySummary.objects.get_or_create(month=self.date.replace(day=1))
        summary.total_expenses += self.amount
        summary.balance -= self.amount
        summary.save()

        def __str__(self):
            return f"{self.category.name} - {self.date.strftime('%d-%m-%Y')}"


class Deposit(models.Model):
    # Other fields
    date = models.DateField()
    team_member = models.ForeignKey(Socity_member, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Expense_head, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update the corresponding MonthlySummary
        summary, created = MonthlySummary.objects.get_or_create(month=self.date.replace(day=1))
        summary.total_deposits += self.amount
        summary.balance += self.amount
        summary.save()

    def __str__(self):
        return f"{self.team_member.name} - {self.date.strftime('%d-%m-%Y')}"






