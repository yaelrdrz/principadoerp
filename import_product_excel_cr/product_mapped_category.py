import xmlrpc.client as xmlrpclib
import csv
import logging

_logger = logging.getLogger(__name__)

# filelist = ['/home/odoo/src/user/import_product_excel_cr/principado_product/final_catalogue_141022_latest.csv']
# filelist = ['/home/hardik/workspace/cr/principadoerp/import_product_excel_cr/principado_product/final_catalogue_141022_latest.csv']
filelist = ['/home/hardik/workspace/cr/principadoerp/import_product_excel_cr/principado_product/test1.csv']
not_found = []
missing_product_categ = []
for filepath in filelist:
    file = open(filepath)
    reader = csv.DictReader(file, delimiter=",")
    # reader_categ = csv.DictReader(file1, delimiter=",")
    # db_name = "yaelrdrz-principadoerp-main-5969988"
    db_name = "db_principado15"
    # db_password = "AdM1nPr1nc."
    db_password = "admin"
    # server = xmlrpclib.ServerProxy('https://principado.odoo.com/xmlrpc/object', allow_none=True)
    server = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object',allow_none=True)
    main_categ_data = []
    for categ_line in reader:
        # print("---------categ_line--------",categ_line)
        if main_categ_data and categ_line['Product_template_name'] in [x['Product_template_name'] for x in
                                                                       main_categ_data] and \
                categ_line['Attribute_1_size'] in [x['Attribute_1_size'] for x in main_categ_data] and \
                categ_line['Attribute_2_color'] in [x['Attribute_2_color'] for x in main_categ_data]:
            continue
        else:
            main_categ_data.append({
                "Product_template_name": categ_line['Product_template_name'],
                "Variant_internal_reference": categ_line["Variant_internal_reference"],
                "Attribute_1_size": categ_line["Attribute_1_size"],
                "Attribute_2_color": categ_line["Attribute_2_color"],
                "Barcode": categ_line["Barcode"],
                "Product_category_1": categ_line["Product_category_1"],
                "Product_category_2": categ_line["Product_category_2"],
                "Product_category_3": categ_line["Product_category_3"],
                "Product_category_4": categ_line["Product_category_4"],
                "Product_category_5": categ_line["Product_category_5"],
                "Product_category_6": categ_line["Product_category_6"],
                "Product_category_7": categ_line["Product_category_7"],
                "Product_category_8": categ_line["Product_category_8"],
                "Product_category_9": categ_line["Product_category_9"],
                "Product_category_10": categ_line["Product_category_10"],
            })
    print("-------main_categ_data------------", len(main_categ_data))
    for line in main_categ_data:
        print("----------line--------------",line)
        final_name = line['Product_template_name'] + '(Tamaño:' + line['Attribute_1_size'] + ',Color:' + line[
            'Attribute_2_color'] + ')'
        print("-------final_name-------------",final_name)
        product_tmpl_id = server.execute(db_name, 2, db_password, 'product.template', "product_search_sql_xmlrpc",
                                         [], final_name)
        print("-----product_tmpl_id---search----", product_tmpl_id)
        if product_tmpl_id:
            # categ_name = "All / "
            # if line.get("Product_category_1"):
            #     categ_name = categ_name + line['Product_category_1']
            # if line.get("Product_category_2"):
            #     categ_name = categ_name + " / " + line['Product_category_2']
            # if line.get("Product_category_3"):
            #     categ_name = categ_name + " / " + line['Product_category_3']
            # if line.get("Product_category_4"):
            #     categ_name = categ_name + " / " + line['Product_category_4']
            # if line.get("Product_category_5"):
            #     categ_name = categ_name + " / " + line['Product_category_5']
            # if line.get("Product_category_6"):
            #     categ_name = categ_name  + " / " + line['Product_category_6']
            # if line.get("Product_category_7"):
            #     categ_name = categ_name  + " / " + line['Product_category_7']
            # if line.get("Product_category_8"):
            #     categ_name = categ_name  + " / " + line['Product_category_8']
            # if line.get("Product_category_9"):
            #     categ_name = categ_name  + " / " + line['Product_category_9']
            # if line.get("Product_category_10"):
            #     categ_name = categ_name + " / " + line['Product_category_10']
            categ_name = ''
            if line.get("Product_category_10"):
                categ_name = line['Product_category_10']+"##product_categ_10"
            elif line.get("Product_category_9"):
                categ_name = line['Product_category_9']+"##product_categ_9"
            elif line.get("Product_category_8"):
                categ_name = line['Product_category_8']+"##product_categ_8"
            elif line.get("Product_category_7"):
                categ_name = line['Product_category_7']+"##product_categ_7"
            elif line.get("Product_category_6"):
                categ_name = line['Product_category_6']+"##product_categ_6"
            elif line.get("Product_category_5"):
                categ_name = line['Product_category_5']+"##product_categ_5"
            elif line.get("Product_category_4"):
                categ_name = line['Product_category_4']+"##product_categ_4"
            elif line.get("Product_category_3"):
                categ_name = line['Product_category_3']+"##product_categ_3"
            elif line.get("Product_category_2"):
                categ_name = line['Product_category_2']+"##product_categ_2"
            elif line.get("Product_category_1"):
                categ_name = line['Product_category_1']+"##product_categ_1"
            print("---------categ_name----------------",categ_name)
            if categ_name:
                categ_id = server.execute(db_name, 2, db_password, 'product.category', "search",
                                          [('name', '=', categ_name)])
                print("----------categ_id-----------",categ_id)
                if categ_id:
                    server.execute(db_name, 2, db_password, 'product.template', "write",product_tmpl_id,
                                   {'categ_id': categ_id[0]})
                else:
                    not_found.append(line['Barcode'])
        else:
            not_found.append(line['Barcode'])
print("--------not_found-----------",not_found)