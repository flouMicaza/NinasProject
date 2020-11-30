#Ejemplo de script para tomar data de un csv y guardar datos en la base de datos.
import csv
def crear_regiones(path):
    with open(path, 'r') as csvFile:
        reader = csv.reader(csvFile)
        headers = next(reader, None)
        for row in reader:
            #Region.objects.create(id=row[0], nombre=row[1],latitud=row[2], longitud=row[3])
            print(row[1])
