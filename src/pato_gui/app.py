"""
The PATO GUI for launching Maven builds based on PATO.
"""

# Python modules
import os
import sys

try:
    from importlib import metadata as importlib_metadata
except ImportError:
    # Backwards compatibility - importlib.metadata was added in Python 3.8
    import importlib_metadata
    
import argparse
import subprocess
from gooey import Gooey, GooeyParser
from shutil import which

# f"" syntax: Python 3.6
if sys.version_info < (3, 6):
    sys.exit("Please use Python 3.6+")

#     
for app_module in [sys.modules['__main__'].__package__ , 'pato_gui']:
    # Retrieve the app's metadata
    try:
        metadata = importlib_metadata.metadata(app_module)
        if 'Formal-Name' in metadata:
            break
    except importlib_metadata.PackageNotFoundError as err:
        pass
    

__title__ = metadata['Formal-Name'] if metadata['Formal-Name'] else "PatoGui"
# __package_name__ = 'pato-gui'
__author__ = metadata['Author']
__description__ = metadata['Summary']
__email__ = metadata['Author-email']
__version__ = '3.2.0'
__version_info__ = tuple(__version__.split("."))
__license__ = 'MIT License'
__copyright__ = 'Copyright (c) 2021-2023 Gert-Jan Paulissen'
__url__ = metadata['Home-page']
__help_url__ = "https://paulissoft.github.io/pato-gui"

def create_dict(*args):
    d = dict()
    for i in args:
        d[i] = eval(i)
    return d

about = create_dict('__title__', '__author__', '__email__', '__version_info__', '__version__', '__license__', '__copyright__', '__url__', '__help_url__')

logger = None

__all__ = ['about', 'db_order', 'initialize', 'check_environment', 'process_POM', 'main']


DEFAULT_SIZE = (1200, 800)
MENU = [{'name': 'Help',
         'items': [{'type': 'Link',
                    'menuTitle': 'Documentation',
                    'url': __help_url__},
                   {'type': 'AboutDialog',
                    'menuTitle': 'About',
                    'name': 'Paulissoft Application Tools for Oracle (PATO)',
                    'description': 'Run the various PATO commands',
                    'version': __version__,
                    'copyright': __copyright__,
                    'website': __url__,
                    'author(s)': __author__,
                    'license': __license__}]}]
TERMINAL_FONT_FAMILY = 'Courier New'

MVND = '--mvnd'
EXTRA_MAVEN_COMMAND_LINE_OPTIONS = '--extra-maven-command-line-options'
ACTION = '--action'
DB = '--db'
DB_PROXY_PASSWORD = '--db-proxy-password'
DB_PASSWORD = '--db-password'
FILE = '--file'
DB_CONFIG_DIR = '--db-config-dir'


def find_executable(executables):
    for executable in executables:
        if which(executable) is not None:
            return executable
    assert False, "None of the executables ({}) can be found on the PATH.".format(", ".join(executables))


PYTHONW = find_executable(['pythonw3', 'pythonw', 'python3', 'python'])
PYTHON = find_executable(['python3', 'python'])


@Gooey(program='Get POM file',
       target=f"{PYTHONW} -u {__file__}",
       show_success_modal=False,
       show_failure_modal=True,
       show_restart_button=True,
       disable_progress_bar_animation=True,
       clear_before_run=True,
       default_size=DEFAULT_SIZE,
       menu=MENU,
       terminal_font_family=TERMINAL_FONT_FAMILY)
def get_POM_file(argv):
    logger.debug('get_POM_file(%s)' % (argv))
    parser = GooeyParser(description='Get a Maven POM file to work with')
    parser.add_argument(
        'file',
        help='The POM file',
        nargs='?',
        widget="FileChooser",
        gooey_options={
            'validator': {
                'test': "user_input[-7:] == 'pom.xml'",
                'message': 'This is not a POM file'
            }
        })
    parser.add_argument(
        DB_CONFIG_DIR,
        required=False,
        help='The database configuration directory',
        widget="DirChooser")
    args = parser.parse_args(argv)
    logger.debug('args: %s' % (args))
    logger.debug('return')
    return args


@Gooey(program='Run POM file',
       show_success_modal=True,
       show_failure_modal=True,
       show_restart_button=True,
       disable_progress_bar_animation=False,
       clear_before_run=True,
       required_cols=3,
       default_size=DEFAULT_SIZE,
       menu=MENU,
       terminal_font_family=TERMINAL_FONT_FAMILY)
def run_POM_file_gui(pom_file, db_config_dir, mvnd):
    logger.debug('run_POM_file_gui({}, {}, {})'.format(pom_file, db_config_dir, mvnd))

    db_config_dir, dbs, profiles, db_proxy_username, db_username = process_POM(pom_file, db_config_dir)
    db_proxy_password_help = f'The password for database proxy account {db_proxy_username}'
    db_password_help = f'The password for database account {db_username}'
    dbs_sorted = sorted(dbs, key=db_order)

    parser = GooeyParser(description='Get the Maven POM settings to work with and run the Maven POM file')

    group0 = parser.add_argument_group('Database Information', 'Choose the database connection')
    group0.add_argument(DB, required=True, choices=dbs_sorted, default=dbs_sorted[0], help='The database to log on to')
    if db_proxy_username:
        group0.add_argument(DB_PROXY_PASSWORD, required=True, widget="PasswordField", help=db_proxy_password_help)
    else:
        group0.add_argument(DB_PASSWORD, required=True, widget="PasswordField", help=db_password_help)

    group1 = parser.add_argument_group('Other Information', 'Choose action to perform and (optionally) extra Maven command line options')
    group1.add_argument(ACTION, required=True, choices=profiles, default=profiles[0], help='The action to perform')
    group1.add_argument(EXTRA_MAVEN_COMMAND_LINE_OPTIONS, required=False, help='Extra Maven command line options')
    if mvnd:
        group1.add_argument(MVND, required=False, widget='CheckBox', default=True, help='Use the Maven daemon for a (possibly) better performance')  # , metavar='Maven daemon'

    group2 = parser.add_argument_group('Information to be supplied to Maven', 'DO NOT CHANGE!')
    group2.add_argument(
        FILE,
        required=True,
        default=pom_file,
        gooey_options={
            'validator': {
                'test': "hash(user_input) == {}".format(hash(pom_file)),
                'message': 'Did you change the POM file?'
            }
        },
        help='The POM file (DO NOT CHANGE!)'
    )
    group2.add_argument(
        DB_CONFIG_DIR,
        required=False,
        default=db_config_dir,
        gooey_options={
            'validator': {
                'test': "hash(user_input) == {}".format(hash(db_config_dir)),
                'message': 'Did you change the database configuration directory?'
            }
        },
        help='The database configuration directory (DO NOT CHANGE!)'
    )

    args = parser.parse_args(list(pom_file))
    logger.debug('args: %s' % (args))
    logger.debug('return')


def run_POM_file(argv):
    logger.debug('run_POM_file(%s)' % (argv))
    parser = argparse.ArgumentParser(description='Get the POM settings to work with and run the POM file')
    db_proxy_password_help = 'The password for database proxy account'
    db_password_help = 'The password for database account'
    # 4 positional arguments
    parser.add_argument(ACTION, help='The action to perform')
    parser.add_argument(DB, help='The database to log on to')
    parser.add_argument(DB_PROXY_PASSWORD, default='', required=False, help=db_proxy_password_help)
    parser.add_argument(DB_PASSWORD, default='', required=False, help=db_password_help)
    parser.add_argument(FILE, help='The POM file')
    parser.add_argument(DB_CONFIG_DIR, help='The database configuration directory')
    parser.add_argument(MVND, action='store_true', help='Use the Maven daemon')
    args, extra_maven_command_line_options = parser.parse_known_args(argv)
    logger.debug('args: %s; extra_maven_command_line_options: %s' % (args, extra_maven_command_line_options))
    try:
        extra_maven_command_line_options.remove(EXTRA_MAVEN_COMMAND_LINE_OPTIONS)
    except Exception:
        pass
    cmd = '{0} {1} {2} -B -P{3} -Ddb.config.dir={4} -Ddb={5}'.format('mvnd' if args.mvnd else 'mvn', FILE, args.file, args.action, args.db_config_dir, args.db)
    if len(extra_maven_command_line_options) > 0:
        cmd += ' ' + ' '.join(extra_maven_command_line_options)
    sql_home = os.path.dirname(os.path.dirname(which('sql')))
    logger.debug('sql_home: {}'.format(sql_home))
    cmd += f' -Dsql.home="{sql_home}"'
    logger.info('Maven command to execute: %s' % (cmd))
    # now add the password
    if args.db_proxy_password:
        os.environ['DB_PASSWORD'] = args.db_proxy_password
    elif args.db_password:
        os.environ['DB_PASSWORD'] = args.db_password
    subprocess.run(cmd, check=True, shell=True)
    os.environ['DB_PASSWORD'] = ''
    logger.debug('return')


# Python modules
import sys
import os
import argparse
import subprocess
import re
from pathlib import Path
import logging
from shutil import which
# from pkg_resources import packaging
import pkg_resources


# items to test
__all__ = ['db_order', 'initialize', 'check_environment', 'process_POM']


logger = None


DB_ORDER = {'dev': 1, 'tst': 2, 'test': 2, 'acc': 3, 'prod': 4, 'prd': 4}


def db_order(db):
    for key in DB_ORDER.keys():
        if db.lower().endswith(key):
            return DB_ORDER[key]
    return 256 + ord(db.lower()[0])


def initialize():
    global logger

    argv = [argc for argc in sys.argv[1:] if argc != '--']

    parser = argparse.ArgumentParser(description='Setup logging')
    parser.add_argument('-d', dest='debug', action='store_true', help='Enable debugging')
    parser.add_argument('--db-config-dir', help='The database configuration directory')
    parser.add_argument('file', nargs='?', help='The POM file')
    args, rest = parser.parse_known_args(argv)
    if args.db_config_dir:
        args.db_config_dir = os.path.abspath(args.db_config_dir)
    if args.file:
        args.file = os.path.abspath(args.file)
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG if args.debug else logging.INFO)
    logger = logging.getLogger()
    if len(rest) == 0 and args.file:
        args.mvnd = 'mvnd' in check_environment()
    else:
        args.mvnd = False
    if '-d' in argv:
        argv.remove('-d')
    logger.debug('argv: %s; logger: %s; args: %s' % (argv, logger, args))
    return argv, logger, args


def check_environment():
    programs = [
        ['mvn', '-version', '3.3.1', r'Apache Maven ([0-9.]+)', True, True],
        ['perl', '--version', '5.16.0', r'\(v([0-9.]+)\)', True, True],
        ['sql', '-V', '18.0.0.0', r'SQLcl: Release ([0-9.]+)', True, True],
        ['java', '-version', '1.8.0', r'(?:java|openjdk) version "([0-9.]+).*"', False, True],  # version is printed to stderr (!#$?)
        ['javac', '-version', '1.8.0', r'javac ([0-9.]+)', True, True],
        ['mvnd', '--version', '0.8.0', r'mvnd ([0-9.]+)', True, False],  # Maven daemon may be there or not
    ]
    programs_found = []

    for i, p in enumerate(programs):
        # p[0]: program
        # p[1]: command line option to get the version
        # p[2]: minimum version
        # p[3]: regular expression to parse for version
        # p[4]: print stdout (True) or stderr (False)?
        # p[5]: program mandatory?
        proc = subprocess.run(p[0] + ' ' + p[1], shell=True, capture_output=True, text=True)
        assert not (p[5]) or proc.returncode == 0, proc.stderr

        if proc.returncode == 0:
            logger.debug('proc: {}'.format(proc))
            expected_version = p[2]
            regex = p[3]
            output = proc.stdout if p[4] else proc.stderr
            m = re.search(regex, output)
            assert m, 'Could not find {} in {}'.format(regex, output)
            actual_version = m.group(1)
            assert pkg_resources.packaging.version.parse(actual_version) >= pkg_resources.packaging.version.parse(expected_version), f'Version of program "{p[0]}" is "{actual_version}" which is less than the expected version "{expected_version}"'
            logger.info('Version of "{}" is "{}" and its location is "{}"'.format(p[0], actual_version, os.path.dirname(which(p[0]))))
            programs_found.append(p[0])
        else:
            logger.info('Command "{0}" failed: {1}'.format(p[0] + ' ' + p[1], proc.stderr))

    return programs_found


def process_POM(pom_file, db_config_dir):
    """
    Process a single POM file and setup the GUI.
    The POM file must be either based on an PATO parent POM for the database or Apex.
    """
    def determine_POM_settings(pom_file, db_config_dir):
        properties = {}
        profiles = set()

        cmd = f"mvn --file {pom_file} -B -N help:all-profiles -Pconf-inquiry compile"
        if db_config_dir:
            cmd += f" -Ddb.config.dir={db_config_dir}"
        mvn = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
        stdout, stderr = mvn.communicate()

        if mvn.returncode == 0:
            pass
        else:
            returncode = mvn.returncode
            error = ''
            for ch in stderr:
                error += ch
            raise Exception(f'The command "{cmd}" failed with return code {returncode} and error:\n{error}')

        # Profile Id: db-install (Active: false , Source: pom)
        line = ''
        for ch in stdout:
            if ch != "\n":
                line += ch
            else:
                logger.debug("line: %s" % (line))
                m = re.search(r"Profile Id: ([a-zA-Z0-9_.-]+) \(Active: .*, Source: pom\)", line)
                if m:
                    logger.debug("adding profile: %s" % (m.group(1)))
                    profiles.add(m.group(1))
                else:
                    # GJP 2023-09-06 https://github.com/paulissoft/pato-gui/issues/8
                    # Change re.match() into re.search() so we can match not only from the beginning but also in the middle.
                    m = re.search(r'\[echoproperties\] ([a-zA-Z0-9_.-]+)=(.+)$', line)
                    if m:
                        logger.debug("adding property %s = %s" % (m.group(1), m.group(2)))
                        properties[m.group(1)] = m.group(2)
                line = ''
        return properties, profiles

    logger.debug('process_POM()')
    properties, profiles = determine_POM_settings(pom_file, db_config_dir)
    apex_profiles = ['apex-seed-publish', 'apex-export', 'apex-import']
    db_profiles = ['db-info', 'db-install', 'db-code-check', 'db-test', 'db-generate-ddl-full']  # , 'db-generate-ddl-incr']
    if profiles.issuperset(set(apex_profiles)):
        profiles = apex_profiles
    elif profiles.issuperset(set(db_profiles)):
        profiles = db_profiles
    else:
        raise Exception('Profiles (%s) must be a super set of either the Apex (%s) or database (%s) profiles' % (profiles, set(apex_profiles), set(db_profiles)))
    if not db_config_dir:
        # C\:\\dev\\bc\\oracle-tools\\conf\\src => C:\dev\bc\oracle-tools\conf\src =>
        db_config_dir = properties.get('db.config.dir', '').replace('\\:', ':').replace('\\\\', '\\')
    assert db_config_dir, 'The property db.config.dir must have been set in order to choose a database (on of its subdirectories)'
    logger.debug('db_config_dir: ' + db_config_dir)

    p = Path(db_config_dir)
    dbs = []
    try:
        dbs = [d.name for d in filter(Path.is_dir, p.iterdir())]
    except Exception:
        pass
    assert len(dbs) > 0, 'The directory %s must have subdirectories, where each one contains information for one database (and Apex) instance' % (properties['db.config.dir'])

    db_proxy_username = properties.get('db.proxy.username', '')
    db_username = properties.get('db.username', '')
    assert db_proxy_username or db_username, f'The database acount (Maven property db.proxy.username {db_proxy_username} or db.username {db_username}) must be set'

    logger.debug('return: (%s, %s, %s, %s, %s)' % (db_config_dir, dbs, profiles, db_proxy_username, db_username))
    return db_config_dir, dbs, profiles, db_proxy_username, db_username


def main():
    global logger

    argv, logger, args = initialize()
    if len(argv) <= 4:
        if not args.file:
            args = get_POM_file(argv)
        run_POM_file_gui(args.file, args.db_config_dir, args.mvnd)
    else:
        run_POM_file(argv)


if __name__ == '__main__':
    # Last argument version (from Makefile)?
    # Please note that there is always at least one: the program
    if sys.argv[-1] == 'version':
        print(__version__)
    else:
        main()
