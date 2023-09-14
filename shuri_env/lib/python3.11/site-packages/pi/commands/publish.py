import os
from subprocess import check_call
from pi.dist import read_script


def publish(execute=True, verbose=False, script_name='setup.py'):
    dist = read_script(script_name)
    name = dist.get_name()
    version = dist.get_version()

    if os.path.exists('README.md'):
        print 'Converting README.md to reStructuredText, because PyPI requires reStructuredText'
        if execute:
            check_call(['pandoc', 'README.md', '-o', 'README.rst'])

    # print 'Tagging current version in git'
    ## e.g., git tag -a v1.2.3 -m 1.2.3
    # subprocessor('git', 'tag', '-a', 'v' + pi.__version__, '-m', pi.__version__)
    # subprocessor('git', 'push')

    print 'Installing locally in develop mode (version=%s)' % version
    if execute:
        dist.run_command('develop')

    # python setup.py --help register
    print 'Registering on PyPI: https://pypi.python.org/pypi/%s' % name
    if execute:
        dist.run_command('register')

    # python setup.py --help sdist upload
    print 'Uploading source distribution: https://pypi.python.org/simple/%s' % name
    if execute:
        dist.run_command('sdist')
        dist.run_command('upload')


def cli(parser):
    parser.add_argument('-n', '--dry-run', action='store_true', help='Print publish sequence without running')
    opts = parser.parse_args()

    publish(execute=not opts.dry_run, verbose=opts.verbose or opts.dry_run)
