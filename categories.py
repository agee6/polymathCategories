import sys
import sqlite3
import requests
import os
import xml.etree.ElementTree as ET
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

def makeDatabase():
    lead = "{urn:ebay:apis:eBLBaseComponents}"
    r = requests.post(url, data=xml, headers=header)
    root = ET.fromstring(r.text)
    category_array = root.find(lead + "CategoryArray")
    if(os.path.isfile(database)):
        os.remove(database)
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('CREATE TABLE {tn} (CategoryID INT, CategoryName TEXT, CategoryLevel INT, BestOfferEnabled INT, CategoryParentID INT )'\
    .format(tn="main"))
    c.execute('CREATE INDEX CategoryIndex ON {tn} ({cn})'\
    .format(tn="main", cn="CategoryID"))
    for child in category_array:
        ID = int(child.find(lead + "CategoryID").text)
        Name = child.find(lead + "CategoryName").text
        Level = int(child.find(lead + "CategoryLevel").text)
        if(child.find(lead + "BestOfferEnabled")):
            BOEnabledB = child.find(lead + "BestOfferEnabled").text
        else:
            BOEnabledB = False
        ParentID = int(child.find(lead + "CategoryParentID").text)
        if(BOEnabledB == 'true'):
            BOEnabled = 1
        else:
            BOEnabled = 0
        vals = (ID, Name, Level, BOEnabled, ParentID)
        c.execute("INSERT INTO main(CategoryID, CategoryName, CategoryLevel, BestOfferEnabled, CategoryParentID) VALUES(?, ?, ?, ?, ?)", vals)
    conn.commit()
    conn.close()
    print("database built successfully")

def renderCategory(num):
    html_header = f"""
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="utf-8">
        <title>category:{num}</title>
        <link rel="stylesheet" href="style.css">
      </head>
      <body>
        <h1 class='title'>Category Tree for number: {num}</h1>
        <div class='container'>
      """
    conn = sqlite3.connect(database)
    c = conn.cursor()
    num_list = (num)
    c.execute("SELECT * FROM main WHERE CategoryID={the_id}"\
    .format(the_id=num))
    category_item_array = c.fetchall()
    conn.close()
    if(len(category_item_array) == 0):
        print("No category with ID:" + str(num))
        return
    main_body = buildBody(category_item_array)
    tail = """
    </div>
    </body>
    </html>
    """
    final_html = html_header + main_body + tail
    filename = str(num) + ".html"
    html_file = open(filename, "w")
    html_file.write(final_html)
    html_file.close()
    print("successfully rendered html file. You may now open " + filename + " in your browser" );

def buildBody(arr):
    if(len(arr) == 0):
        return ""
    html_string = "<ul>"
    for ele in arr:
        if(ele[3] == 1):
            BestOfferEnabled = "true"
        else:
            BestOfferEnabled = "false"
        list_item = f"""
        <li><div class=list-item>
            <h2>Category Name: {ele[1]}</h2>
            <h4>Category ID: {ele[0]}</h4>
            <h4>Category Level: {ele[2]}</h4>
            <h4>Best Offer Enabled: {BestOfferEnabled}</h4>
        """
        conn = sqlite3.connect(database)
        c = conn.cursor()
        c.execute("SELECT * FROM main WHERE CategoryLevel={next_level} AND CategoryParentID={the_id}"\
        .format(the_id=ele[0],next_level=ele[2] + 1))
        category_item_array = c.fetchall()
        conn.close()
        html_string += list_item + buildBody(category_item_array) + "</div></li>"
    html_string += "</ul>"
    return html_string

if(sys.argv[1]):
    if(sys.argv[1] == "--rebuild"):
        makeDatabase()
    elif(sys.argv[1] == "--render"):
        if(os.path.isfile(database)):
            if(sys.argv[2]):
                renderCategory(sys.argv[2])
            else:
                print("error: no categoryID entered")
        else:
            print("error: no database. Run '--rebuild' to continue")
    else:
        print("error: invalid argument")
else:
    print("error: no valid argument")
