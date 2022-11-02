import xmlrpc.client as xmlrpclib
import csv
import logging
_logger = logging.getLogger(__name__)
# filelist = ['/home/odoo/src/user/import_product_excel_cr/principado_product/final_catalogue_141022_latest.csv']
# filelist = ['/home/hardik/workspace/cr/principadoerp/import_product_excel_cr/principado_product/import_product_1.csv']
filelist = ['/home/hardik/workspace/cr/principadoerp/import_product_excel_cr/principado_product/final_catalogue_141022_latest.csv']
not_found = []

missing_unspsc_categ = []
for filepath in filelist:
    file_barcode = open(filepath)
    reader_barcode = csv.DictReader(file_barcode, delimiter=",")
    # db_name = "yaelrdrz-principadoerp-main-5969988"
    db_name = "db_principado15"
    db_password = "admin"
    # server = xmlrpclib.ServerProxy('https://principado.odoo.com/xmlrpc/object',allow_none=True)
    server = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object',allow_none=True)
    barcode_list = [x['Barcode'] for x in reader_barcode]
    print("---------barcode_list-------------",len(barcode_list))

    newlist = []  # empty list to hold unique elements from the list
    duplist = []  # empty list to hold the duplicate elements from the list
    for i in barcode_list:
        if i not in newlist:
            newlist.append(i)
        else:
            duplist.append(i)  # this method catches the first duplicate entries, and appends them to the list
    # The next step is to print the duplicate entries, and the unique entries
    print("List of duplicates", duplist)
    # print("Unique Item List", newlist)  # prints the final list of unique items

    print("---------barcode_list----set---------",len(list(set(barcode_list))))

# ['39304777998', '91202697976', '91202697969', '91201050680', '91201049936', '91201050697', '91201083206', '91201083183', '91201083800', '52175039019', '52175039033', '52175040015', '52175040046', '52175040206']