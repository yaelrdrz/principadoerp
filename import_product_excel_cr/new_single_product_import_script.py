import xmlrpc.client as xmlrpclib
import csv
import logging
_logger = logging.getLogger(__name__)
filelist = ['/home/odoo/src/user/import_product_excel_cr/principado_product/final_catalogue_141022_latest.csv']
# filelist = ['/home/hardik/workspace/cr/principadoerp/import_product_excel_cr/principado_product/final_catalogue_141022_latest.csv']
not_found = []
missing_unspsc_categ = []
for filepath in filelist:
    file_size = open(filepath)
    file_color = open(filepath)
    file_unspsc = open(filepath)
    file_barcode = open(filepath)
    file_vendor = open(filepath)
    file = open(filepath)
    reader_size = csv.DictReader(file_size,delimiter=",")
    reader_color = csv.DictReader(file_color,delimiter=",")
    reader_unspsc = csv.DictReader(file_unspsc,delimiter=",")
    reader_vendor = csv.DictReader(file_vendor,delimiter=",")
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
    unspsc_list = [x['UNSPSC_Category'] for x in reader_unspsc]
    vendor_list = [x['Provider'] for x in reader_vendor]
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
    unspsc_value_dict = {}
    vendor_value_dict = {}
    barcode_value_dict = {}
    for size in list(set(size_list)):
        size_value_id = server.execute(db_name, 2, db_password, 'product.attribute.value', "search", [('name','=',size),('attribute_id','=',size_attribute_id[0])])
        if not size_value_id:
            size_value_id = [server.execute(db_name, 2, db_password, 'product.attribute.value', "create",{'name': size, 'attribute_id': size_attribute_id[0]})]
        size_value_dict.update({size:size_value_id[0]})
    for color in list(set(color_list)):
        color_value_id = server.execute(db_name, 2, db_password, 'product.attribute.value', "search", [('name','=',color),('attribute_id','=',color_attribute_id[0])])
        if not color_value_id:
            color_value_id = [server.execute(db_name, 2, db_password, 'product.attribute.value', "create",{'name': color, 'attribute_id': color_attribute_id[0]})]
        color_value_dict.update({color: color_value_id[0]})
    for unspsc in list(set(unspsc_list)):
        unspsc_id = server.execute(db_name, 2, db_password, 'product.unspsc.code', "search",
                                   [('comp_name', '=like', unspsc)])
        if not unspsc_id:
            unspsc_split = unspsc.split("-")
            if len(unspsc_split) > 1:
                unspsc_id = server.execute(db_name, 2, db_password, 'product.unspsc.code', "search",
                                           [('code', '=like', unspsc_split[0])])
        if unspsc_id:
            unspsc_value_dict.update({unspsc: unspsc_id and unspsc_id[0] or False})
        else:
            missing_unspsc_categ.append(unspsc)
    for vendor in list(set(vendor_list)):
        vendor_id = server.execute(db_name, 2, db_password, 'res.partner', "search", [('name','=',vendor)])
        if not vendor_id:
            vendor_id = [server.execute(db_name, 2, db_password, 'res.partner', "create", {'name' : vendor})]
        vendor_value_dict.update({vendor: vendor_id[0]})
    # for barcode in list(set(barcode_list)):
    #     barcode_id = server.execute(db_name, 2, db_password, 'product.barcode', "search", [('barcode','=',barcode)])
    #     if not barcode_id:
    #         barcode_id = [server.execute(db_name, 2, db_password, 'product.barcode', "create",{'barcode': barcode})]
    #     barcode_value_dict.update({barcode: barcode_id[0]})
    all_lines = []
    for line_read in reader:
        all_lines.append(line_read)
    # line_count = 0
    for line in all_lines:
        # already_created = False
        # line_count += 1
        # print("line_count------------",line_count)
        try:
            # product_tmpl_id = server.execute(db_name, 2, db_password, 'product.template', "search_read",[('name', '=', line['Product_template_name']),
            #                                                                                         ('default_code', '=', line['Variant_internal_reference']),
            #                                                                                         ('size_attribute_value_id', '=', size_value_dict.get(line['Attribute_1_size'])),
            #                                                                                         ('color_attribute_value_id', '=', color_value_dict.get(line['Attribute_2_color'])),
            #                                                                                         ],['product_variant_id'])
            # product_tmpl_id = server.execute(db_name, 2, db_password, 'product.template', "search",[('name', '=', line['Product_template_name']),
            #                                                                                         ('default_code', '=', line['Variant_internal_reference']),
            #                                                                                         ('size_attribute_value_id', '=', size_value_dict.get(line['Attribute_1_size'])),
            #                                                                                         ('color_attribute_value_id', '=', color_value_dict.get(line['Attribute_2_color'])),
            #                                                                                         ])
            product_tmpl_id = server.execute(db_name, 2, db_password, 'product.template', "product_search_sql_xmlrpc",
                                             [], line['Product_template_name'], line['Variant_internal_reference'], size_value_dict.get(line['Attribute_1_size']), color_value_dict.get(line['Attribute_2_color']))
            print("-----product_tmpl_id-------", product_tmpl_id)
            if not product_tmpl_id:
                variant_vals = [(0,0,{'attribute_id':size_attribute_id[0],'value_ids': [size_value_dict.get(line['Attribute_1_size'])]}),
                                (0,0,{'attribute_id':color_attribute_id[0],'value_ids': [color_value_dict.get(line['Attribute_2_color'])]})]
                product_tmpl_vals = {
                    "name": line['Product_template_name'],
                    "default_code": line['Variant_internal_reference'],
                    "uom_id": 1,
                    'available_in_pos': True,
                    'type': 'product',
                    'website_published': True,
                    'tracking': 'lot',
                    "list_price": line['Unit price'],
                    'sale_ok': True,
                    'purchase_ok': True,
                    'invoice_policy': 'order',
                    'purchase_method': 'purchase',
                    'unspsc_code_id': unspsc_value_dict.get(line['UNSPSC_Category']),
                    'attribute_line_ids': variant_vals,
                    'seller_ids': vendor_value_dict and [(0, 0, {'name': vendor_value_dict.get(line['Provider']), 'min_qty': 1.0})],
                    'size_attribute_value_id': size_value_dict.get(line['Attribute_1_size']),
                    'color_attribute_value_id': color_value_dict.get(line['Attribute_2_color'])
                }
                product_tmpl_id = [server.execute(db_name, 2, db_password, 'product.template', "create", product_tmpl_vals)]
                # product_tmpl_id = server.execute(db_name, 2, db_password, 'product.template', "search",
                #                                  [('id', '=', tmpl_id)], ['product_variant_id'])
                # already_created = True
            # print("----------product_tmpl_id-----------",product_tmpl_id)
            # if product_tmpl_id and already_created:
            #     barcode_update = server.execute(db_name, 2, db_password, 'product.template',"product_search_sql_xmlrpc",
            #                                      [], line['Product_template_name']
            #     barcode_update = server.execute(db_name, 2, db_password, 'product.barcode', "write",
            #                                     [barcode_value_dict.get(x) for x in ],
            #                                     {"product_tmpl_id": product_tmpl_id[0]})
                # barcode_update = server.execute(db_name, 2, db_password, 'product.barcode', "create",{"barcode": line['Barcode'],
                #                                                                                       # "product_id": product_tmpl_id[0].get("product_variant_id")[0],
                #                                                                                       "product_tmpl_id":product_tmpl_id[0]})
        except:
            not_found.append({"tmpl_name": line['Product_template_name'],"size": line['Attribute_1_size'],"color": line['Attribute_2_color'],"price": line['Unit price']})
print("-----------not_found-----------",not_found)