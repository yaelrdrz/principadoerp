import csv

file_test = "/home/hardik/workspace/cr/principadoerp/import_product_excel_cr/principado_product/test_principado.csv"

file_original = "/home/hardik/workspace/cr/principadoerp/import_product_excel_cr/principado_product/final_catalogue_141022.csv"
file_original_reader = csv.DictReader(open(file_original),delimiter=",")

missing_barcode_filelist = ["/home/hardik/workspace/cr/principadoerp/import_product_excel_cr/principado_product/missing_barcode_file.csv"]
missing_file = open(missing_barcode_filelist[0])
missing_barcode_reader = csv.DictReader(missing_file,delimiter=",")
missing_barcode_reader_list = [x['Barcode'] for x in missing_barcode_reader]

temp = []
temp_keys = True
for line in file_original_reader:
    if line['Barcode'] in missing_barcode_reader_list:
        temp.append(dict(line))
        if temp_keys:
            hh = list(line.keys())
            temp_keys = False
            # print("--------asd--------",fields,type(fields))
            # print("--------asd--------",line,type(dict(line)))
            # stop
# print("-------temp-------",len(temp))
# print("-------temp-------", type(fields))

with open(file_test, 'w') as f1:
    # creating a csv dict writer object
    writer = csv.DictWriter(f1, fieldnames=hh)
    writer.writeheader()
    for dd in temp:
        print("-------dd--------",type(dd))
        # writing data rows
        writer.writerow(dd)



