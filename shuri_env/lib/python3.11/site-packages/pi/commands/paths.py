import sys

import logging
logger = logging.getLogger(__name__)


def cli(parser):
    # opts = parser.parse_args()
    for path in sys.path:
        print path
