from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    es_profesora = models.BooleanField('estado de profesora', default=False)
    es_voluntaria = models.BooleanField('estado de voluntaria', default=False)
    es_coordinadora = models.BooleanField('estado de coordinadora', default=False)
    es_alumna = models.BooleanField('estado de alumna', default=False)
    model_pic = models.ImageField(upload_to='media/imagenes/', default='pic_folder/None/no-img.jpg')

    def get_menu_items(self):
        items_dict = {
            'profesora': [('Mis cursos', reverse('usuarios:index'))],
            'voluntaria': [('Mis cursos', reverse('usuarios:index'))],
            'alumna:': [('Ver curso', reverse('usuarios:index'))],
            'coordinadora': [('Mis cursos', reverse('usuarios:index')),
                             ('Modo coordinadora', reverse('coordinadora:inicio_coordinadora'))]
        }
        if self.es_coordinadora:
            return items_dict['coordinadora']
        elif self.es_profesora:
            return items_dict['profesora']
        elif self.es_voluntaria:
            return items_dict['voluntaria']
        elif self.es_alumna:
            return items_dict['alumna:']
