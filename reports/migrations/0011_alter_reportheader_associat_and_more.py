# Generated by Django 4.1.5 on 2023-06-03 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0010_alter_reportheader_associat_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportheader',
            name='associat',
            field=models.BooleanField(default=False, null=True, verbose_name='Associat'),
        ),
        migrations.AlterField(
            model_name='reportheader',
            name='fondul',
            field=models.BooleanField(default=False, null=True, verbose_name='Fondul'),
        ),
    ]