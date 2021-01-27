import csv
import datetime

from django.core.management.base import BaseCommand
from usuarios.models import User
from cursos.models import Curso
from coordinacion.models import Sede

# modo de uso:
# $python3 manage.py crear_users tipo_de_usuarias path 
# curso = input (si se deja en blanco solo se crean, no se agrega a ningun curso)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('user_kind', nargs='+', type=str)
        parser.add_argument('path', nargs='+', type=str)

    def handle(self, *args, **options):
        sede  = input('Sede: ')
        try:
            sede = Sede.objects.get(nombre=sede)
        except:
            raise Exception(f"No existe sede con ese nombre")
        curso = input('Curso (dejar vacio si solo desea crear usuarias): ')
        if curso == "":
            curso = False
        else:
            anho = datetime.datetime.now().year
            try:
                curso = Curso.objects.get(nombre=curso, sede=sede, anho = anho)
            except:
                raise Exception(f"El curso '{curso}' no existe")
        
        csvFile = open(options['path'][0],'r', encoding='utf-8-sig')
        self.csvValidator(csvFile)
        csvFile = open(options['path'][0],'r', encoding='utf-8-sig')
        self.create(options['user_kind'][0], sede, curso, csvFile)
        self.stdout.write(f"{options['user_kind'][0]} creadas con exito!")

    
    def csvValidator(self, csvFile=None):
        try:
            reader = csv.reader(csvFile)
        except Exception as e:
            raise e
        headers = next(reader, None)
        if len(headers)!=3: #Actualmente solo se considera nombre,apellido,email
            raise Exception(f"Se esperaban 3 columnas en los headers, pero hay {len(headers)}")
        elif headers!=["nombre","apellido","email"]: #Se espera que los headers tengan ese orden
            raise Exception("Los headers no estan correctos, deberian ser: nombre,apellido,email")
        for i,row in enumerate(reader):
            if len(row)!=3:
                raise Exception(f"Se esperaban 3 columnas en la fila {i+1}, pero hay {len(row)}")
        csvFile.close()

    def create(self, kind, sede, curso, csvFile):
        tipos = {'profesoras':False, 'alumnas':False, 'coordinadoras':False, 'voluntarias':False} #tipos de usuarias disponibles
        if tipos.get(kind) != None:
            tipos[kind] = True
        else:
            raise Exception(f'El tipo de usuarias {kind} no esta definido, debe ser alguno de los siguientes: {(", ").join(list(tipos.keys()))}')
        reader = csv.reader(csvFile)
        next(reader,None)
        for row in reader:
            username = f'{row[2]}' #Ex: email
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.first_name=row[0]
                user.last_name=row[1]
                user.es_profesora = tipos['profesoras']
                user.es_voluntaria = tipos['voluntarias']
                user.es_alumna = tipos['alumnas']
                user.set_password('tempPass21')
                user.save()
            else:
                user.is_active = True
                user.save()
            ops_sede = {'profesoras':sede.profesoras, 'alumnas':sede.alumnas, 'voluntarias':sede.voluntarias}
            ops_sede[kind].add(user)
            if curso and kind!='coordinadoras':
                # tipos de usuarias que pueden pertenecer al curso
                ops = {'profesoras':curso.profesoras, 'alumnas':curso.alumnas, 'voluntarias':curso.voluntarias}
                ops[kind].add(user)

