import configargparse


def argument_parser():
    parser = configargparse.ArgParser(description='This script is for '
                                      'automating the bamboo download '
                                      'and execution process for Traktor DJ')
    parser.add_argument('platform', choices=['mac',
                                             'ios',
                                             'macios',
                                             'win',
                                             'all'],
                        help='Choose the platform for which you want '
                             'Traktor DJ to be downloaded.')
    parser.add_argument('-c', '--configfile', default='Traktor.ini',
                        help='Config file path relative to script location ')
    parser.add_argument('-b', '--build', type=int, default=0,
                        help='Specify the build of the traktor repo you want '
                        'to checkout. Default is latest')
    parser.add_argument('-s', '--search',
                        help='Specify the search term you\'re looking for.')
    parser.add_argument('-d', '--download', action='store_false',
                        help='Download artifact from bamboo')
    parser.add_argument('-x', '--extract', action='store_true',
                        help='Extract compressed artifact')
    parser.add_argument('-l', '--launch', action='store_true',
                        help='Launch application')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Show more debug output')
    return parser.parse_args()


def with_parsed_arguments(func, *args):
    def func_wrapper(*args):
        return func(argument_parser())
    return func_wrapper
