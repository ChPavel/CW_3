import logging
# from config import LOGGER_API_PATH, LOGGER_FORMAT

def config(app):


    api_logger = logging.getLogger("api_logger")
    api_logger.setLevel(logging.DEBUG)

    api_logger_hendler = logging.FileHandler(filename=app.config["LOGGER_API_PATH"])
    api_logger_hendler.setLevel(logging.DEBUG)
    api_logger.addHandler(api_logger_hendler)

    api_logger_format = logging.Formatter(app.config["LOGGER_FORMAT"])
    api_logger_hendler.setFormatter(api_logger_format)







