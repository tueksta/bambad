from bamboo.BambooConnection import call_bamboo


class BambooWrapper:
    REST   = 'rest/api/latest/'
    JSON   = '.json'

    @staticmethod
    def search(connection, plankey, term):
        parameters = {'masterPlanKey': plankey,
                      'searchTerm': term,
                      'favourite': True
                      }
        url = BambooWrapper.REST + 'search/branches' + BambooWrapper.JSON
        request = call_bamboo(connection,
                              connection.host + url,
                              params=parameters)
        return request.json()

    @staticmethod
    def build(connection, plankey):
        url = BambooWrapper.REST + 'result/' + plankey + BambooWrapper.JSON
        request = call_bamboo(connection,
                              connection.host + url)
        return request.json()

    @staticmethod
    def artifactUrl(connection, plankey, buildnumber, path, name):
        url = 'browse/' + plankey
        if buildnumber:
            url += '-' + str(buildnumber)
        url += '/artifact/shared/' + path + name
        return connection.host + url
