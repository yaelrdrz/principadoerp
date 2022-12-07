import xmlrpc.client as xmlrpclib
import csv
import logging

_logger = logging.getLogger(__name__)

filelist = ['/home/odoo/src/user/import_product_excel_cr/principado_product/final_catalogue_141022_latest.csv']
# filelist = ['/home/hardik/workspace/cr/principadoerp/import_product_excel_cr/principado_product/final_catalogue_141022_latest.csv']
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
    # db_password = "admin"
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



    print("------product_categ_1---------",len(product_categ_1))
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
    for cat in product_categ_1:
        categ_id = server.execute(db_name, 2, db_password, 'product.category', "create",
                                  {'name': cat+"##product_categ_1", 'property_cost_method': 'average',
                                   'property_valuation': 'real_time'})
        if categ_id:
            categ_dict.update({cat+"##product_categ_1":categ_id})
    for cat in product_categ_2:
        categ_id = server.execute(db_name, 2, db_password, 'product.category', "create",
                                  {'name': cat+"##product_categ_2", 'property_cost_method': 'average',
                                   'property_valuation': 'real_time'})
        if categ_id:
            categ_dict.update({cat+"##product_categ_2":categ_id})
    for cat in product_categ_3:
        categ_id = server.execute(db_name, 2, db_password, 'product.category', "create",
                                  {'name': cat+"##product_categ_3", 'property_cost_method': 'average',
                                   'property_valuation': 'real_time'})
        if categ_id:
            categ_dict.update({cat+"##product_categ_3":categ_id})
    for cat in product_categ_4:
        categ_id = server.execute(db_name, 2, db_password, 'product.category', "create",
                                  {'name': cat+"##product_categ_4", 'property_cost_method': 'average',
                                   'property_valuation': 'real_time'})
        if categ_id:
            categ_dict.update({cat+"##product_categ_4":categ_id})
    for cat in product_categ_5:
        categ_id = server.execute(db_name, 2, db_password, 'product.category', "create",
                                  {'name': cat+"##product_categ_5", 'property_cost_method': 'average',
                                   'property_valuation': 'real_time'})
        if categ_id:
            categ_dict.update({cat+"##product_categ_5":categ_id})
    for cat in product_categ_6:
        categ_id = server.execute(db_name, 2, db_password, 'product.category', "create",
                                  {'name': cat+"##product_categ_6", 'property_cost_method': 'average',
                                   'property_valuation': 'real_time'})
        if categ_id:
            categ_dict.update({cat+"##product_categ_6":categ_id})
    for cat in product_categ_7:
        categ_id = server.execute(db_name, 2, db_password, 'product.category', "create",
                                  {'name': cat+"##product_categ_7", 'property_cost_method': 'average',
                                   'property_valuation': 'real_time'})
        if categ_id:
            categ_dict.update({cat+"##product_categ_7":categ_id})
    for cat in product_categ_8:
        categ_id = server.execute(db_name, 2, db_password, 'product.category', "create",
                                  {'name': cat+"##product_categ_8", 'property_cost_method': 'average',
                                   'property_valuation': 'real_time'})
        if categ_id:
            categ_dict.update({cat+"##product_categ_8":categ_id})
    for cat in product_categ_9:
        categ_id = server.execute(db_name, 2, db_password, 'product.category', "create",
                                  {'name': cat+"##product_categ_9", 'property_cost_method': 'average',
                                   'property_valuation': 'real_time'})
        if categ_id:
            categ_dict.update({cat+"##product_categ_9":categ_id})
    for cat in product_categ_10:
        categ_id = server.execute(db_name, 2, db_password, 'product.category', "create",
                                  {'name': cat+"##product_categ_10", 'property_cost_method': 'average',
                                   'property_valuation': 'real_time'})
        if categ_id:
            categ_dict.update({cat+"##product_categ_10":categ_id})

    main_categ_data = []
    for categ_line in reader_categ:
        # print("---------categ_line--------",categ_line)
        if main_categ_data and categ_line['Product_template_name'] in [x['Product_template_name'] for x in main_categ_data] and \
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
    # stop
    for ll in main_categ_data:
            # print("--------main_line----------",ll['main_line'])
        try:
            if ll['main_line'].get('Product_category_1'):
                server.execute(db_name, 2, db_password, 'product.category', "write",[categ_dict.get(ll['main_line']['Product_category_1']+"##product_categ_1")],
                                          {'parent_id': 1})
            if ll['main_line']['Product_category_1'] and ll['main_line']['Product_category_2']:
                server.execute(db_name, 2, db_password, 'product.category', "write",[categ_dict.get(ll['main_line']['Product_category_2']+"##product_categ_2")],
                                          {'parent_id': categ_dict.get(ll['main_line']['Product_category_1']+"##product_categ_1")})
            if ll['main_line']['Product_category_2'] and ll['main_line']['Product_category_3']:
                server.execute(db_name, 2, db_password, 'product.category', "write",[categ_dict.get(ll['main_line']['Product_category_3']+"##product_categ_3")],
                                          {'parent_id': categ_dict.get(ll['main_line']['Product_category_2']+"##product_categ_2")})
            if ll['main_line']['Product_category_3'] and ll['main_line']['Product_category_4']:
                server.execute(db_name, 2, db_password, 'product.category', "write",[categ_dict.get(ll['main_line']['Product_category_4']+"##product_categ_4")],
                                          {'parent_id': categ_dict.get(ll['main_line']['Product_category_3']+"##product_categ_3")})
            if ll['main_line']['Product_category_4'] and ll['main_line']['Product_category_5']:
                server.execute(db_name, 2, db_password, 'product.category', "write",[categ_dict.get(ll['main_line']['Product_category_5']+"##product_categ_5")],
                                          {'parent_id': categ_dict.get(ll['main_line']['Product_category_4']+"##product_categ_4")})
            if ll['main_line'].get('Product_category_5') and ll['main_line'].get('Product_category_6'):
                server.execute(db_name, 2, db_password, 'product.category', "write",[categ_dict.get(ll['main_line']['Product_category_6']+"##product_categ_6")],
                                          {'parent_id': categ_dict.get(ll['main_line']['Product_category_5']+"##product_categ_5")})
            if ll['main_line'].get('Product_category_6') and ll['main_line'].get('Product_category_7'):
                server.execute(db_name, 2, db_password, 'product.category', "write",[categ_dict.get(ll['main_line']['Product_category_7']+"##product_categ_7")],
                                          {'parent_id': categ_dict.get(ll['main_line']['Product_category_6']+"##product_categ_6")})
            if ll['main_line'].get('Product_category_7') and ll['main_line'].get('Product_category_8'):
                server.execute(db_name, 2, db_password, 'product.category', "write",[categ_dict.get(ll['main_line']['Product_category_8']+"##product_categ_8")],
                                          {'parent_id': categ_dict.get(ll['main_line']['Product_category_7']+"##product_categ_7")})
            if ll['main_line'].get('Product_category_8') and ll['main_line'].get('Product_category_9'):
                server.execute(db_name, 2, db_password, 'product.category', "write",[categ_dict.get(ll['main_line']['Product_category_9']+"##product_categ_9")],
                                          {'parent_id': categ_dict.get(ll['main_line']['Product_category_8']+"##product_categ_8")})
            if ll['main_line'].get('Product_category_9') and ll['main_line'].get('Product_category_10'):
                server.execute(db_name, 2, db_password, 'product.category', "write",[categ_dict.get(ll['main_line']['Product_category_10']+"##product_categ_10")],
                                          {'parent_id': categ_dict.get(ll['main_line']['Product_category_9']+"##product_categ_9")})
        except:
            missing_product_categ.append(ll['main_line']['Barcode'])
    all_categ_id = server.execute(db_name, 2, db_password, 'product.category', "search_read",[('name','ilike','##product_categ_')],["name"])
    print("-------all_categ_id-----------",len(all_categ_id))
    if all_categ_id:
        for all_categ in all_categ_id:
            origin_name = (all_categ['name']).split("##")[0]
            # print("---------all_categ------------",all_categ,origin_name)
            server.execute(db_name, 2, db_password, 'product.category', "write",
                           [all_categ['id']], {"name": origin_name})

print("-----------missing_product_categ-----------", missing_product_categ)
