# Generated by Django 4.1.5 on 2023-06-01 12:45

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportItems3',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('code', models.AutoField(primary_key=True, serialize=False, verbose_name='Code')),
                ('n_year', models.DecimalField(decimal_places=1, max_digits=10, null=True)),
                ('n_1_year', models.DecimalField(decimal_places=1, max_digits=10, null=True)),
                ('perc', models.IntegerField(verbose_name='Perc')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_report_items_3', to='reports.companydata', verbose_name='Company')),
            ],
        ),
        migrations.CreateModel(
            name='ReportItems2',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('code', models.AutoField(primary_key=True, serialize=False, verbose_name='Code')),
                ('d_t_ini', models.DecimalField(decimal_places=1, max_digits=10, null=True)),
                ('c_t_ini', models.DecimalField(decimal_places=1, max_digits=10, null=True)),
                ('calculat', models.DecimalField(decimal_places=1, max_digits=10, null=True)),
                ('transferat', models.DecimalField(decimal_places=1, max_digits=10, null=True)),
                ('d_t_fin', models.DecimalField(decimal_places=1, max_digits=10, null=True)),
                ('c_t_fin', models.DecimalField(decimal_places=1, max_digits=10, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_report_items_2', to='reports.companydata', verbose_name='Company')),
            ],
        ),
        migrations.CreateModel(
            name='ReportItems1',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('code', models.AutoField(primary_key=True, serialize=False, verbose_name='Code')),
                ('prejud', models.DecimalField(decimal_places=1, max_digits=10, null=True)),
                ('sup_10', models.DecimalField(decimal_places=1, max_digits=10, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_report_items_1', to='reports.companydata', verbose_name='Company')),
            ],
        ),
        migrations.CreateModel(
            name='ReportHeader',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('code', models.AutoField(primary_key=True, serialize=False, verbose_name='Code')),
                ('associat', models.BooleanField(verbose_name='Associat')),
                ('fondul', models.BooleanField(verbose_name='Associat')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_report_header', to='reports.companydata', verbose_name='Company')),
            ],
        ),
        migrations.CreateModel(
            name='VolVanzAmauntul',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('code', models.AutoField(primary_key=True, serialize=False, verbose_name='Code')),
                ('counter', models.IntegerField(default=0, verbose_name='Counter')),
                ('name', models.CharField(max_length=150, null=True, verbose_name='Denumirea')),
                ('n_year', models.IntegerField(blank=True, null=True, verbose_name='Year')),
                ('n_month', models.IntegerField(blank=True, null=True, verbose_name='Month')),
                ('prec', models.DecimalField(decimal_places=1, max_digits=10, null=True)),
                ('cur', models.DecimalField(decimal_places=1, max_digits=10, null=True)),
                ('percentage', models.DecimalField(decimal_places=1, max_digits=10, null=True)),
                ('pond_prec', models.DecimalField(decimal_places=1, max_digits=10, null=True)),
                ('pond_cur', models.DecimalField(decimal_places=1, max_digits=10, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_volvanz', to='reports.companydata', verbose_name='Company')),
            ],
            options={
                'unique_together': {('code', 'counter')},
            },
        ),
    ]