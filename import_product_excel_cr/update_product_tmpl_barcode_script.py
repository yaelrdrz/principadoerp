import xmlrpc.client as xmlrpclib
import csv
import logging
_logger = logging.getLogger(__name__)
filelist = ['/home/odoo/src/user/import_product_excel_cr/principado_product/final_catalogue_141022_latest.csv']
# filelist = ['/home/hardik/workspace/cr/principadoerp/import_product_excel_cr/principado_product/import_product_1.csv']
# filelist = ['/home/hardik/workspace/cr/principadoerp/import_product_excel_cr/principado_product/final_catalogue_141022_latest.csv']
not_found = []

missing_unspsc_categ = []
for filepath in filelist:
    file_size = open(filepath)
    file_color = open(filepath)
    file_barcode = open(filepath)
    file = open(filepath)
    reader_size = csv.DictReader(file_size,delimiter=",")
    reader_color = csv.DictReader(file_color,delimiter=",")
    reader_barcode = csv.DictReader(file_barcode, delimiter=",")
    reader = csv.DictReader(file,delimiter=",")
    db_name = "yaelrdrz-principadoerp-main-5969988"
    # db_name = "db_principado15"
    db_password = "admin"
    server = xmlrpclib.ServerProxy('https://principado.odoo.com/xmlrpc/object',allow_none=True)
    # server = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object',allow_none=True)
    product_template_list = []
    size_list = [x['Attribute_1_size'] for x in reader_size]
    color_list = [x['Attribute_2_color'] for x in reader_color]
    barcode_list = [x['Barcode'] for x in reader_barcode]
    #Create Attribute
    size_vals = {"name": "Size","display_type": "select","create_variant": "always","visibility" : "visible"}
    color_vals = {"name": "Color","display_type": "color","create_variant": "always","visibility" : "visible"}
    size_attribute_id = server.execute(db_name, 2, db_password, 'product.attribute', "search", [('name','=','Size')])
    if not size_attribute_id:
        size_attribute_id = [server.execute(db_name, 2, db_password, 'product.attribute', "create", size_vals)]
    color_attribute_id = server.execute(db_name, 2, db_password, 'product.attribute', "search", [('name','=','Color')])
    if not color_attribute_id:
        color_attribute_id = [server.execute(db_name, 2, db_password, 'product.attribute', "create", color_vals)]
    #Create Size,Color & Barcode Attribute
    size_value_dict = {}
    color_value_dict = {}
    barcode_value_dict = {}
    for size in list(set(size_list)):
        size_value_id = server.execute(db_name, 2, db_password, 'product.attribute.value', "search", [('name','=',size),('attribute_id','=',size_attribute_id[0])])
        if not size_value_id:
            size_value_id = [server.execute(db_name, 2, db_password, 'product.attribute.value', "create",{'name': size, 'attribute_id': size_attribute_id[0]})]
        size_value_dict.update({size:size_value_id[0]})
    print("--------size------done-------")
    for color in list(set(color_list)):
        color_value_id = server.execute(db_name, 2, db_password, 'product.attribute.value', "search", [('name','=',color),('attribute_id','=',color_attribute_id[0])])
        if not color_value_id:
            color_value_id = [server.execute(db_name, 2, db_password, 'product.attribute.value', "create",{'name': color, 'attribute_id': color_attribute_id[0]})]
        color_value_dict.update({color: color_value_id[0]})
    print("--------color------done-------")
    for barcode in list(set(barcode_list)):
        barcode_id = server.execute(db_name, 2, db_password, 'product.barcode', "search", [('barcode','=',barcode)])
        if not barcode_id:
            barcode_id = [server.execute(db_name, 2, db_password, 'product.barcode', "create",{'barcode': barcode})]
        barcode_value_dict.update({barcode: barcode_id[0]})
    print("--------barcode------done-------")
    all_lines = []
    for line_read in reader:
        all_lines.append(line_read)
    all_lines.reverse()
    print("--------read------done-------")
    for line in all_lines:
        try:
            product_tmpl_id = server.execute(db_name, 2, db_password, 'product.template', "product_search_sql_xmlrpc",
                                             [], line['Product_template_name'], line['Variant_internal_reference'], size_value_dict.get(line['Attribute_1_size']), color_value_dict.get(line['Attribute_2_color']))
            # print("-----product_tmpl_id---search----", product_tmpl_id)
            if product_tmpl_id:
                barcode_update = server.execute(db_name, 2, db_password, 'product.barcode', "write",
                                                [barcode_value_dict.get(line['Barcode'])],
                                                {"product_tmpl_id": product_tmpl_id[0]})
        except:
            not_found.append({"tmpl_name": line['Product_template_name'],"size": line['Attribute_1_size'],"color": line['Attribute_2_color'],"price": line['Unit price']})
print("-----------not_found-----------",not_found)