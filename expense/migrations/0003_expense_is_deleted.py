# Generated by Django 5.1.1 on 2024-10-21 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0002_delete_income_alter_expense_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
