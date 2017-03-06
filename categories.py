import sys
import sqlite3
import requests
import pdb
header = {
'X-EBAY-API-CALL-NAME' : 'GetCategories',
'X-EBAY-API-APP-NAME' : 'EchoBay62-5538-466c-b43b-662768d6841',
'X-EBAY-API-CERT-NAME' : '00dd08ab-2082-4e3c-9518-5f4298f296db',
'X-EBAY-API-DEV-NAME' : '16a26b1b-26cf-442d-906d-597b60c41c19',
'X-EBAY-API-SITEID' : '0',
'X-EBAY-API-COMPATIBILITY-LEVEL': '861'
}
xml = """<?xml version='1.0' encoding='utf-'?>
<GetCategoriesRequest xmlns="urn:ebay:apis:eBLBaseComponents">
    <RequesterCredentials>
      <eBayAuthToken>AgAAAA**AQAAAA**aAAAAA**PMIhVg**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6wFk4GhCpaCpQWdj6x9nY+seQ**L0MCAA**AAMAAA**IahulXaONmBwi/Pzhx0hMqjHhVAz9/qrFLIkfGH5wFH8Fjwj8+H5FN4NvzHaDPFf0qQtPMFUaOXHpJ8M7c2OFDJ7LBK2+JVlTi5gh0r+g4I0wpNYLtXnq0zgeS8N6KPl8SQiGLr05e9TgLRdxpxkFVS/VTVxejPkXVMs/LCN/Jr1BXrOUmVkT/4Euuo6slGyjaUtoqYMQnmBcRsK4xLiBBDtiow6YHReCJ0u8oxBeVZo3S2jABoDDO9DHLt7cS73vPQyIbdm2nP4w4BvtFsFVuaq6uMJAbFBP4F/v/U5JBZUPMElLrkXLMlkQFAB3aPvqZvpGw7S8SgL7d2s0GxnhVSbh4QAqQrQA0guK7OSqNoV+vl+N0mO24Aw8whOFxQXapTSRcy8wI8IZJynn6vaMpBl5cOuwPgdLMnnE+JvmFtQFrxa+k/9PRoVFm+13iGoue4bMY67Zcbcx65PXDXktoM3V+sSzSGhg5M+R6MXhxlN3xYfwq8vhBQfRlbIq+SU2FhicEmTRHrpaMCk4Gtn8CKNGpEr1GiNlVtbfjQn0LXPp7aYGgh0A/b8ayE1LUMKne02JBQgancNgMGjByCIemi8Dd1oU1NkgICFDbHapDhATTzgKpulY02BToW7kkrt3y6BoESruIGxTjzSVnSAbGk1vfYsQRwjtF6BNbr5Goi52M510DizujC+s+lSpK4P0+RF9AwtrUpVVu2PP8taB6FEpe39h8RWTM+aRDnDny/v7wA/GkkvfGhiioCN0z48</eBayAuthToken>
    </RequesterCredentials>
    <CategorySiteID>0</CategorySiteID>
    <DetailLevel>ReturnAll</DetailLevel>
</GetCategoriesRequest>"""
database = "./eb_db.sqlite"
url = "https://api.sandbox.ebay.com/ws/api.dll"
print(sys.argv)
table_name = 'my_table'
new_field = 'my_1st_column'
field_type = 'INTEGER'
table_name2 = 'my_table2'

r = requests.post(url, data=xml, headers=header)
array = r.text.split("/CategoryID")

print(array[2])



def makeDatabase():
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('CREATE TABLE {tn} ({nf} {ft})'\
        .format(tn=table_name, nf=new_field, ft=field_type))
    c.execute('CREATE TABLE {tn} ({nf} {ft} PRIMARY KEY)'\
        .format(tn=table_name2, nf=new_field, ft=field_type))
    conn.commit()
    conn.close()


if(sys.argv[1]):
    if(sys.argv[1] == "--rebuild"):
        makeDatabase()
    elif(sys.argv[1] == "--render"):
        if(sys.argv[2]):
            renderCategory(sys.argv[2])
        else:
            print("error: no categoryID entered")
    else:
        print("error: invalid argument")
else:
    print("error: no valid argument")
