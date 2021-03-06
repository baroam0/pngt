# Generated by Django 3.2 on 2022-05-25 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idsigho', models.CharField(blank=True, max_length=100, null=True)),
                ('apellido', models.CharField(max_length=100)),
                ('nombre', models.CharField(max_length=100)),
                ('numerodocumento', models.CharField(max_length=100)),
                ('sexo', models.CharField(choices=[('masculino', 'masculino'), ('femenino', 'femenino')], default='masculino', max_length=9)),
                ('pais', models.CharField(max_length=100)),
                ('provincia', models.CharField(max_length=100)),
                ('partido', models.CharField(max_length=100)),
                ('localidad', models.CharField(max_length=100)),
                ('barrio', models.CharField(max_length=100)),
                ('domicilio', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Pacientes',
            },
        ),
    ]
