"""
The PATO GUI for launching Maven builds based on PATO.
"""

# Python modules
import os
import sys
import argparse
import subprocess
import shlex
import re
from gooey import Gooey, GooeyParser
from shutil import which

# local module(s)
from pato_gui import about
from pato_gui.pom import db_order, initialize, process_POM

# f"" syntax
if sys.version_info < (3, 6):
    sys.exit("Please use Python 3.6+")


logger = None
parse_state = ''
parse_info_expr = re.compile(r'\[INFO\]( (.+))?')
parse_flyway_info_expr = re.compile(r'\[INFO\] (--- flyway:(\d+\.)*\d+:info .+ ---)')
parse_summary_expr = re.compile(r'\[INFO\] ((Reactor Summary|BUILD SUCCESS).*)')

DEFAULT_SIZE1 = (1200, 600)
DEFAULT_SIZE2 = (1500, 750)
MENU = [{'name': 'Help',
         'items': [{'type': 'Link',
                    'menuTitle': 'Documentation',
                    'url': about.__help_url__},
                   {'type': 'AboutDialog',
                    'menuTitle': 'About',
                    'name': 'Paulissoft Application Tools for Oracle (PATO)',
                    'description': 'Run the various PATO commands',
                    'version': about.__version__,
                    'copyright': about.__copyright__,
                    'website': about.__url__,
                    'author(s)': about.__author__,
                    'license': about.__license__}]}]
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
       show_success_modal=False,
       show_failure_modal=True,
       show_restart_button=True,
       disable_progress_bar_animation=True,
       clear_before_run=True,
       default_size=DEFAULT_SIZE1,
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
       default_size=DEFAULT_SIZE2,
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


def process_output_line(line):
    """
Should be able to parse output like this:

[INFO] --- flyway:10.12.0:info (default-cli) @ ORACLE_TOOLS ---
[INFO] 6 SQL migrations were detected but not run because they did not follow the filename convention.
[INFO] Set 'validateMigrationNaming' to true to fail fast and see a list of the invalid file names.
[INFO] Database: jdbc:oracle:thin:@bc_dev (Oracle 19.27)
[INFO] Schema version: 20210607094700
[INFO]
[INFO] +------------+----------------+------------------------------------------------------------+----------+---------------------+------------+----------+
...
+------------+----------------+------------------------------------------------------------+----------+---------------------+------------+----------+

[INFO]

or:

[INFO] --- flyway:10.12.0:info (default-cli) @ BC_UI ---
[INFO] 4 SQL migrations were detected but not run because they did not follow the filename convention.
[INFO] Set 'validateMigrationNaming' to true to fail fast and see a list of the invalid file names.
[INFO] Database: jdbc:oracle:thin:@bc_dev (Oracle 19.27)
[INFO] Schema version: 0
[INFO]
[INFO] +------------+---------+-----------------------------------------------------+----------+---------------------+------------+----------+
...
+------------+---------+-----------------------------------------------------+----------+---------------------+------------+----------+

[INFO] ------------------------------------------------------------------------

and return:

--- flyway:10.12.0:info (default-cli) @ BC_UI ---
4 SQL migrations were detected but not run because they did not follow the filename convention.
Set 'validateMigrationNaming' to true to fail fast and see a list of the invalid file names.
Database: jdbc:oracle:thin:@bc_dev (Oracle 19.27)
Schema version: 0

+------------+---------+-----------------------------------------------------+----------+---------------------+------------+----------+
...
+------------+---------+-----------------------------------------------------+----------+---------------------+------------+----------+

"""
    global parse_state, parse_info_expr, parse_flyway_info_expr, parse_summary_expr

    debug = False

    if debug:
        print("parse_state = %r, line = %r" % (parse_state, line))

    output = None

    if parse_state == 'summary':
        output = line
    elif parse_state == 'flyway_info':
        if not line:
            parse_state = ''
        else:
            m = parse_info_expr.match(line)
            if m:
                output = m.group(2)
                if output is not None and output == 'Skipping Flyway execution':
                    parse_state = 'flyway_info_skip'
            else:
                output = line
    else:
        m = parse_flyway_info_expr.match(line)
        if m:
            output = line  # show whole line
            parse_state = 'flyway_info'
        else:
            m = parse_summary_expr.match(line)
            if m:
                output = line  # show whole line
                parse_state = 'summary'

    if debug:
        print("parse_state = %r, output = %r" % (parse_state, output))
    elif output:
        print(output, flush=True)

    return


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

    mvn_args = '-B'
    cmd = '{0} {1} {2} -P{3} {4} -Ddb.config.dir={5} -Ddb={6}'.format('mvnd' if args.mvnd else 'mvn', FILE, args.file, args.action, mvn_args, args.db_config_dir, args.db)
    if len(extra_maven_command_line_options) > 0:
        cmd += ' ' + ' '.join(extra_maven_command_line_options)
    sql_home = os.path.dirname(os.path.dirname(which('sql')))
    logger.debug('sql_home: {}'.format(sql_home))
    cmd += f' -Dsql.home="{sql_home}"'
#    if args.action == 'db-info':
#        cmd +='| grep '
    logger.info('Maven command to execute: %s' % (cmd))
    # now add the password
    if args.db_proxy_password:
        os.environ['DB_PASSWORD'] = args.db_proxy_password
    elif args.db_password:
        os.environ['DB_PASSWORD'] = args.db_password

    # Run the command as a subprocess so we can process flyway:info output and let other flyway output unchanged

    if args.action != 'db-info':
        subprocess.run(shlex.split(cmd), check=True, shell=False)
    else:
        exit_code = None
        with subprocess.Popen(shlex.split(cmd),
                              shell=False,
                              # We pipe the output to an internal pipe
                              stdout=subprocess.PIPE,
                              # Make sure that if this Python program is killed, this gets killed too
                              preexec_fn=os.setsid) as process:
            # Poll for output, note: readline() blocks efficiently until there is output with a newline
            while True:
                output = process.stdout.readline()
                # If the output is not empty, feed it to the function, strip the newline first
                if output:
                    process_output_line(output.strip().decode("utf-8"))
                else:
                    # Polling returns None when the program is still running, exit_code otherwise
                    exit_code = process.poll()
                    if exit_code is not None:
                        break

        # Program ended, get exit/return code
        if exit_code is not None and exit_code != 0:
            raise RuntimeError("Command '{}' finished with exit code {}".format(cmd, exit_code))

    os.environ['DB_PASSWORD'] = ''
    logger.debug('return')


def main():
    global logger

    argv, logger, args = initialize()
    if len(argv) <= 4:
        if not args.file:
            args = get_POM_file(argv)
        run_POM_file_gui(args.file, args.db_config_dir, args.mvnd)
    else:
        run_POM_file(argv)
