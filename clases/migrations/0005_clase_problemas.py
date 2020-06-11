# Generated by Django 2.2.13 on 2020-06-09 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problemas', '0007_remove_problema_clases'),
        ('clases', '0004_remove_clase_problemas'),
    ]

    operations = [
        migrations.AddField(
            model_name='clase',
            name='problemas',
            field=models.ManyToManyField(blank=True, help_text='Problemas a resolver en esta clase', to='problemas.Problema'),
        ),
    ]