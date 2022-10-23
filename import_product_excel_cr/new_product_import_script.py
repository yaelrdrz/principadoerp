import xmlrpc.client as xmlrpclib
import csv
import logging
_logger = logging.getLogger(__name__)
# filelist = ['/home/odoo/src/user/import_product_excel_cr/principado_product/final_catalogue_141022_latest.csv']
filelist = ['/home/hardik/workspace/cr/principadoerp/import_product_excel_cr/principado_product/test.csv']
not_found = []
missing_unspsc_categ = []
for filepath in filelist:
    file_size = open(filepath)
    file_color = open(filepath)
    file_barcode = open(filepath)
    file_unspsc = open(filepath)
    file_vendor = open(filepath)
    file_uom = open(filepath)
    file = open(filepath)

    reader_size = csv.DictReader(file_size,delimiter=",")
    reader_color = csv.DictReader(file_color,delimiter=",")
    reader_barcode = csv.DictReader(file_barcode,delimiter=",")
    reader_unspsc = csv.DictReader(file_unspsc,delimiter=",")
    reader_vendor = csv.DictReader(file_vendor,delimiter=",")
    reader_uom = csv.DictReader(file_uom,delimiter=",")
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
    uom_list = [x['Unit_of_measure'] for x in reader_uom]
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
    unspsc_value_dict = {}
    vendor_value_dict = {}
    uom_value_dict = {}
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
    for uom in list(set(uom_list)):
        uom_value_dict.update({uom: 1})
    for barcode in list(set(barcode_list)):
        barcode_id = server.execute(db_name, 2, db_password, 'product.barcode', "search", [('barcode','=',barcode)])
        if not barcode_id:
            barcode_id = [server.execute(db_name, 2, db_password, 'product.barcode', "create",{'barcode': barcode})]
        barcode_value_dict.update({barcode: barcode_id[0]})
    final_dict = {}
    tmpl_price = {}
    tmpl_unspsc_dict = {}
    tmpl_vendor_dict = {}
    for line in reader:
        if final_dict and line['Product_template_name'] in final_dict.keys():
            for k_dict, v_dict in final_dict.items():
                if k_dict == line['Product_template_name']:
                    if line['Attribute_1_size'] in [x['Attribute_1_size'] for x in v_dict] and line['Attribute_2_color'] in [x['Attribute_2_color'] for x in v_dict]:
                        match_found = False
                        for v_bar_dict in v_dict:
                            if v_bar_dict['Attribute_1_size'] == line['Attribute_1_size'] and v_bar_dict['Attribute_2_color'] == line['Attribute_2_color']:
                                v_bar_dict['Barcodes'].append(line['Barcode'])
                                match_found = True
                        if not match_found:
                            v_dict.append({'Attribute_1_size': line['Attribute_1_size'],'Attribute_2_color': line['Attribute_2_color'],
                                           'Variant_internal_reference': line['Variant_internal_reference'],
                                           'Barcodes': [line['Barcode']]})
                    else:
                        v_dict.append(
                            {'Attribute_1_size': line['Attribute_1_size'], 'Attribute_2_color': line['Attribute_2_color'],
                             'Variant_internal_reference': line['Variant_internal_reference'],
                             'Barcodes': [line['Barcode']]})
        else:
            final_dict.update({line['Product_template_name']: [{'Attribute_1_size': line['Attribute_1_size'],'Attribute_2_color': line['Attribute_2_color'],
                                                                'Variant_internal_reference': line['Variant_internal_reference'],
                                                                'Barcodes': [line['Barcode']]}]})
            tmpl_price.update({line['Product_template_name']: line['Unit price']})
            tmpl_unspsc_dict.update({line['Product_template_name']: unspsc_value_dict.get(line['UNSPSC_Category'])})
            tmpl_vendor_dict.update({line['Product_template_name']: vendor_value_dict.get(line['Provider'])})
    for k,v in final_dict.items():
        prod_tmpl_dict = {}
        print("----------k----------------",k)
        # print("----------v----------------",v)
        # already_created = True
        try:
            product_tmpl_id = server.execute(db_name, 2, db_password, 'product.template', "search",[('name', '=', k)])
            if not product_tmpl_id:
                variant_vals = [(0,0,{'attribute_id':size_attribute_id[0],'value_ids': [size_value_dict.get(x['Attribute_1_size']) for x in v if x.get('Attribute_1_size')]}),
                                (0,0,{'attribute_id':color_attribute_id[0],'value_ids': [color_value_dict.get(x['Attribute_2_color']) for x in v if x.get('Attribute_2_color')]})]
                product_tmpl_vals = {
                    "name": k,
                    'available_in_pos': True,
                    'type': 'product',
                    'website_published': True,
                    'tracking': 'lot',
                    "list_price": tmpl_price.get(k),
                    'sale_ok': True,
                    'purchase_ok': True,
                    'invoice_policy': 'order',
                    'purchase_method': 'purchase',
                    # 'unspsc_code_id': unspsc_value_dict.get(line['UNSPSC_Category']),
                    'unspsc_code_id': tmpl_unspsc_dict.get(k),
                    'attribute_line_ids': variant_vals,
                    'seller_ids': vendor_value_dict and [
                        (0, 0, {'name': tmpl_vendor_dict.get(k), 'min_qty': 1.0})],
                }
                product_tmpl_id = [server.execute(db_name, 2, db_password, 'product.template', "create", product_tmpl_vals)]
                already_created = False
            if product_tmpl_id:
                for line_2 in v:
                    # print("-------product_id-------------", line_2)
                    product_template_size_attribute_value_id = server.execute(db_name, 2, db_password,
                                                                              'product.template.attribute.value',
                                                                              "search", [('attribute_id','=',size_attribute_id[0]),('product_tmpl_id', '=',
                                                                                          product_tmpl_id[0]), (
                                                                                         'name', '=',
                                                                                         line_2['Attribute_1_size'])])
                    product_template_color_attribute_value_id = server.execute(db_name, 2, db_password,
                                                                               'product.template.attribute.value',
                                                                               "search", [('attribute_id','=',color_attribute_id[0]),('product_tmpl_id', '=',
                                                                                           product_tmpl_id[0]), (
                                                                                          'name', '=',
                                                                                          line_2['Attribute_2_color'])])
                    # print("----------product_template_size_attribute_value_id-------",product_template_size_attribute_value_id)
                    # print("----------product_template_color_attribute_value_id-------",product_template_color_attribute_value_id)
                    if product_template_size_attribute_value_id and product_template_color_attribute_value_id:
                        prod_variant_domain = [('product_tmpl_id', '=', product_tmpl_id[0]),
                                               ('name', '=', k),
                                               ('product_template_attribute_value_ids', 'in',
                                                [product_template_size_attribute_value_id[-1]]),
                                               ('product_template_attribute_value_ids', 'in',
                                                [product_template_color_attribute_value_id[-1]])]
                        # print("--------prod_variant_domain----------",prod_variant_domain)
                        product_id = server.execute(db_name, 2, db_password, 'product.product', "search",
                                                    prod_variant_domain)
                        # print("-------product_id-------------",product_id)
                        if product_id:
                            barcode_update = server.execute(db_name, 2, db_password, 'product.barcode', "write",
                                                            [barcode_value_dict.get(x) for x in line_2['Barcodes']],
                                                            {"product_id": product_id[0]})
                            product_variant_update = server.execute(db_name, 2, db_password, 'product.product', "write",
                                                                    product_id,{"default_code": line_2['Variant_internal_reference']})
            # attribute_line_not_created = True
            # for line in v:
            #     if attribute_line_not_created:
            #         size_attribute_line_id = [server.execute(db_name, 2, db_password, 'product.template.attribute.line', "create",{'product_tmpl_id': product_tmpl_id[0],'attribute_id':size_attribute_id[0],'value_ids': [size_value_dict.get(line['Attribute_1_size'])]})]
            #         color_attribute_line_id = [server.execute(db_name, 2, db_password, 'product.template.attribute.line', "create",{'product_tmpl_id': product_tmpl_id[0],'attribute_id':color_attribute_id[0],'value_ids': [color_value_dict.get(line['Attribute_2_color'])]})]
            #         prod_tmpl_dict.update({product_tmpl_id[0] : {'size_id': size_attribute_line_id[0],'color_id': color_attribute_line_id[0]}})
            #         attribute_line_not_created = False
            #     else:
            #         size_attribute_update = server.execute(db_name, 2, db_password, 'product.template.attribute.line', "write",[prod_tmpl_dict.get(product_tmpl_id[0]).get("size_id")],{'value_ids': [(4,size_value_dict.get(line['Attribute_1_size']))]})
            #         color_attribute_update = server.execute(db_name, 2, db_password, 'product.template.attribute.line', "write",[prod_tmpl_dict.get(product_tmpl_id[0]).get("color_id")],{'value_ids': [(4,color_value_dict.get(line['Attribute_2_color']))]})
        except:
            not_found.append(k)
print("-----------not_found-----------",not_found)
print("-----------missing_unspsc_categ-----------",missing_unspsc_categ)