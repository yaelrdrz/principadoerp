import logging
from xmlrpc import client as xmlrpclib
from datetime import datetime, timedelta
import xlsxwriter

_logger = logging.getLogger(__name__)

# dbname = 'sfs_migrated'
url = 'https://principado.odoo.com'
dbname = 'yaelrdrz-principadoerp-main-5969988'    #the database
username = 'admin'    #the user
password = 'AdM1nPr1nc.'
common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
uid = common.authenticate(dbname, username, password, {})
uid = 2

#replace localhost with the address of the server
sock = xmlrpclib.ServerProxy('https://principado.odoo.com/xmlrpc/object')

row = 0

def generate_record(vals,last_parent):
	last_categ_id = sock.execute_kw(dbname, uid, password, 'pos.category', 'create', [{
		    'name': vals
		}])
	if last_parent and last_categ_id:
		sock.execute_kw(dbname, uid, password, 'pos.category', 'write', [[last_parent], {
    'parent_id': last_categ_id    
}])

	return last_categ_id

def concate_list(lines):	
	return ''.join(lines)

import csv
with open('/home/odoo/src/user/import_product_excel_cr/principado_product/final_catalogue_141022_latest.csv', mode='r')as file:
	csvfile = csv.reader(file)
	final_dict = {}
	for lines in csvfile:
		actual_lines = lines.copy()	
		if row == 0: 
			row += 1
			continue
		till = 10
		lines = lines[10:20]
		last_parent = False
		while len(lines) >= 1:
			lines = lines[:len(lines)]
			if lines[-1] == '' or not lines[-1]:
				
				lines = lines[:len(lines)-1]
				continue
			new_key = concate_list(lines)
			if new_key not in final_dict:
				last_parent = generate_record(lines[-1], last_parent)
				final_dict[new_key] = last_parent
			else:
				if last_parent != final_dict[new_key]:
					sock.execute_kw(dbname, uid, password,'pos.category',  'write',[[last_parent], {
					    'parent_id': final_dict[new_key]    
					}])

					break				
			lines = lines[:len(lines)-1]
			
		prod_name = actual_lines[1] + '(Tamaño:' + (actual_lines[4] or '' ) + ',Color:' + (actual_lines[5] or '') + ')'
		product_id = sock.execute_kw(dbname, uid, password,'product.template',  'search',[[('name','=',prod_name),('default_code','=',actual_lines[3])]])
		print (' productname, id,categ id  =================',prod_name, product_id, row)
		product_id and sock.execute_kw(dbname, uid, password, 'product.template', 'write', [[product_id[0]], {
		    'pos_categ_id': final_dict[ ''.join(actual_lines[10:20]) ]
		}])
		row += 1
		




