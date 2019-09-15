import logging
import os
from bamboo.BambooArtifact import BambooArtifact
from utils.colors import bold, red


class BambooManager:
    """The BambooManager manages the different actions on the
    different artifacts of a build.

    It takes a connection to pass it on to the artifacts,
             a config, to know the details of the bamboo plan,
             a build, with the results of the identification,
             platforms, specifying which artifacts to process.
    """
    platformdict = {'mac': ['mac'],
                    'ios': ['ios'],
                    'win': ['win'],
                    'macios': ['mac', 'ios'],
                    'all': ['mac', 'ios', 'win'],
                    }

    def __init__(self, connection, config, build, platforms='mac'):
        self.connection   = connection
        self.build        = build
        self.name         = config['general']['name']
        self.platforms    = self.platformdict[platforms]
        self.path         = self.initpath(config)
        self.artifacts    = self.initartifacts(config)

    def logtoconsole(self, artifact, action=''):
        project = bold(self.name)
        logging.info(' '.join([project, ':', artifact.displayname, action]))

    def initpath(self, config):
        configpath   = config.get('general', 'path', fallback='~/Downloads')
        branchfolder = self.build.name + '/'
        buildfolder  = str(self.build.buildnumber) + '/'
        relativepath = configpath + branchfolder + buildfolder
        return os.path.expanduser(relativepath)

    def initartifacts(self, config):
        artifacts = []
        for platform in self.platforms:
            try:
                artifact = BambooArtifact(platform, self, config[platform])
                artifacts.append(artifact)
            except KeyError:
                logging.warning(red('Skipping artifact - .ini file '
                                    'has no specs for platform: {}'
                                    .format(platform)))
                pass
        return artifacts

    def download(self):
        for artifact in self.artifacts:
            if artifact.artifactfileexists():
                self.logtoconsole(artifact, 'artifact was already downloaded.')
                continue
            artifact.retrieve()
            if not artifact.artifactfileexists():
                logging.error(red('Retrieval of artifact for {} failed.'
                                  .format(artifact.os)))
            else:
                self.logtoconsole(artifact, 'artifact was downloaded.')

    def extract(self):
        for artifact in self.artifacts:
            if artifact.appexists():
                self.logtoconsole(artifact, 'app was already extracted.')
                continue
            artifact.extract()
            if not artifact.appexists():
                logging.error(red('Extraction of artifact for {} failed.'
                                  .format(artifact.os)))
            else:
                self.logtoconsole(artifact, 'app was extracted.')

    def launch(self):
        for artifact in self.artifacts:
            if not artifact.appexists():
                logging.warning(red('App for {} not found'
                                    .format(artifact.os)))
                continue
            try:
                artifact.launch()
            except OSError as error:
                logging.error(red('Launching of app for {} failed, reason:'
                                  .format(artifact.os, error.strerror)))
                pass
            self.logtoconsole(artifact, 'app was launched.')
