import os
from zipfile import ZipFile 
import shutil


def extract_zip_file_to_folder(path):
	current_directory = os.getcwd()
	
	# Creates folder for path
	access_rights = 0o755
	
	try:  
		os.mkdir(path, access_rights)
	except OSError:  
		print ("Creation of the directory %s failed" % path)
	
	# Copies the zip file to the folder
	shutil.copyfile(path + '.zip', path + '/' + path + '.zip')
	
	# Changes directory to the folder
	os.chdir(path)
	
	# Extracts all files from zip
	with ZipFile(path + '.zip', 'r') as zip: 
		zip.extractall() 
	
	# Deletes the zip in the folder
	os.remove(path + '.zip')
	
	# Goes back to the previous directory
	os.chdir(current_directory)

#delete folder and all its contents
#shutil.rmtree(path)