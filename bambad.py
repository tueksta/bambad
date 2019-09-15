########################################################
# Bamboo Artifact Downloader
# Created by Andreas Beer
########################################################

from bamboo.ArgumentParser import with_parsed_arguments
from bamboo.BambooBuild import BambooBuild
from bamboo.BambooConnection import with_bamboo_connection
from bamboo.BambooManager import BambooManager
from bamboo.MyConfigParser import with_config_file
from utils.Timer import with_timer
from utils.colors import red, green, yellow
import logging


@with_parsed_arguments   # adds options
@with_config_file        # adds config
@with_timer              # runs timer in background
@with_bamboo_connection  # adds connection
def main(connection, config, options):
    """This method takes the branch specified by --build and --search and tries
    to identify it on bamboo as specified in the .ini file. If there is a match
    the app performs the actions --download --extract --launch as specified on
    that build on all of the specified platforms in the required platform
    argument.
    """
    loglevel = logging.DEBUG if options.verbose else logging.INFO
    logging.basicConfig(format='%(levelname)s: %(message)s', level=loglevel)
    try:
        logging.info('Checking Bamboo for plan %s, for build'
                     ' %s, and for searchterm: %s',
                     green(config['server']['bambookey']),
                     yellow('#' + str(options.build)),
                     green(options.search),
                     )
        build = BambooBuild(connection,
                            searchterm=options.search,
                            key=config['server']['bambookey'],
                            buildnumber=options.build,
                            )
    except Exception as error:
        logging.error('No build found, reason: {0}'
                      .format(red(str(error))))
        return
    logging.info(' '.join(['Build found:',
                           green(build.name),
                           yellow('#' + str(build.buildnumber))
                           ]))
    try:
        bamboomanager = BambooManager(connection,
                                      config,
                                      build=build,
                                      platforms=options.platform
                                      )
    except Exception as error:
        logging.error(red('Building project failed, reason: {0}'
                      .format(str(error))))
        return
    logging.info('Artifacts found: {0}'
                 .format(red(' '.join(bamboomanager.platforms))))
    if options.download:
        bamboomanager.download()
    if options.extract:
        bamboomanager.extract()
    if options.launch:
        bamboomanager.launch()


if __name__ == '__main__':
    main()
