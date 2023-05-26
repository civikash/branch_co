# Generated by Django 4.1.5 on 2023-05-04 09:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SecondInfEconOp',
            fields=[
                ('code', models.AutoField(primary_key=True, serialize=False, verbose_name='Code')),
                ('counter', models.IntegerField(default=0, verbose_name='Counter')),
                ('name', models.CharField(max_length=150, verbose_name='Denumirea')),
                ('n_year', models.IntegerField(blank=True, null=True, verbose_name='Year')),
                ('n_month', models.IntegerField(blank=True, null=True, verbose_name='Month')),
                ('n_beforeTotal', models.DecimalField(decimal_places=1, max_digits=10, null=True)),
                ('n_beforeLunar', models.DecimalField(decimal_places=1, max_digits=10, null=True)),
                ('n_total', models.DecimalField(decimal_places=1, max_digits=10, null=True)),
                ('n_lunar', models.DecimalField(decimal_places=1, max_digits=10, null=True)),
                ('n_beforeMarfa', models.DecimalField(decimal_places=1, max_digits=10, null=True)),
                ('n_Marfa', models.DecimalField(decimal_places=1, max_digits=10, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company', to=settings.AUTH_USER_MODEL, verbose_name='Company')),
            ],
            options={
                'unique_together': {('code', 'counter')},
            },
        ),
    ]
