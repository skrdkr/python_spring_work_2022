import pickle
import json
import yaml
from yaml.loader import SafeLoader

def from_pickle(file):
    f = open(file, "rb")
    obj = pickle.load(f)
    f.close()
    return obj

def from_json(file):
    f = open(file, "r")
    obj = json.load(f)
    f.close()
    return print(obj)

def from_yaml(file):
    f = open(file, "r")
    obj = yaml.load(f, Loader=SafeLoader)
    f.close()
    return print(obj)




