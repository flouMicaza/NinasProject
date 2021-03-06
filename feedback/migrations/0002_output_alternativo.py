# Generated by Django 2.2.6 on 2020-05-19 20:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('problemas', '0003_auto_20200518_1218'),
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='output_alternativo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('output_obtenido', models.CharField(help_text='Output obtenido para el test', max_length=255)),
                ('frecuencia', models.IntegerField(default=0, help_text='Frecuencia con que ha aparecido el output')),
                ('agregado', models.BooleanField(default=False, help_text='Si se ha agregado o no como output alternativo')),
                ('caso', models.ForeignKey(help_text='Caso que probó este test_feedback', on_delete=django.db.models.deletion.CASCADE, to='problemas.Caso')),
            ],
            options={
                'unique_together': {('caso', 'output_obtenido')},
            },
        ),
    ]
