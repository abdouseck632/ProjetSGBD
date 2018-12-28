import lxml
from lxml import etree

if __name__ == "__main__":
    import sys, os
    with open(sys.argv[1]) as f:
        doc = etree.parse(f)
    print ("Validating schema ... ")
    try:
        schema = etree.XMLSchema(doc)
    except lxml.etree.XMLSchemaParseError as e:
        print (e)
        exit(1)

    print ("Schema OK")
    print ("Validating document ...")
    try:
        schema.assertValid(doc)
    except lxml.etree.DocumentInvalid as e:
        print (e)
        exit(1)

    print ("Document OK")
