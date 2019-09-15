import configparser
from os import path


def red(string):    return '\033[91m{}\033[00m'.format(string)  # noqa


def config_parser(file):
    config = configparser.ConfigParser()
    file = path.join(path.dirname(__file__), '../config', file)
    try:
        config.read(file)
    except Exception as error:
        return 'Config file {0} not found.'.format(red(str(error)))
    return config


def with_config_file(func, *args):
    def func_wrapper(*args):
        result = func(config_parser(args[0].configfile), *args)
        return result
    return func_wrapper
