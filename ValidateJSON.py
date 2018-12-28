#il faudra passser en argument un fichier JSON
import sys	
import json
def json_validator(data):
    try:
        json.loads(data)
        return True
    except ValueError as error:
        print("invalid json: %s" % error)
        return False
if __name__ == '__main__':
	print (json_validator(sys.argv[1]))
