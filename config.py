import configparser
import os
dirname = os.path.dirname(os.path.realpath(__file__))

config = configparser.ConfigParser()
config.read(f"{dirname}/config/config.ini")