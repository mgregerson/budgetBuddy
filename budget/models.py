from django.db import models
from django.utils.text import slugify
from .choices import INCOME_FREQUENCY_CHOICES

class Project(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
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
        return len(expense_list)

class Category(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

class Expense(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='expenses')
    title = models.CharField(max_length = 100)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-amount',)

class Income(models.Model):
    date = models.DateField()
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    source = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='income_sources')

    class Meta:
        ordering = ('-amount',)