# Generated by Django 2.2.6 on 2020-05-04 20:18

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cursos', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='curso',
            name='alumnas',
            field=models.ManyToManyField(blank=True, related_name='alumnas', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='curso',
            name='profesoras',
            field=models.ManyToManyField(blank=True, related_name='profesoras', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='curso',
            name='tema',
            field=models.ManyToManyField(blank=True, related_name='tags', to='cursos.Tema'),
        ),
        migrations.AddField(
            model_name='curso',
            name='voluntarias',
            field=models.ManyToManyField(blank=True, related_name='voluntarias', to=settings.AUTH_USER_MODEL),
        ),
    ]
