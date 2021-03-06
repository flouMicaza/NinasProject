# Generated by Django 2.2.6 on 2020-05-04 20:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cursos', '0001_initial'),
        ('problemas', '0001_initial'),
        ('clases', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clase',
            name='curso',
            field=models.ForeignKey(help_text='Curso al que pertenece la clase', on_delete=django.db.models.deletion.CASCADE, to='cursos.Curso'),
        ),
        migrations.AddField(
            model_name='clase',
            name='problemas',
            field=models.ManyToManyField(help_text='Problemas a resolver en esta clase', to='problemas.Problema'),
        ),
    ]
