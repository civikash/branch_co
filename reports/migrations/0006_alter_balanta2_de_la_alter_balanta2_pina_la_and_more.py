# Generated by Django 4.1.5 on 2023-07-03 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0005_alter_balanta1_la'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balanta2',
            name='de_la',
            field=models.DateField(null=True, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='balanta2',
            name='pina_la',
            field=models.DateField(null=True, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='balanta3',
            name='de_la',
            field=models.DateField(null=True, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='balanta3',
            name='pina_la',
            field=models.DateField(null=True, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='balanta4',
            name='de_la',
            field=models.DateField(null=True, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='balanta4',
            name='pina_la',
            field=models.DateField(null=True, verbose_name=''),
        ),
    ]