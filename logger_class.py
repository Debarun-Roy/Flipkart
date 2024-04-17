import logging

def getLog(nm):
    # creating custom logger
    logger = logging.getLogger(nm)\
    # reading contents from properties file
    f = open("properties.txt",'r')
    if f.mode == "r":
        loglevel = f.read()
    if loglevel == "ERROR":
        logger.setLevel(logging.ERROR)
    elif loglevel == "DEBUG":
        logger.setLevel(logging.DEBUG)
    # Creating formatters
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s') 
    # Creating handlers
    fileHandler = logging.FileHandler('test.log')
    # Adding formatters to handlers
    fileHandler.setFormatter(formatter)
    # Adding handlers to loggers
    logger.addHandler(fileHandler)
    return logger