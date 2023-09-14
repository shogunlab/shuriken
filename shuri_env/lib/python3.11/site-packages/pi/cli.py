import logging
import pkgutil

import pi
import pi.commands


commands = {}
for imp_importer, name, ispkg in pkgutil.iter_modules(pi.commands.__path__):
    fullname = pi.commands.__name__ + '.' + name
    # if fullname not in sys.modules:
    imp_loader = imp_importer.find_module(fullname)
    module = imp_loader.load_module(fullname)
    commands[name] = module


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Python package manipulation',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('command', choices=commands, help='Command to run')
    parser.add_argument('-V', '--version', action='version', version=pi.__version__)
    parser.add_argument('-v', '--verbose', action='store_true', help='Print extra information')
    opts, _ = parser.parse_known_args()

    loglevel = logging.DEBUG if opts.verbose else logging.INFO
    # logging.basicConfig(format='%(levelname)s: %(message)s', level=loglevel)
    logging.basicConfig(level=loglevel)

    commands[opts.command].cli(parser)

if __name__ == '__main__':
    main()
