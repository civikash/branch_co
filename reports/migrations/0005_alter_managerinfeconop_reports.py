# Generated by Django 4.1.5 on 2023-06-02 09:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0004_managerinfeconop_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='managerinfeconop',
            name='reports',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reports.infeconop', verbose_name='Первый отчет'),
        ),
    ]
