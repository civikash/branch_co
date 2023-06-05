# Generated by Django 4.1.5 on 2023-06-03 18:17

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0007_managerinfeconop_reports_second'),
    ]

    operations = [
        migrations.CreateModel(
            name='ManagerReportDescriereaAsociati',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('date', models.DateField(auto_now=True, verbose_name='Дата')),
                ('report_item_1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reports.reportitems1', verbose_name='Вторая часть')),
                ('report_item_2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reports.reportitems2', verbose_name='Вторая часть')),
                ('report_item_3', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reports.reportitems3', verbose_name='Вторая часть')),
                ('reports', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.reportheader', verbose_name='Головная часть')),
            ],
        ),
    ]
