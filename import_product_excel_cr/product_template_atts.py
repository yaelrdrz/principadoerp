import logging
from xmlrpc import client as xmlrpclib
from datetime import datetime, timedelta
import xlsxwriter

_logger = logging.getLogger(__name__)
url = 'https://principado.odoo.com'
dbname = 'yaelrdrz-principadoerp-main-5969988'    #the database
username = 'admin'    #the user
password = 'AdM1nPr1nc.'

common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
uid = common.authenticate(dbname, username, password, {})
uid = common.login(dbname, username, password)
sock = xmlrpclib.ServerProxy('https://principado.odoo.com/xmlrpc/object'.format(url))
row = 0
not_found = []
import csv
with open('final_catalogue_141022_latest.csv', mode='r')as file:
	reader = csv.reader(file)
	final_dict = {}
	uom_list = {}
	size_value_dict = {}
	color_value_dict = {}
	barcode_value_dict = {}
	unspsc_value_dict = {}
	vendor_value_dict = {}
	uom_value_dict = {}
	raw_data = [x for x in reader]

	#Size attribute creation first-------------------------
	size_list = [x[4] for x in raw_data]
	size_vals = {"name": "Size", "display_type": "select", "create_variant": "always", "visibility": "visible"}
	size_attribute_id = sock.execute(dbname, 2, password, 'product.attribute', "search", [('name', '=', 'Size')])
	if not size_attribute_id:
		size_attribute_id = [sock.execute(dbname, 2, password, 'product.attribute', "create", size_vals)]

	for size in list(set(size_list[1:])):
		size_value_id = sock.execute(dbname, 2, password, 'product.attribute.value', "search",
									   [('name', '=', size), ('attribute_id', '=', size_attribute_id[0])])
		if not size_value_id:
			size_value_id = [sock.execute(dbname, 2, password, 'product.attribute.value', "create",
											{'name': size, 'attribute_id': size_attribute_id[0]})]
		size_value_dict.update({size: size_value_id[0]})

	#color attribute creation first-------------------------
	color_list = [x[5] for x in raw_data]
	color_vals = {"name": "Color", "display_type": "color", "create_variant": "always", "visibility": "visible"}
	color_attribute_id = sock.execute(dbname, 2, password, 'product.attribute', "search",
										[('name', '=', 'Color')])
	if not color_attribute_id:
		color_attribute_id = [sock.execute(dbname, 2, password, 'product.attribute', "create", color_vals)]
	for color in list(set(color_list[1:])):
		color_value_id = sock.execute(dbname, 2, password, 'product.attribute.value', "search",
										[('name', '=', color), ('attribute_id', '=', color_attribute_id[0])])
		if not color_value_id:
			color_value_id = [sock.execute(dbname, 2, password, 'product.attribute.value', "create",
											 {'name': color, 'attribute_id': color_attribute_id[0]})]
		color_value_dict.update({color: color_value_id[0]})

	# Barcode creation first-------------------------
	barcode_list = [x[2]+'-Duplicate' for x in raw_data]
	for barcode in list(set(barcode_list[1:])):
		barcode_id = sock.execute(dbname, 2, password, 'product.barcode', "search", [('barcode', '=', barcode)])
		if not barcode_id:
			barcode_id = [sock.execute(dbname, 2, password, 'product.barcode', "create", {'barcode': barcode})]
		barcode_value_dict.update({barcode: barcode_id[0]})

	# UNSPSC creation first-------------------------
	unspsc_list = [x[8] for x in raw_data]
	for unspsc in list(set(unspsc_list[1:])):
		unspsc_id = sock.execute(dbname, 2, password, 'product.unspsc.code', "search",
								   [('comp_name', '=like', unspsc)])
		if not unspsc_id:
			unspsc_split = unspsc.split("-")
			if len(unspsc_split) > 1:
				unspsc_id = sock.execute(dbname, 2, password, 'product.unspsc.code', "search",
										   [('code', '=like', unspsc_split[0])])
		if unspsc_id:
			unspsc_value_dict.update({unspsc: unspsc_id and unspsc_id[0] or False})

	# Vendor creation first-------------------------
	vendor_list = [x[9] for x in raw_data]
	for vendor in list(set(vendor_list[1:])):
		vendor_id = sock.execute(dbname, 2, password, 'res.partner', "search", [('name', '=', vendor)])
		if not vendor_id:
			vendor_id = [sock.execute(dbname, 2, password, 'res.partner', "create", {'name': vendor})]
		vendor_value_dict.update({vendor: vendor_id[0]})

	# UoM creation first-------------------------
	uom_list = [x[6] for x in raw_data]
	for uom in list(set(uom_list[1:])):
		uom_value_dict.update({uom: 1})

	final_dict = {}
	tmpl_price = {}
	tmpl_unspsc_dict = {}
	tmpl_vendor_dict = {}
	for line in raw_data[1:]:
		if final_dict and ((line[1] + ' -Duplicate')) in final_dict.keys():
			for k_dict, v_dict in final_dict.items():
				if k_dict == (line[1] + ' -Duplicate'):
					if line[4] in [x['Attribute_1_size'] for x in v_dict] and \
							line[5] in [x['Attribute_2_color'] for x in v_dict]:
						match_found = False
						for v_bar_dict in v_dict:
							if v_bar_dict['Attribute_1_size'] == line[4] and v_bar_dict[
								'Attribute_2_color'] == line[5]:
								v_bar_dict['Barcodes'].append(line[2])
								match_found = True
						if not match_found:
							v_dict.append({'Attribute_1_size': line[4],
										   'Attribute_2_color': line[5],
										   'Variant_internal_reference': line[3],
										   'Barcodes': [line[2]]})
					else:
						v_dict.append(
							{'Attribute_1_size': line[4],
							 'Attribute_2_color': line[5],
							 'Variant_internal_reference': line[3],
							 'Barcodes': [line[2]]})
		else:
			final_dict.update({(line[1] + ' -Duplicate'): [
				{'Attribute_1_size': line[4], 'Attribute_2_color': line[5],
				 'Variant_internal_reference': line[3],
				 'Barcodes': [line[2]]}]})
			tmpl_price.update({(line[1] + ' -Duplicate'): line[7]})
			tmpl_unspsc_dict.update({(line[1] + ' -Duplicate'): unspsc_value_dict.get(line[8])})
			tmpl_vendor_dict.update({(line[1] + ' -Duplicate'): vendor_value_dict.get(line[9])})
	for line in raw_data[1:]:
		_logger.info('------------------------ line ref --------- %s', line[1])
		prod_tmpl_dict = {}
		try:
			product_tmpl_vals = {}
			product_tmpl_id = sock.execute(dbname, 2, password, 'product.template', "search", [('name', '=', (line[1] + ' -Duplicate'))])
			if not product_tmpl_id:
				variant_vals = [(0,0,{'attribute_id':size_attribute_id[0],
									  'value_ids': [size_value_dict.get(line[4])]}),
								(0,0,{'attribute_id':color_attribute_id[0],
									  'value_ids': [color_value_dict.get(line[5])]})]
				product_tmpl_vals = {
					"name": line[1] + ' -Duplicate',
					"default_code": line[3],
					"uom_id": 1,
					'available_in_pos': True,
					'type': 'product',
					'website_published': True,
					'tracking': 'lot',
					"list_price": line[7],
					'sale_ok': True,
					'purchase_ok': True,
					'invoice_policy': 'order',
					'purchase_method': 'purchase',
					'unspsc_code_id': unspsc_value_dict.get(line[8]),
					'attribute_line_ids': variant_vals,
					'seller_ids': vendor_value_dict and [(0, 0, {'name': vendor_value_dict.get(line[9]), 'min_qty': 1.0})],
					'vendor_partner_id': vendor_value_dict and vendor_value_dict.get(line[9]) or False,
					'size_attribute_value_id': size_value_dict.get(line[4]),
					'color_attribute_value_id': color_value_dict.get(line[5]),
					'size_id': size_attribute_id[0],
					'size_value_id': size_value_dict.get(line[4]),
					'color_id': color_attribute_id[0],
					'color_value_id': color_value_dict.get(line[5]),
				}
				product_tmpl_id = [
					sock.execute(dbname, 2, password, 'product.template', "product_templ_create_sql_xmlrpc", [], product_tmpl_vals)]

				prod_variant_domain = [('product_tmpl_id', '=', product_tmpl_id),
									   ('name', '=', (line[1] + ' -Duplicate')), ]
				product_id = sock.execute(dbname, 2, password, 'product.product', "search",
										  prod_variant_domain)
				if product_id:
					barcode_key = line[2] + '-Duplicate'
					barcode = barcode_value_dict[barcode_key]
					barcode_update = sock.execute(dbname, 2, password, 'product.barcode', "write",
												  [barcode_value_dict[barcode_key]],
												  {"product_id": product_id[0], 'product_tmpl_id': product_tmpl_id})
					product_variant_update = sock.execute(dbname, 2, password, 'product.product', "write",
														  product_id, {"default_code": line[3]})
				already_created = False
			else:
				for key in final_dict[(line[1] + ' -Duplicate')]:
					key.update({'value_orig':size_value_dict[key['Attribute_1_size']] })
					key.update({'color_value_orig':color_value_dict[key['Attribute_2_color']] })
					value_ids = [
						sock.execute(dbname, 2, password, 'product.template', "prod_template_create_attrs", product_tmpl_id,
									 key)]

				prod_variant_domain = [('product_tmpl_id', '=', product_tmpl_id[0]),
									   ('name', '=',(line[1] + ' -Duplicate')),]
				product_id = sock.execute(dbname, 2, password, 'product.product', "search",
											prod_variant_domain)
				if product_id:
					barcode_key = line[2]+ '-Duplicate'
					barcode = barcode_value_dict[barcode_key]
					barcode_update = sock.execute(dbname, 2, password, 'product.barcode', "write",
													[barcode_value_dict[barcode_key]],
													{"product_id": product_id[0], 'product_tmpl_id': product_tmpl_id[0]})
					product_variant_update = sock.execute(dbname, 2, password, 'product.product', "write",
															product_id, {"default_code": line[3]})
				else:
					product_tmpl_vals = {
						'attribute_line_ids': variant_vals,
						'product_tmpl_id': product_tmpl_id[0],
						'size_attribute_value_id': size_value_dict.get(line[4]),
						'color_attribute_value_id': color_value_dict.get(line[5]),
						'size_id': size_attribute_id[0],
						'size_value_id': size_value_dict.get(line[4]),
						'color_id': color_attribute_id[0],
						'color_value_id': color_value_dict.get(line[5]),
					}
					product_tmpl_id = [sock.execute(dbname, 2, password, 'product.template', "product_templ_create_sql_xmlrpc", [],
								 product_tmpl_vals)]
		except:
			not_found.append(line[1])
