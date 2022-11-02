import xmlrpc.client as xmlrpclib
import csv
import logging
_logger = logging.getLogger(__name__)
# filelist = ['/home/odoo/src/user/import_product_excel_cr/principado_product/final_catalogue_141022_latest.csv']
filelist = ['/home/hardik/workspace/cr/principadoerp/import_product_excel_cr/principado_product/final_catalogue_141022_latest.csv']
not_found = []
for filepath in filelist:
    file = open(filepath)
    reader = csv.DictReader(file,delimiter=",")
    db_name = "yaelrdrz-principadoerp-main-5969988"
    # db_name = "db_principado15"
    db_password = "admin"
    server = xmlrpclib.ServerProxy('https://principado.odoo.com/xmlrpc/object',allow_none=True)
    # server = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object',allow_none=True)
    file_size = open(filepath)
    file_color = open(filepath)
    reader_size = csv.DictReader(file_size, delimiter=",")
    reader_color = csv.DictReader(file_color, delimiter=",")
    size_list = [x['Attribute_1_size'] for x in reader_size]
    color_list = [x['Attribute_2_color'] for x in reader_color]

    size_vals = {"name": "Size", "display_type": "select", "create_variant": "always", "visibility": "visible"}
    color_vals = {"name": "Color", "display_type": "color", "create_variant": "always", "visibility": "visible"}
    size_attribute_id = server.execute(db_name, 2, db_password, 'product.attribute', "search", [('name', '=', 'Size')])
    if not size_attribute_id:
        size_attribute_id = [server.execute(db_name, 2, db_password, 'product.attribute', "create", size_vals)]
    color_attribute_id = server.execute(db_name, 2, db_password, 'product.attribute', "search",
                                        [('name', '=', 'Color')])
    if not color_attribute_id:
        color_attribute_id = [server.execute(db_name, 2, db_password, 'product.attribute', "create", color_vals)]

    size_value_dict = {}
    color_value_dict = {}
    barcode_value_dict = {}
    for size in list(set(size_list)):
        size_value_id = server.execute(db_name, 2, db_password, 'product.attribute.value', "search",
                                       [('name', '=', size), ('attribute_id', '=', size_attribute_id[0])])
        if not size_value_id:
            size_value_id = [server.execute(db_name, 2, db_password, 'product.attribute.value', "create",
                                            {'name': size, 'attribute_id': size_attribute_id[0]})]
        size_value_dict.update({size: size_value_id[0]})
    for color in list(set(color_list)):
        color_value_id = server.execute(db_name, 2, db_password, 'product.attribute.value', "search",
                                        [('name', '=', color), ('attribute_id', '=', color_attribute_id[0])])
        if not color_value_id:
            color_value_id = [server.execute(db_name, 2, db_password, 'product.attribute.value', "create",
                                             {'name': color, 'attribute_id': color_attribute_id[0]})]
        color_value_dict.update({color: color_value_id[0]})


    missing_uom_lines = []
    for l in reader:
        if l['Unit_of_measure'] == "Par":
            missing_uom_lines.append(l)
    print("------missin---26-----",len(missing_uom_lines))
    for line in missing_uom_lines:
        product_tmpl_id = server.execute(db_name, 2, db_password, 'product.template', "product_search_sql_xmlrpc",
                                         [], line['Product_template_name'], line['Variant_internal_reference'],
                                         size_value_dict.get(line['Attribute_1_size']),
                                         color_value_dict.get(line['Attribute_2_color']))
        print("-----product_tmpl_id---search----", product_tmpl_id)
        if product_tmpl_id:
            product_update = server.execute(db_name, 2, db_password, 'product.template', "write",
                                            product_tmpl_id,
                                            {"uom_id": 26,'uom_po_id':26})