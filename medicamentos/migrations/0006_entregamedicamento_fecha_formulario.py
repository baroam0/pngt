# Generated by Django 3.2 on 2022-06-15 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicamentos', '0005_entregamedicamento'),
    ]

    operations = [
        migrations.AddField(
            model_name='entregamedicamento',
            name='fecha_formulario',
            field=models.DateField(blank=True, null=True),
        ),
    ]