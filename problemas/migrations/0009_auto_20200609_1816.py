# Generated by Django 2.2.13 on 2020-06-09 22:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('problemas', '0008_problema_clases'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problema',
            name='clases',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='clases.Clase'),
        ),
    ]
