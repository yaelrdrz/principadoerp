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

with open('/home/odoo/src/user/import_product_excel_cr/principado_product/final_catalogue_141022_latest.csv', mode='r')as file:
    reader = csv.reader(file)
    raw_data = [x for x in reader]

    for line in raw_data[1:]:
        size_value_id = sock.execute(dbname, 2, password, 'product.attribute.value', "search",
                                     [('name', '=', line[4]), ('attribute_id', '=', 10)])

        color_value_id = sock.execute(dbname, 2, password, 'product.attribute.value', "search",
                                      [('name', '=', line[5]), ('attribute_id', '=', 11)])


        name_read = sock.execute_kw(dbname, 2, password,
                          'product.product', 'search_read',
                          [[
                                            ('size_attribute_value_id', 'in', [size_value_id[0]] ),
                                            ('color_attribute_value_id', 'in', [color_value_id[0]])
                                            ]],
                          {'fields': ['product_tmpl_id', 'name']})
        if name_read and name_read[0]['name'] == line[1] + ' -Duplicate':
            barcode_id = sock.execute(dbname, 2, password, 'product.barcode', "search", [('barcode', '=', line[2] + '-Duplicate')])
            barcode_update = sock.execute(dbname, 2, password, 'product.barcode', "write",
                                          [barcode_id[0]],
                                          {"product_id": name_read[0]['id'],
                                           'product_tmpl_id': name_read[0]['product_tmpl_id'][0]})
            product_variant_update = sock.execute(dbname, 2, password, 'product.product', "write",
                                                  [name_read[0]['id']], {"default_code": line[3]})
        _logger.info('line number ------------------->>>>%s', line[0])
        print (line[0])

