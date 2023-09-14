from subprocess import check_call

import logging
logger = logging.getLogger(__name__)


def install(package, execute=True):
    args = ['easy_install', package]
    logger.debug(' '.join(args))
    if execute:
        check_call(args)


def cli(parser):
    '''
    Currently a cop-out -- just calls easy_install
    '''
    parser.add_argument('-n', '--dry-run', action='store_true', help='Print uninstall actions without running')
    parser.add_argument('packages', nargs='+', help='Packages to install')
    opts = parser.parse_args()

    for package in opts.packages:
        install(package, execute=not opts.dry_run)
