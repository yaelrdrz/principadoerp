import xmlrpc.client as xmlrpclib
import csv
import logging

_logger = logging.getLogger(__name__)

filelist = [
    '/home/erp/workspace/projects/v15e/principado/import_product_excel_cr/principado_product/test2.csv']
# filelist = ['/home/odoo/src/user/import_product_excel_cr/principado_product/final_catalogue_141022_latest.csv']
not_found = []
missing_product_categ = []
for filepath in filelist:
    file = open(filepath)
    file_size = open(filepath)
    file_color = open(filepath)
    reader = csv.DictReader(file, delimiter=",")
    reader_size = csv.DictReader(file_size, delimiter=",")
    reader_color = csv.DictReader(file_color, delimiter=",")
    db_name = "db_sltn_principado_15e"
    # db_name = "db_principado15"
    db_password = "admin"
    server = xmlrpclib.ServerProxy('http://localhost:8015/xmlrpc/object', allow_none=True)
    # server = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object',allow_none=True)

    final_dict = []
    size_value_dict = {}
    color_value_dict = {}
    size_list = [x['Attribute_1_size'] for x in reader_size]
    color_list = [x['Attribute_2_color'] for x in reader_color]
    product_categ_1 = []
    product_categ_2 = []
    product_categ_3 = []
    product_categ_4 = []
    product_categ_5 = []
    product_categ_6 = []
    product_categ_7 = []
    product_categ_8 = []
    product_categ_9 = []
    product_categ_10 = []
    size_vals = {"name": "Size", "display_type": "select", "create_variant": "always", "visibility": "visible"}
    color_vals = {"name": "Color", "display_type": "color", "create_variant": "always", "visibility": "visible"}
    size_attribute_id = server.execute(db_name, 2, db_password, 'product.attribute', "search", [('name', '=', 'Size')])
    if not size_attribute_id:
        size_attribute_id = [server.execute(db_name, 2, db_password, 'product.attribute', "create", size_vals)]
    color_attribute_id = server.execute(db_name, 2, db_password, 'product.attribute', "search",
                                        [('name', '=', 'Color')])
    if not color_attribute_id:
        color_attribute_id = [server.execute(db_name, 2, db_password, 'product.attribute', "create", color_vals)]

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
    for line in reader:
        # print("-------line--------", line)
        if final_dict and line['Product_template_name'] in [x['tmpl_name'] for x in final_dict]:
            continue
        else:
            final_name = line['Product_template_name'] + '(Tamaño:' + line['Attribute_1_size'] + ',Color:' + line[
                'Attribute_2_color'] + ')'
            # print('0000',final_name)
            final_dict.append(
                {'tmpl_name': final_name,
                 'Variant_internal_reference': line['Variant_internal_reference'],
                 'Attribute_1_size': line['Attribute_1_size'], 'Attribute_2_color': line['Attribute_2_color'],
                 'Product_category_1': line['Product_category_1'],
                 'Product_category_2': line['Product_category_2'], 'Product_category_3': line['Product_category_3'],
                 'Product_category_4': line['Product_category_4'], 'Product_category_5': line['Product_category_5'],
                 'Product_category_6': line['Product_category_6'], 'Product_category_7': line['Product_category_7'],
                 'Product_category_8': line['Product_category_8'], 'Product_category_9': line['Product_category_9'],
                 'Product_category_10': line['Product_category_10']})
            if line['Product_category_1']:
                product_categ_1.append(line['Product_category_1'])
            if line['Product_category_2']:
                product_categ_2.append(line['Product_category_2'])
            if line['Product_category_3']:
                product_categ_3.append(line['Product_category_3'])
            if line['Product_category_4']:
                product_categ_4.append(line['Product_category_4'])
            if line['Product_category_5']:
                product_categ_5.append(line['Product_category_5'])
            if line['Product_category_6']:
                product_categ_6.append(line['Product_category_6'])
            if line['Product_category_7']:
                product_categ_7.append(line['Product_category_7'])
            if line['Product_category_8']:
                product_categ_8.append(line['Product_category_8'])
            if line['Product_category_9']:
                product_categ_9.append(line['Product_category_9'])
            if line['Product_category_10']:
                product_categ_10.append(line['Product_category_10'])
    product_categ_1 = list(set(product_categ_1))
    product_categ_2 = list(set(product_categ_2))
    product_categ_3 = list(set(product_categ_3))
    product_categ_4 = list(set(product_categ_4))
    product_categ_5 = list(set(product_categ_5))
    product_categ_6 = list(set(product_categ_6))
    product_categ_7 = list(set(product_categ_7))
    product_categ_8 = list(set(product_categ_8))
    product_categ_9 = list(set(product_categ_9))
    product_categ_10 = list(set(product_categ_10))
    # Categ 1
    product_categ_1_dict = {}
    for categ_1 in product_categ_1:
        categ_id_1 = server.execute(db_name, 2, db_password, 'product.category', "search", [('name', '=', categ_1)])
        if not categ_id_1:
            categ_id_1 = [server.execute(db_name, 2, db_password, 'product.category', "create",
                                         {'parent_id': 1, 'name': categ_1, 'property_cost_method': 'average',
                                          'property_valuation': 'real_time'})]
        product_categ_1_dict.update({categ_1: categ_id_1[0]})
    # categ 2
    product_categ_2_dict = {}
    for categ_2 in product_categ_2:
        categ_id_2 = server.execute(db_name, 2, db_password, 'product.category', "search", [('name', '=', categ_2)])
        if not categ_id_2:
            categ_id_2 = [server.execute(db_name, 2, db_password, 'product.category', "create",
                                         {'name': categ_2, 'property_cost_method': 'average',
                                          'property_valuation': 'real_time'})]
        product_categ_2_dict.update({categ_2: categ_id_2[0]})
    # categ 3
    product_categ_3_dict = {}
    for categ_3 in product_categ_3:
        categ_id_3 = server.execute(db_name, 2, db_password, 'product.category', "search", [('name', '=', categ_3)])
        if not categ_id_3:
            categ_id_3 = [server.execute(db_name, 2, db_password, 'product.category', "create",
                                         {'name': categ_3, 'property_cost_method': 'average',
                                          'property_valuation': 'real_time'})]
        product_categ_3_dict.update({categ_3: categ_id_3[0]})
    # categ 4
    product_categ_4_dict = {}
    for categ_4 in product_categ_4:
        categ_id_4 = server.execute(db_name, 2, db_password, 'product.category', "search", [('name', '=', categ_4)])
        if not categ_id_4:
            categ_id_4 = [server.execute(db_name, 2, db_password, 'product.category', "create",
                                         {'name': categ_4, 'property_cost_method': 'average',
                                          'property_valuation': 'real_time'})]
        product_categ_4_dict.update({categ_4: categ_id_4[0]})
    # categ 5
    product_categ_5_dict = {}
    for categ_5 in product_categ_5:
        categ_id_5 = server.execute(db_name, 2, db_password, 'product.category', "search", [('name', '=', categ_5)])
        if not categ_id_5:
            categ_id_5 = [server.execute(db_name, 2, db_password, 'product.category', "create",
                                         {'name': categ_5, 'property_cost_method': 'average',
                                          'property_valuation': 'real_time'})]
        product_categ_5_dict.update({categ_5: categ_id_5[0]})
    # categ 6
    product_categ_6_dict = {}
    for categ_6 in product_categ_6:
        categ_id_6 = server.execute(db_name, 2, db_password, 'product.category', "search", [('name', '=', categ_6)])
        if not categ_id_6:
            categ_id_6 = [server.execute(db_name, 2, db_password, 'product.category', "create",
                                         {'name': categ_6, 'property_cost_method': 'average',
                                          'property_valuation': 'real_time'})]
        product_categ_6_dict.update({categ_6: categ_id_6[0]})
    # categ 7
    product_categ_7_dict = {}
    for categ_7 in product_categ_7:
        categ_id_7 = server.execute(db_name, 2, db_password, 'product.category', "search", [('name', '=', categ_7)])
        if not categ_id_7:
            categ_id_7 = [server.execute(db_name, 2, db_password, 'product.category', "create",
                                         {'name': categ_7, 'property_cost_method': 'average',
                                          'property_valuation': 'real_time'})]
        product_categ_7_dict.update({categ_7: categ_id_7[0]})
    # categ 8
    product_categ_8_dict = {}
    for categ_8 in product_categ_8:
        categ_id_8 = server.execute(db_name, 2, db_password, 'product.category', "search", [('name', '=', categ_8)])
        if not categ_id_8:
            categ_id_8 = [server.execute(db_name, 2, db_password, 'product.category', "create",
                                         {'name': categ_8, 'property_cost_method': 'average',
                                          'property_valuation': 'real_time'})]
        product_categ_8_dict.update({categ_8: categ_id_8[0]})
    # categ 9
    product_categ_9_dict = {}
    for categ_9 in product_categ_9:
        categ_id_9 = server.execute(db_name, 2, db_password, 'product.category', "search", [('name', '=', categ_9)])
        if not categ_id_9:
            categ_id_9 = [server.execute(db_name, 2, db_password, 'product.category', "create",
                                         {'name': categ_9, 'property_cost_method': 'average',
                                          'property_valuation': 'real_time'})]
        product_categ_9_dict.update({categ_9: categ_id_9[0]})
    # categ 10
    product_categ_10_dict = {}
    for categ_10 in product_categ_10:
        categ_id_10 = server.execute(db_name, 2, db_password, 'product.category', "search", [('name', '=', categ_10)])
        if not categ_id_10:
            categ_id_10 = [server.execute(db_name, 2, db_password, 'product.category', "create",
                                          {'name': categ_10, 'property_cost_method': 'average',
                                           'property_valuation': 'real_time'})]
        product_categ_10_dict.update({categ_10: categ_id_10[0]})
    print("---------final---------", len(final_dict))
    for k in final_dict:
            print('in kkkkkkk')
        # try:
            product_tmpl_id = server.execute(db_name, 2, db_password, 'product.template', "product_search_sql_xmlrpc",
                                             [], k['tmpl_name'], k['Variant_internal_reference'],
                                             size_value_dict.get(k['Attribute_1_size']),
                                             color_value_dict.get(k['Attribute_2_color']))
            # print("-----name---search----", k['tmpl_name'])
            # print("-----k['Variant_internal_reference']---search----", k['Variant_internal_reference'])
            print("-----size_value_dict.get(k['Attribute_1_size']---search----", size_value_dict.get(k['Attribute_1_size']))
            # print("-----color_value_dict.get(k['Attribute_2_color'])---search----", color_value_dict.get(k['Attribute_2_color']))
            # product_tmpl_id = server.execute(db_name, 2, db_password, 'product.template', "search",
            #                                  [('name', '=', k['tmpl_name'])])
            print("-----product_tmpl_id---search----", product_tmpl_id)
            # print('-------', k['tmpl_name'])
            # print('-------template----', product_tmpl_id)
            prod_category_id = False
            csv_categ_count = ''
            if product_tmpl_id:
                print('------template_idssssssssss', product_tmpl_id)
                if k.get("Product_category_10"):
                    prod_category_id = product_categ_10_dict.get(k['Product_category_10'])
                    csv_categ_count = 'Product_category_10'
                if k.get("Product_category_9") and not prod_category_id:
                    prod_category_id = product_categ_9_dict.get(k['Product_category_9'])
                    csv_categ_count = 'Product_category_9'
                if k.get("Product_category_8") and not prod_category_id:
                    prod_category_id = product_categ_8_dict.get(k['Product_category_8'])
                    csv_categ_count = 'Product_category_8'
                if k.get("Product_category_7") and not prod_category_id:
                    prod_category_id = product_categ_7_dict.get(k['Product_category_7'])
                    csv_categ_count = 'Product_category_7'
                if k.get("Product_category_6") and not prod_category_id:
                    prod_category_id = product_categ_6_dict.get(k['Product_category_6'])
                    csv_categ_count = 'Product_category_6'
                if k.get("Product_category_5") and not prod_category_id:
                    prod_category_id = product_categ_5_dict.get(k['Product_category_5'])
                    csv_categ_count = 'Product_category_5'
                if k.get("Product_category_4") and not prod_category_id:
                    prod_category_id = product_categ_4_dict.get(k['Product_category_4'])
                    csv_categ_count = 'Product_category_4'
                if k.get("Product_category_3") and not prod_category_id:
                    prod_category_id = product_categ_3_dict.get(k['Product_category_3'])
                    csv_categ_count = 'Product_category_3'
                if k.get("Product_category_2") and not prod_category_id:
                    prod_category_id = product_categ_2_dict.get(k['Product_category_2'])
                    csv_categ_count = 'Product_category_2'
                if k.get("Product_category_1") and not prod_category_id:
                    prod_category_id = product_categ_1_dict.get(k['Product_category_1'])
                    csv_categ_count = 'Product_category_1'
                for i in range(10, 0, -1):
                    # print('------iiiiiiii', i)
                    i_match = int(csv_categ_count.split("_")[-1])
                    if i_match == i:
                        # print('------imatch------', i_match)
                        for j in range(i_match, 0, -1):
                            categ_dict_variable = "product_categ_%s_dict" % str(j)
                            update_categ_id = eval(categ_dict_variable).get(k["Product_category_" + str(j)])
                            if j != 1:
                                parent_categ_dict_variable = "product_categ_%s_dict" % str(j - 1)
                                parent_categ_id = eval(parent_categ_dict_variable).get(
                                    k["Product_category_" + str(j - 1)])
                            else:
                                parent_categ_dict_variable = "product_categ_%s_dict" % str(j)
                                parent_categ_id = eval(parent_categ_dict_variable).get(k["Product_category_" + str(j)])
                            # try:
                            if j == 1:
                                test = server.execute(db_name, 2, db_password, 'product.category', "write",
                                                      [update_categ_id], {'parent_id': 1})
                            else:
                                test = server.execute(db_name, 2, db_password, 'product.category', "write",
                                                          [update_categ_id], {'parent_id': parent_categ_id})
                            # except:
                                missing_product_categ.append(k['tmpl_name'])
                # stop
                if prod_category_id:
                    # print('-0---', prod_category_id)
                    server.execute(db_name, 2, db_password, 'product.template', "a",
                                   product_tmpl_id, {"categ_id": prod_category_id})
        # except:
        #     print("in e")
        #     not_found.append(k['tmpl_name'])
print("-----------not_found-----------", not_found)
print("-----------missing_product_categ-----------", missing_product_categ)
