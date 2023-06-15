# Generated by Django 4.1.5 on 2023-06-15 13:42

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0004_remove_investitiiactive2_indicatori'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stocuri2',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('code', models.AutoField(primary_key=True, serialize=False, verbose_name='Code')),
                ('counter', models.IntegerField(default=0, verbose_name='Counter')),
                ('code_rind', models.IntegerField(blank=True, null=True, verbose_name='cod_rind')),
                ('indicatorii', models.IntegerField(blank=True, null=True, verbose_name='Indicatorii')),
                ('trimestrul', models.CharField(blank=True, max_length=120, null=True, verbose_name='Trimestrul')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='account_company_stocuri_2', to='reports.companydata', verbose_name='Company')),
            ],
        ),
        migrations.CreateModel(
            name='Stocuri1',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('code', models.AutoField(primary_key=True, serialize=False, verbose_name='Code')),
                ('counter', models.IntegerField(default=0, verbose_name='Counter')),
                ('code_rind', models.IntegerField(blank=True, null=True, verbose_name='cod_rind')),
                ('indicatori', models.CharField(blank=True, max_length=120, null=True, verbose_name='Indicatorii')),
                ('inceputul', models.DecimalField(decimal_places=1, max_digits=10, null=True)),
                ('finele', models.DecimalField(decimal_places=1, max_digits=10, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='account_company_stocuri', to='reports.companydata', verbose_name='Company')),
            ],
        ),
        migrations.CreateModel(
            name='ManagerRaportStocuri',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('date', models.DateField(auto_now=True, verbose_name='Дата')),
                ('ci_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.stocuri1', verbose_name='Cap.Stoc: Stocuri')),
                ('ci_2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reports.stocuri2', verbose_name='Venituri, costuri și cheltuieli operaționale în total pe entitate')),
            ],
        ),
    ]
