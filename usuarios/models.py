from django.contrib.auth.models import AbstractUser
from django.db import models




class User(AbstractUser):
    es_profesora = models.BooleanField('estado de profesora', default=False)
    es_voluntaria = models.BooleanField('estado de voluntaria', default=False)
    es_coordinadora = models.BooleanField('estado de coordinadora', default=False)
    es_alumna = models.BooleanField('estado de alumna', default=False)
    model_pic = models.ImageField(upload_to='media/imagenes/', default='pic_folder/None/no-img.jpg')

