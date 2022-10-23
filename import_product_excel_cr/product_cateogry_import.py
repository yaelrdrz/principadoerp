import xmlrpc.client as xmlrpclib
import csv
import logging
_logger = logging.getLogger(__name__)

# filelist = ['/home/hardik/workspace/cr/principadoerp/import_product_excel_cr/principado_product/test.csv']
filelist = ['/home/odoo/src/user/import_product_excel_cr/principado_product/final_catalogue_141022_latest.csv']
not_found = []
missing_unspsc_categ = []
missing_product_categ = []
for filepath in filelist:
    print("-------------filepath-------",filepath)
    file_unspsc = open(filepath)
    file = open(filepath)
    reader = csv.DictReader(file,delimiter=",")
    db_name = "yaelrdrz-principadoerp-main-5969988"
    # db_name = "db_principado15"
    db_password = "admin"
    server = xmlrpclib.ServerProxy('https://principado.odoo.com/xmlrpc/object',allow_none=True)
    # server = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object',allow_none=True)
    file_unspsc = open(filepath)
    reader_unspsc = csv.DictReader(file_unspsc, delimiter=",")
    final_dict = []
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
        # print("-------line--------",line)
        if final_dict and line['Product_template_name'] in [x['tmpl_name'] for x in final_dict]:continue
        else:
            final_dict.append({'tmpl_name': line['Product_template_name'],'Product_category_1': line['Product_category_1'],
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
    #Categ 1
    product_categ_1_dict = {}
    for categ_1 in product_categ_1:
        categ_id_1 = server.execute(db_name, 2, db_password, 'product.category', "search", [('name', '=', categ_1)])
        if not categ_id_1:
            categ_id_1 = [server.execute(db_name, 2, db_password, 'product.category', "create", {'parent_id': 1,'name': categ_1,'property_cost_method': 'average',
                    'property_valuation': 'real_time'})]
        product_categ_1_dict.update({categ_1: categ_id_1[0]})
    #categ 2
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

    # print("-------product_categ_1_dict--------",product_categ_1_dict)
    # print("-------product_categ_2_dict--------",product_categ_2_dict)
    # print("-------product_categ_3_dict--------",product_categ_3_dict)
    # print("-------product_categ_4_dict--------",product_categ_4_dict)
    # print("-------product_categ_5_dict--------",product_categ_5_dict)
    # print("-------product_categ_6_dict--------",product_categ_6_dict)
    # print("-------product_categ_7_dict--------",product_categ_7_dict)
    # print("-------product_categ_8_dict--------",product_categ_8_dict)
    # print("-------product_categ_9_dict--------",product_categ_9_dict)
    # print("-------product_categ_10_dict--------",product_categ_10_dict)
    print("---------final---------", len(final_dict))
    for k in final_dict:
            # print("----------k----------------",k)
        try:
            product_tmpl_id = server.execute(db_name, 2, db_password, 'product.template', "search",[('name', '=', k['tmpl_name'])])
            prod_category_id = False
            csv_categ_count = ''
            if product_tmpl_id:
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
                # print("----------prod_category_id---------",prod_category_id)
                # print("----------csv_categ_count---------",csv_categ_count)
                for i in range(10,0,-1):
                    i_match = int(csv_categ_count.split("_")[-1])
                    if i_match == i:
                        for j in range(i_match,0,-1):
                            # print("--------j------",j)
                            # print("--------k------",k["Product_category_"+str(j)])
                            categ_dict_variable = "product_categ_%s_dict"%str(j)
                            update_categ_id = eval(categ_dict_variable).get(k["Product_category_"+str(j)])
                            if j != 1:
                                parent_categ_dict_variable = "product_categ_%s_dict"%str(j-1)
                                parent_categ_id = eval(parent_categ_dict_variable).get(k["Product_category_"+str(j-1)])
                            else:
                                parent_categ_dict_variable = "product_categ_%s_dict" % str(j)
                                parent_categ_id = eval(parent_categ_dict_variable).get(k["Product_category_" + str(j)])
                            # print("--------categ_dict_variable-------", categ_dict_variable)
                            # print("--------eval------",update_categ_id,parent_categ_id,type(parent_categ_id))
                            try:
                                if j == 1:
                                    test = server.execute(db_name, 2, db_password, 'product.category', "write",[update_categ_id],{'parent_id': 1})
                                else:
                                    test = server.execute(db_name, 2, db_password, 'product.category', "write",[update_categ_id],{'parent_id': parent_categ_id})
                            except:
                                missing_product_categ.append(k['tmpl_name'])
                # stop
                if prod_category_id:
                    server.execute(db_name, 2, db_password, 'product.template', "write",
                                                        product_tmpl_id,{"categ_id": prod_category_id})
        except:
            not_found.append(k['tmpl_name'])
print("-----------not_found-----------",not_found)
print("-----------missing_unspsc_categ-----------",missing_unspsc_categ)
print("-----------missing_product_categ-----------",missing_product_categ)