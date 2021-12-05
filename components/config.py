from json import load

def getConfig():
    with open("./config.json") as configFile:
        return load(configFile)