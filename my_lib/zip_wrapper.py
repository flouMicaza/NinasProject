import os
from zipfile import ZipFile
import shutil


def extract_zip_file_to_folder(zip_path):
    """
    Extracts the content of a .zip file into a directory of the same name
    :param path: str
    :return: None
    """
    path = zip_path.replace(".zip", "")

    current_directory = os.getcwd()

    # Creates folder for path
    access_rights = 0o755

    try:
        os.mkdir(path, access_rights)
    except OSError:
        print("Creation of the directory %s failed" % path)

    # Changes directory to the folder
    os.chdir(path)

    # Extracts all files from zip
    with ZipFile(path + '.zip', 'r') as zip_file:
        zip_file.extractall()

    # Goes back to the previous directory
    os.chdir(current_directory)


def delete_folder_and_content(path):
    """
    Deletes a folder and its contents
    :param path: str
    :return: None
    """
    shutil.rmtree(path)
