import os
import subprocess
import logging
import tarfile
import zipfile
from bamboo.BambooWrapper import BambooWrapper
from utils.colors import green, yellow, red


class BambooArtifact:
    def __init__(self, platform, bamboo, config):
        self.credentials  = bamboo.connection.credentials
        self.os           = platform
        self.branch       = bamboo.build.name
        self.buildnumber  = '#' + str(bamboo.build.buildnumber)
        self.path         = bamboo.path + self.os + '/'
        self.app          = self.path + config['appname']
        self.url          = BambooWrapper.artifactUrl(bamboo.connection,
                                                      bamboo.build.masterkey,
                                                      bamboo.build.buildnumber,
                                                      config['filepath'],
                                                      config['filename'],
                                                      )
        self.artifactfile = self.path + config['filename']
        self.displayname  = ' '.join([green(self.branch),
                                      yellow(self.buildnumber),
                                      red(self.os),
                                      ])

    def artifactfileexists(self):
        return os.path.exists(self.artifactfile)

    def appexists(self):
        return os.path.exists(self.app)

    def retrieve(self):
        os.makedirs(self.path, exist_ok=True)
        logging.debug(self.url)
        subprocess.run(['curl',
                        '-f',
                        '-o', self.artifactfile,
                        '-#',
                        '-u', self.credentials,
                        self.url,
                        ])

    def extract(self):
        if self.os == 'mac':
            container = tarfile.open(self.artifactfile)
        else:
            container = zipfile.ZipFile(self.artifactfile)
        container.extractall(self.path)
        container.close()

    def launch(self):
        executors = {'mac': ['open', self.app],
                     'ios': ['ios-deploy',
                             '--uninstall',
                             '--bundle', self.app,
                             ],
                     'win': [self.app],
                     }
        logging.debug(executors[self.os])
        response = subprocess.run(executors[self.os])
        return response.returncode
