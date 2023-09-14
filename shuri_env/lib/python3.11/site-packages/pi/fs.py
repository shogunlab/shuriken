import os
import shutil

import logging
logger = logging.getLogger(__name__)


def rm_rf(filepath, execute=True, verbose=False):
    if verbose:
        logger.warn('rm -rf %s', filepath)
    if execute:
        if os.path.isdir(filepath):
            shutil.rmtree(filepath)
        else:
            os.remove(filepath)
