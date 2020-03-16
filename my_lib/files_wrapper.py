import csv
import json
import yaml


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
def check_valid_csv(path):
    with open(path, 'r') as csvFile:
        try:
            reader = csv.reader(csvFile)
            headers = next(reader, None)
            if len(headers) != 4 or headers[0] != "Input" or headers[1] != "Output" or headers[2] != "Comment" or \
                    headers[3] != "Test Type":
                raise Exception

            for row in reader:
                if len(row) != 4:
                    raise Exception

            csvFile.close()
            return True
        except:
            csvFile.close()
            return False


def check_valid_yml(path):
    with open(path, 'r') as ymlFile:
        try:
            yml_str = ymlFile.read()
            new_list = yaml.load(yml_str, Loader=yaml.FullLoader)

            for e in new_list:
                headers = list(e.keys())
                if len(headers) != 4 or headers[0] != "Input" or headers[1] != "Output" or headers[2] != "Comment" or \
                        headers[3] != "Test Type":
                    raise Exception

            ymlFile.close()
            return True
        except:
            ymlFile.close()
            return False


def check_valid_json(path):
    with open(path, 'r') as jsonFile:
        try:
            datastore = json.load(jsonFile)

            for e in datastore:
                headers = list(e.keys())
                if len(headers) != 4 or headers[0] != "Input" or headers[1] != "Output" or headers[2] != "Comment" or \
                        headers[3] != "Test Type":
                    raise Exception

            jsonFile.close()
            return True
        except:
            jsonFile.close()
            return False


valid_file_functions = dict()
valid_file_functions['csv'] = lambda x: check_valid_csv(x)
valid_file_functions['yml'] = lambda x: check_valid_yml(x)
valid_file_functions['yaml'] = lambda x: check_valid_yml(x)
valid_file_functions['json'] = lambda x: check_valid_json(x)
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


def yml_to_dict_list(yml_path):
    """
    Creates a list of dictionaries from a .yml file
    :param yml_path: str
    :return: list(dict())
    """
    with open(yml_path, 'r') as ymlFile:
        yml_str = ymlFile.read()
        new_list = yaml.load(yml_str, Loader=yaml.FullLoader)

    ymlFile.close()

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
file_to_dict_list_functions['yml'] = lambda x: yml_to_dict_list(x)
file_to_dict_list_functions['yaml'] = lambda x: yml_to_dict_list(x)
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

def check_if_file_is_valid(path):
    extension = path.split('.')[-1]
    try:
        return valid_file_functions[extension](path)
    except:
        return False
