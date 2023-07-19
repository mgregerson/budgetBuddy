from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import CreateView
from django.utils.text import slugify

from .models import Project, Category, Expense, Income, Account
from .forms import ExpenseForm, IncomeForm

import json

def project_list(request):
    project_list = Project.objects.all()
    
    return render(request, 'budget/project-list.html', {'project_list': project_list})

def account_list(request):
    account_list = Account.objects.all()

    return render(request, 'account/account-list.html', {'account_list': account_list})

def account_detail(request, account_slug):
    account = get_object_or_404(Account, slug=account_slug)
    expense_form = ExpenseForm()
    income_form = IncomeForm()
    
    if request.method == 'GET':
        return render(request, 'account/account-detail.html', {
            'account': account,
            'expense_list': account.expenses.all(),
            'income_list': account.income_sources.all()
        })
    elif request.method == 'POST':
        if 'expense_submit' in request.POST:
            expense_form = ExpenseForm(request.POST)
            if expense_form.is_valid():
                date = expense_form.cleaned_data['date']
                title = expense_form.cleaned_data['title']
                amount = expense_form.cleaned_data['amount']
                category_name = expense_form.cleaned_data['category']

                category = get_object_or_404(Category, account=account, name=category_name)

                Expense.objects.create(
                  account=account,
                  date=date,
                  title=title,
                  amount=amount,
                  category=category
              ).save()
    elif 'income_submit' in request.POST:
          income_form = IncomeForm(request.POST)
          if income_form.is_valid():
              date = income_form.cleaned_data['date']
              description = income_form.cleaned_data['description']
              amount = income_form.cleaned_data['amount']
              source = income_form.cleaned_data['source']

              Income.objects.create(
                  account=account,
                  date=date,
                  description=description,
                  amount=amount,
                  source=source,
              ).save()
    elif request.method == 'DELETE':
        data = json.loads(request.body)
        item_id = data['id']
        item_type = data['type']

        if item_type == 'expense':
            expense = get_object_or_404(Expense, id=item_id)
            expense.delete()
        elif item_type == 'income':
            income = get_object_or_404(Income, id=item_id)
            income.delete()
        return HttpResponse('')

    return HttpResponseRedirect(account_slug)

def project_detail(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug)
    expense_form = ExpenseForm()
    income_form = IncomeForm()

    if request.method == 'GET':
        category_list = Category.objects.filter(project=project)
        return render(request, 'budget/project-detail.html', {
            'project': project, 
            'expense_list': project.expenses.all(), 
            'income_list': project.income_sources.all(), 
            'category_list': category_list
          })
    
    elif request.method == 'POST':
      if 'expense_submit' in request.POST:
          print('GOT HERE BABY')
          expense_form = ExpenseForm(request.POST)
          if expense_form.is_valid():
              date = expense_form.cleaned_data['date']
              title = expense_form.cleaned_data['title']
              amount = expense_form.cleaned_data['amount']
              category_name = expense_form.cleaned_data['category']

              category = get_object_or_404(Category, project=project, name=category_name)

              Expense.objects.create(
                  project=project,
                  date=date,
                  title=title,
                  amount=amount,
                  category=category
              ).save()
      elif 'income_submit' in request.POST:
          income_form = IncomeForm(request.POST)
          if income_form.is_valid():
              date = income_form.cleaned_data['date']
              description = income_form.cleaned_data['description']
              amount = income_form.cleaned_data['amount']
              source = income_form.cleaned_data['source']

              Income.objects.create(
                  project=project,
                  date=date,
                  description=description,
                  amount=amount,
                  source=source,
              ).save()

    elif request.method == 'DELETE':
        data = json.loads(request.body)
        item_id = data['id']
        item_type = data['type']

        if item_type == 'expense':
            expense = get_object_or_404(Expense, id=item_id)
            expense.delete()
        elif item_type == 'income':
            income = get_object_or_404(Income, id=item_id)
            income.delete()

        return HttpResponse('')

    return HttpResponseRedirect(project_slug)
    
class ProjectCreateView(CreateView):
    model = Project
    template_name = 'budget/add-project.html'
    fields = ('name', 'budget')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()

        categories = self.request.POST['categoriesString'].split(',')
        for category in categories:
            Category.objects.create(
                project=Project.objects.get(id=self.object.id),
                name=category
            ).save()

        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return slugify(self.request.POST['name'])
    
class AccountCreateView(CreateView):
    model = Account
    template_name = 'account/add-account.html'
    fields = ('name', 'balance', 'currency', 'account_number', 'routing_number', 'institution', 'description')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()

        return HttpResponseRedirect(f"accounts/{self.get_success_url()}")
    
    def get_success_url(self):
        return slugify(self.request.POST['name'])