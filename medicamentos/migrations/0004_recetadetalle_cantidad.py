# Generated by Django 3.2 on 2022-06-01 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicamentos', '0003_receta_recetadetalle'),
    ]

    operations = [
        migrations.AddField(
            model_name='recetadetalle',
            name='cantidad',
            field=models.IntegerField(default=0),
        ),
    ]
