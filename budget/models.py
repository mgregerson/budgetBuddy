from django.db import models
from django.utils.text import slugify
from .choices import INCOME_FREQUENCY_CHOICES, CURRENCY_CHOICES

from user.models import CustomUser

class Project(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='projects')
    budget = models.IntegerField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Project, self).save(*args, **kwargs)

    def budget_left(self):
        expense_list = Expense.objects.filter(project=self)
        income_list = Income.objects.filter(project=self)

        total_expense_amount = 0

        for expense in expense_list:
            total_expense_amount += expense.amount

        for income in income_list:
            total_expense_amount -= income.amount

        return self.budget - total_expense_amount

    def total_transactions(self):
        expense_list = Expense.objects.filter(project=self)
        income_list = Income.objects.filter(project=self)
        return len(expense_list) + len(income_list)
    
class Account(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD', choices=CURRENCY_CHOICES)
    account_number = models.CharField(max_length=50, blank=True)
    routing_number = models.CharField(max_length=50, blank=True)
    institution = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='accounts')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Account, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Category(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50)
    
class Expense(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='expenses')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='expenses', null=True)
    title = models.CharField(max_length = 100)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateField(null=True)

    class Meta:
        ordering = ('-amount',)
    
class Income(models.Model):
    date = models.DateField()
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    source = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='income_sources', null=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='income_sources', null=True)

    class Meta:
        ordering = ('-amount',)

# class Goal(models.Model):
#     account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="goals")
#     end_date = models.DateField()
#     target_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     achieved = models.BooleanField(default=False)

    
    