import csv

def csv_to_list(csv_path):
	new_list = []
	
	with open(csv_path, 'r') as csvFile:
		reader = csv.reader(csvFile)
		for row in reader:
			new_list.append(row)
	
	csvFile.close()
	
	return new_list

def list_to_csv(a_list, csv_path):
	with open(csv_path, 'w') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerows(a_list)
	
	csvFile.close()