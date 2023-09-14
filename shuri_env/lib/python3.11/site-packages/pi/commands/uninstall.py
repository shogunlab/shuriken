import os
import sys
from pi import fs

import logging
logger = logging.getLogger(__name__)


def uninstall(package, execute=True, verbose=False):
    # sys_path_basenames = map(os.path.basename, sys.path)
    for filepath in sys.path:
        # filepath = /Library/Python/2.7/site-packages/chardet-2.1.1-py2.7.egg
        basename = os.path.basename(filepath)
        # basename = chardet-2.1.1-py2.7.egg
        name = basename.split('-')[0]
        # name = chardet
        if name == package:
            fs.rm_rf(filepath, execute=execute, verbose=verbose)


def cli(parser):
    parser.add_argument('-n', '--dry-run', action='store_true', help='Print uninstall actions without running')
    parser.add_argument('packages', nargs='+', help='Packages to uninstall')
    opts = parser.parse_args()

    for package in opts.packages:
        uninstall(package.lower(), execute=not opts.dry_run, verbose=opts.verbose or opts.dry_run)
