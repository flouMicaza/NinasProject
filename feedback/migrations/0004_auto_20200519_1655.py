# Generated by Django 2.2.6 on 2020-05-19 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0003_auto_20200519_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outputalternativo',
            name='frecuencia',
            field=models.IntegerField(default=1, help_text='Frecuencia con que ha aparecido el output'),
        ),
    ]
