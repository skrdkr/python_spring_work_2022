import pickle
import json
import yaml

def to_pickle(obj, file, method):
    f = open(file, method)
    pickle.dump(obj, f)
    f.close()

def to_json(obj, file):
    f = open(file, "w")
    json.dump(obj, f, indent=4)
    f.close()

def to_yaml(obj, file):
    f = open(file, "w")
    yaml.dump(obj, f)
    f.close()




