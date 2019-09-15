from bamboo.BambooWrapper import BambooWrapper
import logging


class BambooBuild:
    def __init__(self, connection, searchterm, key, buildnumber):
        self.connection  = connection
        self.masterkey   = self.searchfor(key, searchterm)
        remotebuild      = self.getbuild(buildnumber)
        name             = remotebuild['plan']['shortName']
        self.name        = name.replace('Feature branch builds', 'develop')
        self.buildnumber = buildnumber or remotebuild['buildNumber']

    def searchfor(self, plankey, term):
        if not term:
            return plankey
        term = term.replace('/', '-')
        request = BambooWrapper.search(self.connection,
                                       plankey,
                                       term
                                       )
        try:
            key = request['searchResults'][0]['searchEntity']['key']
        except IndexError:
            raise Exception('No search result found on Bamboo for term: {0}'
                            .format(term))
        return key

    def getbuild(self, buildnumber=0):
        request = BambooWrapper.build(self.connection,
                                      self.masterkey
                                      )['results']
        if request['size'] == 0:
            raise Exception('Bamboo couldn\'t find a build for {0}'
                            .format(self.masterkey))
        result = request['result'][0]
        if result['state'] != 'Successful':
            logging.warning('Latest build marked as non-successful, '
                            'trying to retrieve artifacts anyhow.')
        return result

    def exists(self):
        return self.buildnumber != 0
