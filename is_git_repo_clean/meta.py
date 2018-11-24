from os import path
import json

pathToMetaJson = path.join(path.dirname(path.realpath(__file__)), "meta.json")

with open(pathToMetaJson, "r") as f:
    version = json.load(f)["version"]
