# Generated by Django 4.1.5 on 2023-06-14 09:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0003_alter_managerraportstatistictrimestrial_reports_2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='investitiiactive2',
            name='indicatori',
        ),
    ]
