# Generated by Django 4.2.3 on 2023-07-20 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency', models.CharField(choices=[('USD', 'United States Dollar'), ('EUR', 'Euro'), ('JPY', 'Japanese Yen'), ('GBP', 'British Pound Sterling'), ('AUD', 'Australian Dollar'), ('CAD', 'Canadian Dollar'), ('CHF', 'Swiss Franc'), ('CNY', 'Chinese Yuan'), ('SEK', 'Swedish Krona'), ('NZD', 'New Zealand Dollar'), ('MXN', 'Mexican Peso'), ('SGD', 'Singapore Dollar'), ('HKD', 'Hong Kong Dollar'), ('NOK', 'Norwegian Krone'), ('KRW', 'South Korean Won'), ('TRY', 'Turkish Lira'), ('RUB', 'Russian Ruble'), ('INR', 'Indian Rupee'), ('BRL', 'Brazilian Real'), ('ZAR', 'South African Rand')], default='USD', max_length=3)),
                ('account_number', models.CharField(blank=True, max_length=50)),
                ('routing_number', models.CharField(blank=True, max_length=50)),
                ('institution', models.CharField(blank=True, max_length=100)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('date', models.DateField(null=True)),
            ],
            options={
                'ordering': ('-amount',),
            },
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('description', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('source', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ('-amount',),
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, max_length=100, unique=True)),
                ('budget', models.IntegerField()),
            ],
        ),
    ]
