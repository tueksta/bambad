import logging
import requests
import getpass
import keyring


class BambooConnection:
    session = requests.Session()

    def __init__(self, config):
        self.host         = config['bamboobase']
        self.username     = config.get('username', getpass.getuser())
        self.password     = self.getpassword()
        self.session.auth = (self.username, self.password)
        self.credentials  = self.username + ':' + self.password

    def getpassword(self):
        password = keyring.get_password(self.host, self.username)
        if not password:
            password = getpass.getpass('Bamboo password: ')
            keyring.set_password(self.host, self.username, password)
        return password

    def close(self):
        self.session.close()


def with_bamboo_connection(func, *args):
    def func_wrapper(*args):
        connection = BambooConnection(config=args[0]['server'])
        result = func(connection, *args)
        connection.close()
        return result
    return func_wrapper


def with_errorcode_check(func, *args, **kwargs):
    def func_wrapper(*args, **kwargs):
        request = func(*args, **kwargs)
        if request.status_code != requests.codes.ok:
            try:
                request.raise_for_status()
            except requests.exceptions.HTTPError as error:
                logging.error('HTTP request failed, reason: ', error)
        return request
    return func_wrapper


@with_errorcode_check
def call_bamboo(connection, *args, **kwargs):
    return connection.session.get(*args, **kwargs)
