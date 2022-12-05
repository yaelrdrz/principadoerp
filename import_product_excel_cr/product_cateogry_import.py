import xmlrpc.client as xmlrpclib
import csv
import logging

_logger = logging.getLogger(__name__)

# filelist = ['/home/hardik/workspace/cr/principadoerp/import_product_excel_cr/principado_product/final_catalogue_141022_latest.csv']
filelist = ['/home/odoo/src/user/import_product_excel_cr/principado_product/final_catalogue_141022_latest.csv']
# filelist = ['/home/odoo/src/user/import_product_excel_cr/principado_product/final_catalogue_141022_latest.csv']
not_found = []
missing_product_categ = []
for filepath in filelist:
    file = open(filepath)
    file1 = open(filepath)
    reader = csv.DictReader(file, delimiter=",")
    reader_categ = csv.DictReader(file1, delimiter=",")
    db_name = "yaelrdrz-principadoerp-main-5969988"
    # db_name = "db_principado15"
    db_password = "AdM1nPr1nc."
    server = xmlrpclib.ServerProxy('https://principado.odoo.com/xmlrpc/object', allow_none=True)
    # server = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object',allow_none=True)
    final_dict = {}
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
    for line in reader:
        # print("-------line--------", line)
        # if final_dict and line['Product_template_name'] in [x['tmpl_name'] for x in final_dict]:
        #     continue
        # else:
        #     final_name = line['Product_template_name'] + '(Tamaño:' + line['Attribute_1_size'] + ',Color:' + line[
        #         'Attribute_2_color'] + ')'
        #     # print('0000',final_name)
        #     final_dict.append(
        #         {'tmpl_name': final_name,
        #          'Variant_internal_reference': line['Variant_internal_reference'],
        #          'Attribute_1_size': line['Attribute_1_size'], 'Attribute_2_color': line['Attribute_2_color'],
        #          'Product_category_1': line['Product_category_1'],
        #          'Product_category_2': line['Product_category_2'], 'Product_category_3': line['Product_category_3'],
        #          'Product_category_4': line['Product_category_4'], 'Product_category_5': line['Product_category_5'],
        #          'Product_category_6': line['Product_category_6'], 'Product_category_7': line['Product_category_7'],
        #          'Product_category_8': line['Product_category_8'], 'Product_category_9': line['Product_category_9'],
        #          'Product_category_10': line['Product_category_10']})
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



    print("------product_categ_1---------",product_categ_1)
    print("------product_categ_2---------",len(product_categ_2))
    print("------product_categ_3---------",len(product_categ_3))
    print("------product_categ_4---------",len(product_categ_4))
    print("------product_categ_5---------",len(product_categ_5))
    print("------product_categ_6---------",len(product_categ_6))
    print("------product_categ_7---------",len(product_categ_7))
    print("------product_categ_8---------",len(product_categ_8))
    print("------product_categ_9---------",len(product_categ_9))
    print("------product_categ_10---------",len(product_categ_10))
    categ_dict = {}
    for cat in product_categ_1+product_categ_2+product_categ_3+product_categ_4+product_categ_5+product_categ_6+product_categ_7+product_categ_8+product_categ_9+product_categ_10:
        categ_id = server.execute(db_name, 2, db_password, 'product.category', "create",
                                  {'name': cat, 'property_cost_method': 'average',
                                   'property_valuation': 'real_time'})
        if categ_id:
            categ_dict.update({cat:categ_id})
    main_categ_data = []
    for categ_line in reader_categ:
        # print("---------categ_line--------",categ_line)
        if main_categ_data and categ_line['Product_template_name'] in [x['Product_template_name'] for x in main_categ_data] and \
            categ_line['Variant_internal_reference'] in [x['Variant_internal_reference'] for x in main_categ_data] and \
            categ_line['Attribute_1_size'] in [x['Attribute_1_size'] for x in main_categ_data] and \
            categ_line['Attribute_2_color'] in [x['Attribute_2_color'] for x in main_categ_data]:
            continue
        else:
            main_categ_data.append({
                "Product_template_name": categ_line['Product_template_name'],
                "Variant_internal_reference": categ_line["Variant_internal_reference"],
                "Attribute_1_size": categ_line["Attribute_1_size"],
                "Attribute_2_color": categ_line["Attribute_2_color"],
                "main_line": categ_line
            })
    print("-------main_categ_data------------",len(main_categ_data))
    for ll in main_categ_data:
        try:
            if ll['main_line']['Product_category_1'] and ll['main_line']['Product_category_2']:
                server.execute(db_name, 2, db_password, 'product.category', "write",[categ_dict.get(ll['main_line']['Product_category_2'])],
                                          {'parent_id': categ_dict.get(ll['main_line']['Product_category_1'])})
            if ll['main_line']['Product_category_2'] and ll['main_line']['Product_category_3']:
                server.execute(db_name, 2, db_password, 'product.category', "write",[categ_dict.get(ll['main_line']['Product_category_3'])],
                                          {'parent_id': categ_dict.get(ll['main_line']['Product_category_2'])})
            if ll['main_line']['Product_category_3'] and ll['main_line']['Product_category_4']:
                server.execute(db_name, 2, db_password, 'product.category', "write",[categ_dict.get(ll['main_line']['Product_category_4'])],
                                          {'parent_id': categ_dict.get(ll['main_line']['Product_category_3'])})
            if ll['main_line']['Product_category_4'] and ll['main_line']['Product_category_5']:
                server.execute(db_name, 2, db_password, 'product.category', "write",[categ_dict.get(ll['main_line']['Product_category_5'])],
                                          {'parent_id': categ_dict.get(ll['main_line']['Product_category_4'])})
            if ll['main_line'].get('Product_category_5') and ll['main_line'].get('Product_category_6'):
                server.execute(db_name, 2, db_password, 'product.category', "write",[categ_dict.get(ll['main_line']['Product_category_6'])],
                                          {'parent_id': categ_dict.get(ll['main_line']['Product_category_5'])})
            if ll['main_line'].get('Product_category_6') and ll['main_line'].get('Product_category_7'):
                server.execute(db_name, 2, db_password, 'product.category', "write",[categ_dict.get(ll['main_line']['Product_category_7'])],
                                          {'parent_id': categ_dict.get(ll['main_line']['Product_category_6'])})
            if ll['main_line'].get('Product_category_7') and ll['main_line'].get('Product_category_8'):
                server.execute(db_name, 2, db_password, 'product.category', "write",[categ_dict.get(ll['main_line']['Product_category_8'])],
                                          {'parent_id': categ_dict.get(ll['main_line']['Product_category_7'])})
            if ll['main_line'].get('Product_category_8') and ll['main_line'].get('Product_category_9'):
                server.execute(db_name, 2, db_password, 'product.category', "write",[categ_dict.get(ll['main_line']['Product_category_9'])],
                                          {'parent_id': categ_dict.get(ll['main_line']['Product_category_8'])})
            if ll['main_line'].get('Product_category_9') and ll['main_line'].get('Product_category_10'):
                server.execute(db_name, 2, db_password, 'product.category', "write",[categ_dict.get(ll['main_line']['Product_category_10'])],
                                          {'parent_id': categ_dict.get(ll['main_line']['Product_category_9'])})
        except:
            missing_product_categ.append(ll['main_line'])

print("-----------missing_product_categ-----------", missing_product_categ)
