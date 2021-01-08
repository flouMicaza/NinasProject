from django.core.exceptions import ValidationError

import csv
import json
import os
import random
import string 

def get_file_name(file_path):
    """
    Gets the name of a file from a path
    :param file_path: str
    :return: str
    """
    return file_path.split("/")[-1]


def change_path_extension(path, new_extension):
    """
    Changes the extension of a file
    :param path: str
    :param new_extension: str
    :return: str
    """
    splitted_path = path.split('.')
    if len(splitted_path) > 1:
        splitted_path[-1] = new_extension
        return '.'.join(splitted_path)
    else:
        return path


# ------------------------------------------------------------------------------------------------
# functions to check file validity
def raiseError(File, kind, *kwargs):
    args = [0]*3
    for i,e in enumerate(kwargs):
        args[i] = e
    
    errors = {
        'csv' : {
            0: 'El archivo de test no es valido',
            1: 'Hay una cantidad distinta de columnas a las esperadas',
            2: f'El primer Header debería ser Input, pero es {args[0]}',
            3: f'El segundo Header debería ser Output, pero es {args[0]}',
            4: f'El tercer Header debería ser Categoria, pero es {args[0]}',
            5: f'Test {args[0]} no posee tres elementos',
            6: f'El input "{args[0]}" se repite en los test {args[1]} y {args[2]}' 

        },
        'json': {
            0: 'El archivo de test no es valido',
            1: f'Hay menos elementos de los esperados en el test {args[0]}',
            2: f'El primer Header del test:{args[0]} debería ser Input, pero es {args[1]}',
            3: f'El segundo Header del test:{args[0]} debería ser Output, pero es {args[1]}',
            4: f'El tercer Header del test:{args[0]} debería ser Categoria, pero es {args[1]}',
            5: f'El input "{args[0]}" se repite en los test {args[1]} y {args[2]}'
        }
    }

    extension = File.name.split('.')[-1]    
    File.close()
    if extension == 'csv': 
        if os.path.exists(File.name):
            os.remove(File.name)
    
    raise ValidationError(errors[extension][kind])

def check_inputs(reader, csvFile):
    inputs = dict()
    i = 0
    l = next(reader, None)
    while l != None:
        if len(l)!=3:
            raiseError(csvFile, 5, i+1)
        if inputs.get(l[0]) != None:
            raiseError(csvFile, 6, l[0], inputs.get(l[0]), i+1)
        inputs[l[0]] = i+1
        l = next(reader, None)
        i+=1
    return

def create_csv_file(csvFile):
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(10))
    filename = f'{result_str}.csv'    
    with open(filename, "w") as f:
        content = csvFile.file.file.read().decode()
        for l in content:
            f.write(l)
        f.close()
    return filename

def check_valid_csv(csvFile = None, path = ""):
    if csvFile == None:
        csvFile = open(path, 'r')
        filename = ""
    #crear archivo
    else:
        filename = create_csv_file(csvFile)
        csvFile = open(filename, 'r')
    
    try:
        reader = csv.reader(csvFile, None)
    except:
        raiseError(csvFile, 0)

    headers = next(reader, None)

    if len(headers) != 3:
        raiseError(csvFile, 1)
    elif headers[0] != "Input":
        raiseError(csvFile, 2, headers[0])
    elif headers[1] != "Output":
        raiseError(csvFile, 3, headers[1])
    elif headers[2] != "Categoria":
        raiseError(csvFile, 4, headers[2])

    check_inputs(reader, csvFile)

    if os.path.exists(filename):
        os.remove(filename)

    return True

def check_valid_json(jsonFile = None, path = ""):
    if jsonFile == None:
        jsonFile = open(path, 'r')

    try:
        datastore = json.load(jsonFile)
    except:
        raiseError(jsonFile, 0)

    inputs = dict()
    for i, e in enumerate(datastore):
        headers = list(e.keys())
        vals = list(e.values())

        if len(headers) != 3:
            # print("len de headers es != 3. Línea: ", e)
            raiseError(jsonFile, 1, i+1)

        elif headers[0] != "Input":
            # print("Header 0 no es Input. Línea: ", e)
            raiseError(jsonFile, 2, i+1,headers[0])

        elif headers[1] != "Output":
            # print("Header 0 no es Output. Línea: ", e)
            raiseError(jsonFile, 3,i+1, headers[1])

        elif headers[2] != "Categoria":
            # print("Header 0 no es Categoria. Línea: ", e)
            raiseError(jsonFile, 4, i+1, headers[2])

        if inputs.get(vals[0]) != None:
            raiseError(jsonFile, 5, vals[0], inputs.get(vals[0]),i+1)
        inputs[vals[0]] = i+1

    return True

valid_file_functions = dict()
valid_file_functions['csv'] = lambda x,y: check_valid_csv(x,y)
valid_file_functions['json'] = lambda x,y: check_valid_json(x,y)
# ------------------------------------------------------------------------------------------------
# functions to import files into lists of dicts
def csv_to_dict_list(csv_path):
    """
    Creates a list of dictionaries from a .csv file
    :param csv_path: str
    :return: list(dict())
    """
    new_list = []

    with open(csv_path, 'r') as csvFile:
        reader = csv.reader(csvFile)
        headers = next(reader, None)
        for row in reader:
            element = {}
            for i in range(len(headers)):
                element[headers[i]] = row[i]
            new_list.append(element)

    csvFile.close()

    return new_list


def json_to_dict_list(json_path):
    """
    Creates a list of dictionaries from a .json file
    :param json_path: str
    :return: list(dict())
    """
    with open(json_path, 'r') as jsonFile:
        datastore = json.load(jsonFile)
    jsonFile.close()

    return datastore


file_to_dict_list_functions = dict()
file_to_dict_list_functions['csv'] = lambda x: csv_to_dict_list(x)
file_to_dict_list_functions['json'] = lambda x: json_to_dict_list(x)


# ------------------------------------------------------------------------------------------------
# functions to save lists of dicts to files

def dict_list_to_json_file(data, json_path):
    """
    Saves a list of dictionaries to a .json file
    :param data: list(dict())
    :param json_path: str
    :return: None
    """
    with open(json_path, 'w') as outfile:
        json.dump(data, outfile)
    outfile.close()


def dict_list_to_csv_file(data, csv_path):
    """
    Saves a list of dictionaries to a .csv file
    :param data: list(dict())
    :param csv_path: str
    :return: None
    """
    with open(csv_path, 'w', newline='') as outfile:
        fieldnames = list(data[0].keys())
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for element in data:
            writer.writerow(element)
    outfile.close()


dict_list_to_file_functions = dict()
dict_list_to_file_functions['json'] = lambda x, y: dict_list_to_json_file(x, y)
dict_list_to_file_functions['csv'] = lambda x, y: dict_list_to_csv_file(x, y)


# ------------------------------------------------------------------------------------------------
# functions to append lists of dicts to files

def append_dict_list_to_json_file(data, json_path):
    """
    Appends a list of dictionaries to a .json file
    :param data: list(dict())
    :param json_path: str
    :return: None
    """
    json_data = file_to_dict_list_functions['json'](json_path)
    new_data = json_data + data

    dict_list_to_file_functions['json'](new_data, json_path)


append_dict_list_to_file_functions = dict()
append_dict_list_to_file_functions['json'] = lambda x, y: append_dict_list_to_json_file(x, y)


# ------------------------------------------------------------------------------------------------
# API

def file_to_file(path1, path2):
    """
    Puts de content of a file into another file respecting the extension's format
    :param path1: str
    :param path2: str
    :return: None
    """
    extension1 = path1.split('.')[-1]
    extension2 = path2.split('.')[-1]

    if extension1 in file_to_dict_list_functions and extension2 in dict_list_to_file_functions:
        data = file_to_dict_list_functions[extension1](path1)
        dict_list_to_file_functions[extension2](data, path2)
    else:
        raise Exception('In or Out File Extensions not supported.')


def append_file_to_file(path1, path2):
    """
    Appends the content of a file into another file respecting the extension's format
    :param path1: str
    :param path2: str
    :return: None
    """
    extension1 = path1.split('.')[-1]
    extension2 = path2.split('.')[-1]

    if extension1 in file_to_dict_list_functions and extension2 in append_dict_list_to_file_functions:
        data = file_to_dict_list_functions[extension1](path1)
        append_dict_list_to_file_functions[extension2](data, path2)
    else:
        raise Exception('In or Out File Extensions not supported.')

def check_if_file_is_valid(file = None, path=""):
    extension = path.split('.')[-1] if file == None else file.name.split('.')[-1]
    if valid_file_functions.get(extension) == None:
        return False
    return valid_file_functions[extension](file, path)