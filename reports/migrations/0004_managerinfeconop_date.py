# Generated by Django 4.1.5 on 2023-06-01 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0003_alter_secondinfeconop_company_managerinfeconop'),
    ]

    operations = [
        migrations.AddField(
            model_name='managerinfeconop',
            name='date',
            field=models.DateField(auto_now=True, verbose_name='Дата'),
        ),
    ]
