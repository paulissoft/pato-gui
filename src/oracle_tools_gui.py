"""
The Oracle Tools GUI for launching Maven builds based on Oracle Tools.
"""

# Python modules
import os
import argparse
import subprocess
from gooey import Gooey, GooeyParser
from shutil import which

# local module(s)
from utils import about
from utils.pom import logger, db_order, initialize, process_POM


DEFAULT_SIZE = (1200, 800)
MENU = [{'name': 'Help',
         'items': [{'type': 'Link',
                    'menuTitle': 'Documentation',
                    'url': about.__help_url__},
                   {'type': 'AboutDialog',
                    'menuTitle': 'About',
                    'name': 'Oracle Tools',
                    'description': 'Run the various Oracle Tools commands',
                    'version': about.__version__,
                    'copyright': about.__copyright__,
                    'website': about.__url__,
                    'author(s)': about.__author__,
                    'license': about.__license__}]}]
TERMINAL_FONT_FAMILY = 'Courier New'

EXTRA_MAVEN_COMMAND_LINE_OPTIONS = '--extra-maven-command-line-options'
ACTION = '--action'
DB = '--db'
DB_PROXY_PASSWORD = '--db-proxy-password'
DB_PASSWORD = '--db-password'
FILE = '--file'


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
            'validator': {
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
            'validator': {
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
    db_proxy_password_help = 'The password for database proxy account'
    db_password_help = 'The password for database account'
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
    except Exception:
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


def main():
    argv = initialize()
    if len(argv) <= 2:
        if len(argv) == 0:
            argv.append(get_POM_file(argv))
        run_POM_file_gui(argv[-1])
    else:
        run_POM_file(argv)


if __name__ == '__main__':
    main()
