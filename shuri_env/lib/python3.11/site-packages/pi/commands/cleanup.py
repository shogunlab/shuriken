import os
import sys
import site
from pi import fs

import logging
logger = logging.getLogger(__name__)


def cleanup(sitedir, execute=True, verbose=False):
    sys_path_basenames = map(os.path.basename, sys.path)
    logger.debug('listdir %s', sitedir)
    for filename in os.listdir(sitedir):
        # TODO: read .egg-link files and test if their contents (a local filesystem path) are in sys.path
        if not filename.endswith('.pth') and filename not in sys_path_basenames:
            filepath = os.path.join(sitedir, filename)
            fs.rm_rf(filepath, execute=execute, verbose=verbose)
    # TODO: remove non-existing packages mentioned in the .pth files


def cli(parser):
    '''
    Uninstall inactive Python packages from all accessible site-packages directories.

    Inactive Python packages
    when multiple packages with the same name are installed
    '''
    parser.add_argument('-n', '--dry-run', action='store_true', help='Print cleanup actions without running')
    opts = parser.parse_args()

    for sitedir in site.getsitepackages():
        cleanup(sitedir, execute=not opts.dry_run, verbose=opts.verbose or opts.dry_run)
