"""

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

# local module(s)
import about


logging.basicConfig(force=True, filename='oracle-tools-gui.log', encoding='utf-8', level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_SIZE = (1200, 800)
MENU = [{
           'name': 'Help',
           'items': [{
               'type': 'AboutDialog',
               'menuTitle': 'About',
               'name': 'Oracle Tools',
               'description': 'Run the various Oracle Tools commands',
               'version': about.__version__,
               'copyright': about.__copyright__,
               'website': about.__url__,
               'author(s)': about.__author__,
               'license': about.__license__
           }, {
               'type': 'Link',
               'menuTitle': 'Documentation',
               'url': about.__help_url__
           }]
       }]
TERMINAL_FONT_FAMILY = 'Courier New'


def is_POM_file(file):
    retval = os.path.isfile(file) and os.path.basename(file) == 'pom.xml'
    logger.info('is_POM_file(%s): %s' % (file, retval))
    return retval


@Gooey(default_size=DEFAULT_SIZE,
       menu=MENU,
       terminal_font_family=TERMINAL_FONT_FAMILY)
def get_POM_file(argv):
    logger.info('get_POM_file(%s)' % (argv))
    parser = GooeyParser()
    parser.add_argument('file', help='The POM file', widget="FileChooser")
    args = parser.parse_args(argv)
    logger.info('args: %s' % (args))
    if not is_POM_file(args.file):
        raise Exception('File %s is not a POM file' % (args.file))
    logger.info('return')


@Gooey(required_cols=3,
       default_size=DEFAULT_SIZE,
       menu=MENU,
       terminal_font_family=TERMINAL_FONT_FAMILY)
def get_POM_settings(argv):
    assert len(argv) == 1

    pom_file = argv[0]
    logger.info('get_POM_settings(%s)' % (argv))
    parser = GooeyParser()
    dbs, profiles = process_POM(pom_file)
    # 4 positional arguments
    parser.add_argument('profile', help='The action to perform', widget='Dropdown', choices=profiles)
    parser.add_argument('db', help='The database to log on to', widget='Dropdown', choices=dbs)
    parser.add_argument('db-password', help='The database password', widget="PasswordField")
    parser.add_argument('file', default=pom_file, help='The POM file (DO NOT CHANGE!)')
    args = parser.parse_args(argv)
    logger.info('args: %s' % (args))
    if not is_POM_file(args.file):
        raise Exception('File %s is not a POM file' % (args.file))
    logger.info('return')


def process_POM(pom_file):
    """
    Process a single POM file and setup the GUI.
    The POM file must be either based on an Oracle Tools parent POM for the database or Apex.
    """
    def determine_POM_settings(pom_file, properties):
        property_keys = [p for p in sorted(properties)]
        expressions = ['${' + p + '}' for p in reversed(property_keys)]  # since we are using pop later on
        input = expressions
        answers = {}
        profiles = set()

        input.append('0')
        mvn = subprocess.Popen("mvn --file %s -N help:all-profiles help:evaluate" % (pom_file), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
        stdout, stderr = mvn.communicate('\n'.join(input))

        # Profile Id: db-install (Active: false , Source: pom)
        next_line_contains_answer = False
        line = ''
        for ch in stdout:
            if ch != "\n":
                line += ch
            else:
                logger.debug("line: %s" % (line))
                m = re.search("Profile Id: ([a-zA-Z0-9_-]+) \(Active: .*, Source: pom\)", line)
                if m:
                    logger.info("adding profile: %s" % (m.group(1)))
                    profiles.add(m.group(1))
                elif not next_line_contains_answer:
                    m = re.search('Enter the Maven expression', line)
                    if m:
                        next_line_contains_answer = True
                elif not re.match('\[INFO\]', line):
                    if line == 'null object or invalid expression':
                        line = None
                    property = property_keys.pop()
                    logger.info("adding property %s = %s" % (property, line))
                    answers[property] = line
                    next_line_contains_answer = False
                line = ''
        return answers, profiles
    
    logger.info('process_POM()')
    properties, profiles = determine_POM_settings(pom_file, ['db.config.dir'])
    apex_profiles = {'apex-import', 'apex-export'}
    db_profiles = {'db-generate-ddl-full', 'db-install', 'db-generate-ddl-incr', 'db-test'}
    pom_parent = ''
    if profiles.issuperset(apex_profiles):
        pom_parent = 'apex'
    elif profiles.issuperset(db_profiles):
        pom_parent = 'db'
    assert pom_parent, 'Profiles (%s) must be a super set of either the Apex (%s) or database (%s) profiles' % (profiles, apex_profiles, db_profiles)
    assert properties['db.config.dir'], 'The property db.config.dir must have been set in order to choose a database (on of its subdirectories)'
    
    p = Path(properties['db.config.dir'])
    dbs = []
    try:
        dbs = [d.name for d in filter(Path.is_dir, p.iterdir())]
    except:
        pass
    assert len(dbs) > 0, 'The directory %s must have subdirectories, where each one contains information for one database (and Apex) instance' % (properties['db.config.dir'])
    profiles = db_profiles if pom_parent == 'db' else apex_profiles
    logger.info('return: (%s, %s)' % (dbs, profiles))
    return dbs, profiles


if __name__ == '__main__':
    logger.info('__main__(%s)' % (sys.argv))
    try:
        argv = [argc for argc in sys.argv[1:] if argc != '--']
        if len(argv) <= 1:
            if len(argv) == 0:
                argv.append(get_POM_file(argv))
            get_POM_settings(argv)
        else:
            pass
    except Exception as error:
        logger.exception(error)
    logger.info('exit')
    logging.shutdown()
