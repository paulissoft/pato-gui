"""
The Oracle Tools GUI for launching Maven builds based on Oracle Tools.
"""

# Python modules
import sys
import os
import argparse
import subprocess
import re
from pathlib import Path
import logging
from gooey import Gooey, GooeyParser
import json
from shutil import which
from pkg_resources import packaging

# local module(s)
import about


DEFAULT_SIZE = (1200, 800)
MENU = [{
           'name': 'Help',
           'items': [{
               'type': 'Link',
               'menuTitle': 'Documentation',
               'url': about.__help_url__
           }, {
               'type': 'AboutDialog',
               'menuTitle': 'About',
               'name': 'Oracle Tools',
               'description': 'Run the various Oracle Tools commands',
               'version': about.__version__,
               'copyright': about.__copyright__,
               'website': about.__url__,
               'author(s)': about.__author__,
               'license': about.__license__
           }]
       }]
TERMINAL_FONT_FAMILY = 'Courier New'

EXTRA_MAVEN_COMMAND_LINE_OPTIONS = '--extra-maven-command-line-options'
ACTION = '--action'
DB = '--db'
DB_PROXY_PASSWORD = '--db-proxy-password'
DB_PASSWORD = '--db-password'
FILE = '--file'

logger = None


def setup_logging():
    global logger, debug

    argv = [argc for argc in sys.argv[1:] if argc != '--']

    parser = argparse.ArgumentParser(description='Setup logging')
    parser.add_argument('-d', dest='debug', action='store_true', help='Enable debugging')
    parser.add_argument('file', nargs='?', help='The POM file')
    args, rest = parser.parse_known_args(argv)
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG if args.debug else logging.INFO)
    logger = logging.getLogger()
    if len(rest) == 0 and args.file:
        check_environment()
    if '-d' in argv:
        argv.remove('-d')
    return argv


def check_environment():
    programs = [
        ['mvn', '-version',  '3.3.1', r'Apache Maven ([0-9.]+)'],
        ['perl', '--version', '5.16.0', r'\(v([0-9.]+)\)'],
        ['sql', '-V', '18.0.0.0', r'SQLcl: Release ([0-9.]+)']
    ]

    for i, p in enumerate(programs):
        proc = subprocess.run(p[0] + ' ' + p[1], shell=True, capture_output=True, text=True)
        assert proc.returncode == 0, proc.stderr
        logger.debug('proc: {}'.format(proc))
        expected_version = p[2]
        regex = p[3]
        m = re.search(regex, proc.stdout)
        assert m, 'Could not find {} in {}'.format(regex, proc.stdout)
        actual_version = m.group(1)
        assert packaging.version.parse(actual_version) >= packaging.version.parse(expected_version), f'Version of program "{p[0]}" is "{actual_version}" which is less than the expected version "{expected_version}"'
        logger.info('Version of "{}" is "{}" and its location is "{}"'.format(p[0], actual_version, os.path.dirname(which(p[0]))))


@Gooey(program='Get POM file',
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
        widget="FileChooser",
        gooey_options={
            'validator':{
                'test': "user_input[-7:] == 'pom.xml'",
                'message': 'This is not a POM file'
            }
        })
    args = parser.parse_args(argv)
    logger.debug('args: %s' % (args))
    logger.debug('return')


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
def run_POM_file_gui(pom_file):
    def db_order(db):
        for i, e in enumerate(['dev', 'tst', 'test', 'acc', 'prod', 'prd']):
            if e in db.lower():
                return i
        return 0

    logger.debug('run_POM_file_gui(%s)' % (pom_file))

    dbs, profiles, db_proxy_username, db_username = process_POM(pom_file)
    db_proxy_password_help = f'The password for database account {db_proxy_username}'
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

    group2 = parser.add_argument_group('Information to be supplied to Maven', 'DO NOT CHANGE!')    
    group2.add_argument(
        FILE,
        required=True,
        default=pom_file,
        gooey_options={
            'validator':{
                'test': "hash(user_input) == {}".format(hash(pom_file)),
                'message': 'Did you change the POM file?'
            }
        },
        help='The POM file (DO NOT CHANGE!)'
    )

    args = parser.parse_args(list(pom_file))
    logger.debug('args: %s' % (args))
    logger.debug('return')


def run_POM_file(argv):
    logger.debug('run_POM_file(%s)' % (argv))
    parser = argparse.ArgumentParser(description='Get the POM settings to work with and run the POM file')
    db_proxy_password_help = f'The password for database proxy account'
    db_password_help = f'The password for database account'
    # 4 positional arguments
    parser.add_argument(ACTION, help='The action to perform')
    parser.add_argument(DB, help='The database to log on to')
    parser.add_argument(DB_PROXY_PASSWORD, default='', required=False, help=db_proxy_password_help)
    parser.add_argument(DB_PASSWORD, default='', required=False, help=db_password_help)
    parser.add_argument(FILE, help='The POM file')
    args, extra_maven_command_line_options = parser.parse_known_args(argv)
    logger.debug('args: %s; extra_maven_command_line_options: %s' % (args, extra_maven_command_line_options))
    try:
        extra_maven_command_line_options.remove(EXTRA_MAVEN_COMMAND_LINE_OPTIONS)
    except:
        pass
    cmd = 'mvn {0} {1} -P{2} -Ddb={3}'.format(FILE, args.file, args.action, args.db)
    if len(extra_maven_command_line_options) > 0:
        cmd += ' ' + ' '.join(extra_maven_command_line_options)
    sql_home = os.path.dirname(os.path.dirname(which('sql')))
    logger.debug('sql_home: {}'.format(sql_home))
    cmd += f' -Dsql.home="{sql_home}"'
    logger.info('Maven command to execute: %s' % (cmd))
    # now add the password
    if args.db_proxy_password:
        cmd += ' -Ddb.proxy.password={}'.format(args.db_proxy_password)
    elif args.db_password:
        cmd += ' -Ddb.password={}'.format(args.db_password)
    subprocess.run(cmd, check=True, shell=True)
    logger.debug('return')


def process_POM(pom_file):
    """
    Process a single POM file and setup the GUI.
    The POM file must be either based on an Oracle Tools parent POM for the database or Apex.
    """
    def determine_POM_settings(pom_file):
        properties = {}
        profiles = set()

        cmd = f"mvn {FILE} {pom_file} -N help:all-profiles -Pconf-inquiry compile"
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
                m = re.search("Profile Id: ([a-zA-Z0-9_.-]+) \(Active: .*, Source: pom\)", line)
                if m:
                    logger.debug("adding profile: %s" % (m.group(1)))
                    profiles.add(m.group(1))
                else:
                    m = re.match('\[echoproperties\] ([a-zA-Z0-9_.-]+)=(.+)$', line)
                    if m:
                        logger.debug("adding property %s = %s" % (m.group(1), m.group(2)))
                        properties[m.group(1)] = m.group(2)
                line = ''
        return properties, profiles

    logger.debug('process_POM()')
    properties, profiles = determine_POM_settings(pom_file)
    apex_profiles = ['apex-export', 'apex-import']
    db_profiles = ['db-install', 'db-test', 'db-generate-ddl-full', 'db-generate-ddl-incr']
    if profiles.issuperset(set(apex_profiles)):
        profiles = apex_profiles
    elif profiles.issuperset(set(db_profiles)):
        profiles = db_profiles
    else:
        raise Exception('Profiles (%s) must be a super set of either the Apex (%s) or database (%s) profiles' % (profiles, set(apex_profiles), set(db_profiles)))
    # C\:\\dev\\bc\\oracle-tools\\conf\\src => C:\dev\bc\oracle-tools\conf\src =>
    db_config_dir = properties.get('db.config.dir', '').replace('\\:', ':').replace('\\\\', '\\')
    assert db_config_dir, 'The property db.config.dir must have been set in order to choose a database (on of its subdirectories)'
    logger.debug('db_config_dir: ' + db_config_dir)

    p = Path(db_config_dir)
    dbs = []
    try:
        dbs = [d.name for d in filter(Path.is_dir, p.iterdir())]
    except:
        pass
    assert len(dbs) > 0, 'The directory %s must have subdirectories, where each one contains information for one database (and Apex) instance' % (properties['db.config.dir'])

    db_proxy_username = properties.get('db.proxy.username', '')
    db_username = properties.get('db.username', '')
    assert db_proxy_username or db_username, f'The database acount (Maven property db.proxy.username {db_proxy_username} or db.username {db_username}) must be set'

    logger.debug('return: (%s, %s, %s, %s)' % (dbs, profiles, db_proxy_username, db_username))
    return dbs, profiles, db_proxy_username, db_username


if __name__ == '__main__':
    argv = setup_logging()
    if len(argv) <= 2:
        if len(argv) == 0:
            argv.append(get_POM_file(argv))
        run_POM_file_gui(argv[-1])
    else:
        run_POM_file(argv)

