import logging
from xmlrpc import client as xmlrpclib

_logger = logging.getLogger(__name__)
url = 'http://localhost:8069'
dbname = 'yaelrdrz-principadoerp-main-5969988'    #the database
username = 'admin'    #the user
password = 'AdM1nPr1nc.'

sock = xmlrpclib.ServerProxy('https://principado.odoo.com/xmlrpc/object', allow_none=True)


product_tmpl_vals  = {'test': 'Test'}
sock.execute(dbname, 2, password, 'product.template', "update_variant_value", [], product_tmpl_vals)
sock.execute(dbname, 2, password, 'product.template', "create_variant_vals", [], product_tmpl_vals)
#
# import csv
# with open('/home/erp/repo/principadoerp/import_product_excel_cr/final_catalogue_141022_latest.csv', mode='r')as file:
#     reader = csv.reader(file)
#     raw_data = [x for x in reader]


