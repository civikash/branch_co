# Generated by Django 4.1.5 on 2023-06-20 21:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyData',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=150, verbose_name='Denumirea')),
                ('address', models.CharField(max_length=150, verbose_name='Adresa')),
                ('district', models.CharField(max_length=74, verbose_name='Raionul')),
                ('village', models.CharField(max_length=55, verbose_name='Satul')),
                ('street', models.CharField(max_length=155, verbose_name='Strada')),
                ('code_cuiio', models.IntegerField()),
                ('code_idno', models.IntegerField()),
                ('ruler', models.CharField(max_length=150, verbose_name='Conducătorul')),
                ('accountant', models.CharField(max_length=150, verbose_name='Contabil')),
                ('executor', models.CharField(max_length=150, verbose_name='Executantul')),
                ('tel', models.CharField(max_length=15, verbose_name='Tel')),
                ('anul', models.CharField(max_length=5, verbose_name='Anul')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
        migrations.CreateModel(
            name='InfEconOp',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('code', models.AutoField(primary_key=True, serialize=False, verbose_name='Code')),
                ('counter', models.IntegerField(default=0, verbose_name='Counter')),
                ('n_year', models.IntegerField(blank=True, null=True, verbose_name='Year')),
                ('n_month', models.IntegerField(blank=True, null=True, verbose_name='Month')),
                ('before_year', models.IntegerField(blank=True, null=True, verbose_name='Before Year')),
                ('before_month', models.IntegerField(blank=True, null=True, verbose_name='Before Month')),
                ('n_beforeTotal', models.DecimalField(decimal_places=1, max_digits=10, null=True)),
                ('n_beforeLunar', models.DecimalField(decimal_places=1, max_digits=10, null=True)),
                ('n_total', models.DecimalField(decimal_places=1, max_digits=10, null=True)),
                ('n_lunar', models.DecimalField(decimal_places=1, max_digits=10, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='account_company', to='reports.companydata', verbose_name='Company')),
            ],
            options={
                'unique_together': {('code', 'counter')},
            },
        ),
        migrations.CreateModel(
            name='InvestitiiActive1',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('code', models.AutoField(primary_key=True, serialize=False, verbose_name='Code')),
                ('counter', models.IntegerField(default=0, verbose_name='Counter')),
                ('codul_rind', models.IntegerField(blank=True, null=True, verbose_name='Codul_rînd')),
                ('indicatori', models.CharField(blank=True, max_length=120, null=True, verbose_name='Indicatorii')),
                ('intrari', models.DecimalField(decimal_places=1, max_digits=10, null=True)),
                ('investitii', models.DecimalField(decimal_places=1, max_digits=10, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='account_company_investitii', to='reports.companydata', verbose_name='Company')),
            ],
        ),
        migrations.CreateModel(
            name='InvestitiiActive2',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('code', models.AutoField(primary_key=True, serialize=False, verbose_name='Code')),
                ('counter', models.IntegerField(default=0, verbose_name='Counter')),
                ('codul_rind', models.IntegerField(blank=True, null=True, verbose_name='Codul_rînd')),
                ('code_cuatm', models.IntegerField(blank=True, null=True, verbose_name='CodCUATM')),
                ('numa_oras', models.CharField(blank=True, max_length=120, null=True, verbose_name='Numa_oras')),
                ('cladiri', models.DecimalField(decimal_places=1, max_digits=10, null=True)),
                ('apart', models.DecimalField(decimal_places=1, max_digits=10, null=True)),
                ('sup_total', models.DecimalField(decimal_places=1, max_digits=10, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='account_company_investitii_2', to='reports.companydata', verbose_name='Company')),
            ],
        ),
        migrations.CreateModel(
            name='Stocuri2',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('code', models.AutoField(primary_key=True, serialize=False, verbose_name='Code')),
                ('counter', models.IntegerField(default=0, verbose_name='Counter')),
                ('code_rind', models.IntegerField(blank=True, null=True, verbose_name='cod_rind')),
                ('indicatorii', models.CharField(blank=True, max_length=520, null=True, verbose_name='Indicatorii')),
                ('trimestrul', models.DecimalField(blank=True, decimal_places=1, max_digits=10, null=True, verbose_name='Trimestrul')),
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
            name='SecondInfEconOp',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('code', models.AutoField(primary_key=True, serialize=False, verbose_name='Code')),
                ('counter', models.IntegerField(default=0, verbose_name='Counter')),
                ('name', models.CharField(max_length=150, null=True, verbose_name='Denumirea')),
                ('n_year', models.IntegerField(blank=True, null=True, verbose_name='Year')),
                ('n_month', models.IntegerField(blank=True, null=True, verbose_name='Month')),
                ('before_year', models.IntegerField(blank=True, null=True, verbose_name='Before Year')),
                ('before_month', models.IntegerField(blank=True, null=True, verbose_name='Before Month')),
                ('n_beforeTotal', models.DecimalField(decimal_places=1, max_digits=10, null=True)),
                ('n_beforeLunar', models.DecimalField(decimal_places=1, max_digits=10, null=True)),
                ('n_total', models.DecimalField(decimal_places=1, max_digits=10, null=True)),
                ('n_lunar', models.DecimalField(decimal_places=1, max_digits=10, null=True)),
                ('n_beforeMarfa', models.DecimalField(decimal_places=1, max_digits=10, null=True)),
                ('n_Marfa', models.DecimalField(decimal_places=1, max_digits=10, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='company', to='reports.companydata', verbose_name='Company')),
            ],
            options={
                'unique_together': {('code', 'counter')},
            },
        ),
        migrations.CreateModel(
            name='ReportItems3',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('counter', models.IntegerField(default=0, verbose_name='Counter')),
                ('code', models.AutoField(primary_key=True, serialize=False, verbose_name='Code')),
                ('n_year', models.DecimalField(decimal_places=1, max_digits=10, null=True)),
                ('n_1_year', models.DecimalField(decimal_places=1, max_digits=10, null=True)),
                ('perc', models.IntegerField(null=True, verbose_name='Perc')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_report_items_3', to='reports.companydata', verbose_name='Company')),
            ],
        ),
        migrations.CreateModel(
            name='ReportItems2',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('counter', models.IntegerField(default=0, verbose_name='Counter')),
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
                ('counter', models.IntegerField(default=0, verbose_name='Counter')),
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
                ('counter', models.IntegerField(default=0, verbose_name='Counter')),
                ('code', models.AutoField(primary_key=True, serialize=False, verbose_name='Code')),
                ('associat', models.DecimalField(decimal_places=1, max_digits=10, null=True)),
                ('fondul', models.DecimalField(decimal_places=1, max_digits=10, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_report_header', to='reports.companydata', verbose_name='Company')),
            ],
        ),
        migrations.CreateModel(
            name='MiscCadrelor',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('counter', models.IntegerField(default=0, verbose_name='Counter')),
                ('code', models.AutoField(primary_key=True, serialize=False, verbose_name='Code')),
                ('codul_rind', models.IntegerField(blank=True, null=True, verbose_name='Codul rînd')),
                ('category', models.IntegerField(blank=True, null=True, verbose_name='Categorii')),
                ('num_func', models.IntegerField(blank=True, null=True, verbose_name='Num func')),
                ('num_script', models.IntegerField(blank=True, null=True, verbose_name='Num scriptic')),
                ('num_locuri', models.IntegerField(blank=True, null=True, verbose_name='Num locuri')),
                ('sal_pana', models.IntegerField(blank=True, null=True, verbose_name='Sal pana la 30 ani')),
                ('studii_super', models.IntegerField(blank=True, null=True, verbose_name='Studii Superioare')),
                ('studii_medii_speciale', models.IntegerField(blank=True, null=True, verbose_name='Studii medii speciale')),
                ('studii_medii', models.IntegerField(blank=True, null=True, verbose_name='Studii medii')),
                ('absolventi', models.IntegerField(blank=True, null=True, verbose_name='Absolventi')),
                ('mai_ani', models.IntegerField(blank=True, null=True, verbose_name='mai mare 5 ani')),
                ('mai_ani_consum', models.IntegerField(blank=True, null=True, verbose_name='mai mare 5 ani consum')),
                ('perfectionare', models.IntegerField(blank=True, null=True, verbose_name='Perfectionare a cadrelor')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='misc_cadrelor', to='reports.companydata', verbose_name='Company')),
            ],
        ),
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
        migrations.CreateModel(
            name='ManagerRaportStocuri',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('date', models.DateField(auto_now=True, verbose_name='Дата')),
                ('ci_2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reports.stocuri2', verbose_name='Venituri, costuri și cheltuieli operaționale în total pe entitate')),
                ('reports', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.stocuri1', verbose_name='Cap.Stoc: Stocuri')),
            ],
        ),
        migrations.CreateModel(
            name='ManagerRaportStatisticTrimestrial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('date', models.DateField(auto_now=True, verbose_name='Дата')),
                ('reports', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.investitiiactive1', verbose_name='Investiţii în active imobilizate')),
                ('reports_2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reports.investitiiactive2', verbose_name='Clădiri rezidenţiale (de locuit)')),
            ],
        ),
        migrations.CreateModel(
            name='ManagerMiscCadrelor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('date', models.DateField(auto_now=True, verbose_name='Дата')),
                ('reports', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.misccadrelor', verbose_name='MiscCadrelor')),
            ],
        ),
        migrations.CreateModel(
            name='ManagerInfEconOp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('date', models.DateField(auto_now=True, verbose_name='Дата')),
                ('reports', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.infeconop', verbose_name='Первый отчет')),
                ('reports_second', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reports.secondinfeconop', verbose_name='Вторая часть')),
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
