# Generated by Django 3.2 on 2022-05-27 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0003_auto_20220525_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='ayn',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
