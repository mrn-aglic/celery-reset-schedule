from os import environ

ENVIRONMENT = environ.get("ENVIRONMENT", "").upper()
DEV_NAME = "DEV"

if ENVIRONMENT not in ("PROD", DEV_NAME):
    raise Exception("Please set the environment variable to either DEV or PROD")


def is_dev():
    return ENVIRONMENT == DEV_NAME