# Generated by Django 2.0.13 on 2020-01-29 19:11

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='curso_default', max_length=100)),
                ('cant_clases', models.IntegerField()),
                ('alumnas', models.ManyToManyField(blank=True, related_name='alumnas', to=settings.AUTH_USER_MODEL)),
                ('profesoras', models.ManyToManyField(blank=True, related_name='profesoras', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
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
