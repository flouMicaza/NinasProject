import csv
import datetime
import sys

from django.core.management.base import BaseCommand
from usuarios.models import User
from cursos.models import Curso

# modo de uso:
# $python3 manage.py crear_users tipo_de_usuarias path 
# curso = input (si se deja en blanco solo se crean, no se agrega a ningun curso)

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('user_kind', nargs='+', type=str)
        parser.add_argument('path', nargs='+', type=str)

    def handle(self, *args, **options):
        curso = input('Curso (dejar vacio para solo crear): ')
        if curso == "":
            curso = False
        else:
            try:
                curso = Curso.objects.get(nombre=curso)
            except:
                raise Exception(f"El curso '{curso}' no existe")

        self.csvValidator(options['path'][0])
        self.create(options['path'][0], options['user_kind'][0], curso)
    
    def csvValidator(self, path):
        try:
            csvFile = open(path, 'r', encoding='utf-8-sig')
            reader = csv.reader(csvFile)
        except Exception as e:
            raise e
        headers = next(reader, None)
        if len(headers)!=2: #Actualmente solo se considera nombre,apellido
            raise Exception(f"Se esperaban 2 columnas en los headers, pero hay {len(headers)}")
        elif headers!=["nombre","apellido"]: #Se espera que los headers tengan ese orden
            raise Exception("Los headers no estan correctos, deberian ser: nombre,apellido")
        for i,row in enumerate(reader):
            if len(row)!=2:
                raise Exception(f"Se esperaban 2 columnas en la fila {i+1}, pero hay {len(row)}")
        csvFile.close()

    def create(self, path, kind, curso):
        tipos = {'profesoras':False, 'alumnas':False, 'coordinadoras':False, 'voluntarias':False} #tipos de usuarias disponibles
        if tipos.get(kind) != None:
            tipos[kind] = True
        else:
            raise Exception(f'El tipo de usuarias {kind} no esta definido, debe ser alguno de los siguientes: {(", ").join(list(tipos.keys()))}')
        with open(path,'r', encoding='utf-8-sig') as csvFile:
            reader = csv.reader(csvFile)
            next(reader,None)
            for row in reader:
                username = f'{row[0]}.{row[1]}.{str(datetime.date.today().year)[-2:]}' #Ex: nombre.apellido.21
                i = 1
                while len(User.objects.filter(username=username))>0: #Si por alguna razon existe el user -> nombre.apellido1.21
                    username = f'{row[0]}.{row[1]}{i}.{str(datetime.date.today().year)[-2:]}'
                    i+=1
                user = User.objects.create_user(first_name=row[0], last_name=row[1],username=username,
                                                es_profesora= tipos['profesoras'], es_voluntaria = tipos['voluntarias'],
                                                es_coordinadora = tipos['coordinadoras'], es_alumna =tipos['alumnas'], 
                                                password='tempPass21')
                if curso and kind!='coordinadoras':
                    # tipos de usuarias que pueden pertenecer al curso
                    ops = {'profesoras':curso.profesoras, 'alumnas':curso.alumnas, 'voluntarias':curso.voluntarias}
                    ops[kind].add(user)
        self.stdout.write(f"{kind} creadas con exito!")

