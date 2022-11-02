import xmlrpc.client as xmlrpclib
not_found = []

db_name = "yaelrdrz-principadoerp-main-5969988"
# db_name = "db_principado15"
db_password = "admin"
server = xmlrpclib.ServerProxy('https://principado.odoo.com/xmlrpc/object',allow_none=True)
# server = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object',allow_none=True)
product_tmpl_id = server.execute(db_name, 2, db_password, 'product.template', "search",[])
print("-----product_tmpl_id---search----", len(product_tmpl_id))
if product_tmpl_id:
    count = 1
    for tmpl in product_tmpl_id:
        try:
            server.execute(db_name, 2, db_password, 'product.template', "update_attribute_values", [tmpl])
        except:
            not_found.append(tmpl)
        count += 1
        if count in [10000,20000,30000,40000,50000,60000,70000,80000,90000,100000,110000,120000,130000]:
            print("-------count---------",count)
print("-----------not_found-----------",not_found)