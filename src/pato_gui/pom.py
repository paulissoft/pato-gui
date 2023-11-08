"""
The PATO GUI for launching Maven builds based on PATO.
"""

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
from packaging.version import parse as parse_version


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
            assert parse_version(actual_version) >= parse_version(expected_version), f'Version of program "{p[0]}" is "{actual_version}" which is less than the expected version "{expected_version}"'
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
    db_profiles = ['db-info', 'db-install', 'db-code-check', 'db-test', 'db-generate-ddl-full', 'db-generate-ddl-incr']
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
