import xmlrpc.client as xmlrpclib
import csv
import logging
_logger = logging.getLogger(__name__)
# filelist = ["/home/hardik/workspace/cr/principadoerp/import_product_excel_cr/principado_product/final_catalogue_141022.csv"]
filelist = ["/home/hardik/workspace/cr/principadoerp/import_product_excel_cr/principado_product/test_principado.csv"]


missing_barcode_filelist = ["/home/hardik/workspace/cr/principadoerp/import_product_excel_cr/principado_product/missing_barcode_file.csv"]
missing_file = open(missing_barcode_filelist[0])
missing_barcode_reader = csv.DictReader(missing_file,delimiter=",")
missing_barcode_reader_list = [x['Barcode'] for x in missing_barcode_reader]
print("------missing_barcode_reader_list-------",len(missing_barcode_reader_list))
not_found = []
db_name = "db_principado15"
# db_name = "yaelrdrz-principadoerp-main-5969988"
db_password = "admin"
# server = xmlrpclib.ServerProxy('https://principado.odoo.com/xmlrpc/object',allow_none=True)
server = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object',allow_none=True)
for filepath in filelist:
    file = open(filepath)
    reader = csv.DictReader(file,delimiter=",")
    product_template_list = []
    #Create Attribute
    # size_vals = {"name": "Size","display_type": "select","create_variant": "always","visibility" : "visible"}
    # color_vals = {"name": "Color","display_type": "color","create_variant": "always","visibility" : "visible"}
    size_attribute_id = server.execute(db_name, 2, db_password, 'product.attribute', "search", [('name','=','Size')])
    # if not size_attribute_id:
    #     size_attribute_id = [server.execute(db_name, 2, db_password, 'product.attribute', "create", size_vals)]
    color_attribute_id = server.execute(db_name, 2, db_password, 'product.attribute', "search", [('name','=','Color')])
    # if not color_attribute_id:
    #     color_attribute_id = [server.execute(db_name, 2, db_password, 'product.attribute', "create", color_vals)]
    print("--------size_attribute_id-------",size_attribute_id)
    print("--------color_attribute_id-------",color_attribute_id)
    #Create Size,Color & Barcode Attribute
    final_dict = {}
    # temp_missing_barcode_list = []
    # for line in reader:
    #     # print("-------line---------------",line['Barcode'])
    #     if line['Barcode'] in missing_barcode_reader_list:
    #         temp_missing_barcode_list.append(line)
    # print("------temp_missing_barcode_list------",len(temp_missing_barcode_list))
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
    count = 0
    for k,v in final_dict.items():
        prod_tmpl_dict = {}
        # print("----------k----------------",k,v)
        try:
            product_tmpl_id = server.execute(db_name, 2, db_password, 'product.template', "search",[('name', '=', k)])
            if product_tmpl_id:
                for line_2 in v:
                    for bb in line_2['Barcodes']:
                        if bb in missing_barcode_reader_list:
                            print("-----------missing----------",k)
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
                            if product_template_size_attribute_value_id and product_template_color_attribute_value_id:
                                prod_variant_domain = [('product_tmpl_id', '=', product_tmpl_id[0]),
                                                       ('name', '=', k),
                                                       ('product_template_attribute_value_ids', 'in',
                                                        [product_template_size_attribute_value_id[-1]]),
                                                       ('product_template_attribute_value_ids', 'in',
                                                        [product_template_color_attribute_value_id[-1]])]
                                product_id = server.execute(db_name, 2, db_password, 'product.product', "search",
                                                            prod_variant_domain)
                                print("--------product_id---------",product_id)
                                if product_id:
                                    count += 1
                                    barcode_search = server.execute(db_name, 2, db_password, 'product.barcode', "search",[('barcode','in',line_2['Barcodes'])])
                                    print("--------barcode_search-----------",barcode_search)
                                    barcode_update = server.execute(db_name, 2, db_password, 'product.barcode', "write",barcode_search,{"product_id": product_id[0]})
                                    product_variant_update = server.execute(db_name, 2, db_password, 'product.product', "write",
                                                                            product_id,{"default_code": line_2['Variant_internal_reference']})
        except:
            not_found.append(k)
print("-----------not_found-----------",not_found,count)