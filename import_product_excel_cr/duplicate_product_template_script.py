import logging
from xmlrpc import client as xmlrpclib

_logger = logging.getLogger(__name__)
url = 'http://localhost:8069'
dbname = 'yaelrdrz-principadoerp-main-5969988'    #the database
username = 'admin'    #the user
password = 'AdM1nPr1nc.'

sock = xmlrpclib.ServerProxy('https://principado.odoo.com/xmlrpc/object', allow_none=True)

# product_tmpl_vals  = {'test': 'Test'}
# sock.execute(dbname, 2, password, 'product.template', "update_variant_value", [], product_tmpl_vals)
# template_ids = sock.execute(dbname, 2, password, 'product.template', "search", [('name','ilike','-Duplicate')])

import csv

with open('/home/erp/repo/principadoerp/import_product_excel_cr/final_catalogue_141022_latest.csv', mode='r')as file:
    reader = csv.reader(file)
    raw_data = [x for x in reader]
    barcode_value_dict = {}
    size_value_dict = {}
    color_value_dict = {}

    # Size attribute creation first-------------------------
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

    # color attribute creation first-------------------------
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
    barcode_list = [x[2] + '-Duplicate' for x in raw_data]
    for barcode in list(set(barcode_list[1:])):
        barcode_id = sock.execute(dbname, 2, password, 'product.barcode', "search", [('barcode', '=', barcode)])
        if not barcode_id:
            barcode_id = [sock.execute(dbname, 2, password, 'product.barcode', "create", {'barcode': barcode})]
        barcode_value_dict.update({barcode: barcode_id[0]})
    for line in raw_data[1:]:
        product_name_search = sock.execute(dbname, 2, password, 'product.product', "search",
                                           [
                                            ('size_attribute_value_id', 'in', [size_value_dict[line[4]]] ),
                                            ('color_attribute_value_id', 'in', [color_value_dict[line[5]]] )
                                            ])
        name_read = sock.execute_kw(dbname, 2, password,
                          'product.product', 'search_read',
                          [[
                              ['size_attribute_value_id', 'in', [size_value_dict[line[4]]]],
                              ['color_attribute_value_id', 'in', [color_value_dict[line[5]]]]
                               ]],
                          {'fields': ['product_tmpl_id', 'name']})
        if name_read and name_read[0]['name'] == line[1] + ' -Duplicate':
            barcode_key = line[2] + '-Duplicate'
            barcode = barcode_value_dict[barcode_key]
            barcode_update = sock.execute(dbname, 2, password, 'product.barcode', "write",
                                          [barcode_value_dict[barcode_key]],
                                          {"product_id": name_read[0]['id'],
                                           'product_tmpl_id': name_read[0]['product_tmpl_id'][0]})
            product_variant_update = sock.execute(dbname, 2, password, 'product.product', "write",
                                                  product_name_search, {"default_code": line[3]})
        _logger.info('line number ------------------->>>>%s', line[0])

