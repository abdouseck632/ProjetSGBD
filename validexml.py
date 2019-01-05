from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from glob import glob
import sys

def parsefile(file):
    parser = make_parser()
    parser.setContentHandler(ContentHandler())
    parser.parse(file)

for arg in sys.argv[1:]:
    for filename in glob(arg):
        try:
            parsefile(filename)
        except Exception, e:
            print "%s n'est pas bien formé! %s" % (filename, e)
