import sys

import json
from jsonschema import validate

# fonction de validation du ficheir json

def fonction_demo(dict_to_test, dict_valid):
    try:
        validate(dict_to_test, dict_valid)
    except Exception as valid_err:
        print("Validation KO: {}".format(valid_err))
        raise valid_err
    else:
        # Realise votre travail
        print("JSON validé")
