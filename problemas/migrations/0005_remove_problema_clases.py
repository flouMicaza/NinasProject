# Generated by Django 2.2.6 on 2020-05-29 19:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problemas', '0004_problema_clases'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problema',
            name='clases',
        ),
    ]
