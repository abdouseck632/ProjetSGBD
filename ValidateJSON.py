#il faudra passser en argument un fichier JSON
import sys

import json
from jsonschema import validate

# fonction de validation du ficheir json

def fonction_demo(dict_to_test, dict_valid):
    try:
        validate(dict_to_test, dict_valid)
    except Exception as valid_err:
        print("Validation NO: {}".format(valid_err))
        raise valid_err
    else:
        # Realise votre travail
        print("JSON validé")
fichier_json = sys.argv[1]
if __name__ == '__main__':
#permet de verifier la validation avec la fonction fonction_demo    
    with open(fichier_json, "r") as fichier:
        dict_to_test = json.load(fichier)        
