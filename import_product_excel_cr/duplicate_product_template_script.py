import logging
from xmlrpc import client as xmlrpclib

_logger = logging.getLogger(__name__)
url = 'http://localhost:8069'
dbname = 'yaelrdrz-principadoerp-main-5969988'    #the database
username = 'admin'    #the user
password = 'AdM1nPr1nc.'

sock = xmlrpclib.ServerProxy('https://principado.odoo.com/xmlrpc/object', allow_none=True)

product_tmpl_vals  = {'test': 'Test'}
# sock.execute(dbname, 2, password, 'product.template', "update_variant_value", [], product_tmpl_vals)
sock.execute(dbname, 2, password, 'product.template', "create_variant_vals", [], product_tmpl_vals)

# import csv
#
# with open('/home/erp/repo/principadoerp/import_product_excel_cr/final_catalogue_141022_latest.csv', mode='r')as file:
#     reader = csv.reader(file)
#     raw_data = [x for x in reader]
#     barcode_value_dict = {}
#
#     # Barcode creation first-------------------------
#     barcode_list = [x[2] + '-Duplicate' for x in raw_data]
#     for barcode in list(set(barcode_list[1:])):
#         barcode_id = sock.execute(dbname, 2, password, 'product.barcode', "search", [('barcode', '=', barcode)])
#         if not barcode_id:
#             barcode_id = [sock.execute(dbname, 2, password, 'product.barcode', "create", {'barcode': barcode})]
#         barcode_value_dict.update({barcode: barcode_id[0]})
#
#     for line in raw_data[1:]:
#         variant_search_id = True
#
#         barcode_key = line[2] + '-Duplicate'
#         barcode = barcode_value_dict[barcode_key]
#         barcode_update = sock.execute(dbname, 2, password, 'product.barcode', "write",
#                                       [barcode_value_dict[barcode_key]],
#                                       {"product_id": variant_search_id,
#                                        'product_tmpl_id': variant_search_id.product_tmpl_id.id})
#         product_variant_update = sock.execute(dbname, 2, password, 'product.product', "write",
#                                               variant_search_id, {"default_code": line[3]})

