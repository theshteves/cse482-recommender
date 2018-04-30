import csv
import os
import json

def read_csv_string(input_):
	"""
	Takes a string which is the contents of a CSV file.
	Returns an object containing the data from the file.
	The specific representation of the object is up to you.
	The data object will be passed to the write_*_string functions.
	"""
	#Create and open a temporary file containing input info
	temp_file = open("temp_proj2_file_74837","w+")
	temp_file.write(input_)
	temp_file.close()
	read_file = open("temp_proj2_file_74837","r")
	
	reader = csv.reader(read_file)
	
	data_obj = []
	row_count = 0
	#Create a list to store the headers in
	headers = list()
	for row in reader:
		entry = {}
		if row_count == 0:
			headers = row
			row_count+=1
		else:
			item_num = 0
			for item in headers:
				entry.update({item : row[item_num]})
				item_num+=1
			data_obj.append(entry)
	
	#Close and remove the temporary file
	read_file.close()
	os.remove("temp_proj2_file_74837")
	
	return data_obj
		


def write_csv_string(data):
	"""
	Takes a data object (created by one of the read_*_string functions).
	Returns a string in the CSV format.
	"""
	data_return = ""
	row_num = 0
	#Building the string to return
	#print('data',data)
	for row in data:
		data_return += ','.join(str(v) for v in data[row_num].values())
		data_return += "\n"
		row_num += 1
		
	return data_return


def read_json_string(input_):
	"""
	Similar to read_csv_string, except works for JSON files.
	"""
	return json.loads(input_)



def write_json_string(data):
	"""
	Writes JSON strings. Similar to write_csv_string.
	"""
	return json.dumps(data)



if __name__ == "__main__":
    fp = open('meta_s.json')
    written = open('asin_img_lookup.csv','w') 
    count = 0
    failed = 0

    for line in fp:
        to_write = read_json_string(line)
		
        keys_l = ['asin','imUrl','title']
        try:
            new_write = { k: to_write[k].replace(',', '') for k in keys_l }
        except:
            failed += 1
        #print(new_write)
        
        to_write = write_csv_string([new_write])
        print(to_write)
        written.write(to_write)
        #if count == 10:
            #break
        count += 1
    print("Failed converts = ", failed)
    print("Total items = ", count-failed)
    written.close()






