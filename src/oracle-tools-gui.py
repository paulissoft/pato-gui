"""

"""

import sys
import os
import argparse
import subprocess
import re
from pathlib import Path
import logging
from gooey import Gooey, GooeyParser

import about


def run_POM(argv):
    logging.info('run_POM()')
    parser = argparse.ArgumentParser()
    parser.add_argument('--profile', dest='profile', required=True, help='The action to perform')
    parser.add_argument('--db', dest='db', required=True, help='The database to log on to')
    parser.add_argument('--db-password', dest='db_password', required=True, help='The database password')
    parser.add_argument('file', help='The POM file')
    logging.info('argv: %s' % (argv))
    args = parser.parse_args(argv)
    logging.info('return: %s' % (args))
    cmd = 'mvn --file %s -P%s -Ddb=%s -Ddb.password=%s' % (args.file, args.profile, args.db, args.db_password)
    subprocess.call(cmd, shell=True)


@Gooey(default_size=(1200, 800),
       menu=[{
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
       }],
       terminal_font_family='Courier New')
def run_POM_gui(argv, pom_file, dbs, profiles):
    logging.info('run_POM_gui(%s, %s, %s, %s)' % (argv, pom_file, dbs, profiles))
    parser = GooeyParser()
    parser.add_argument('--profile', dest='profile', required=True, help='The action to perform', choices=sorted(profiles))
    parser.add_argument('--db', dest='db', required=True, help='The database to log on to', choices=sorted(dbs))
    parser.add_argument('--db-password', dest='db_password', required=True, help='The database password', widget="PasswordField")
    parser.add_argument('file', default=pom_file, help='The POM file (DO NOT CHANGE!)')
    logging.info('argv: %s' % (argv))
    args = parser.parse_args(argv)
    logging.info('return: %s' % (args))


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
                logging.debug("line: %s" % (line))
                m = re.search("Profile Id: ([a-zA-Z0-9_-]+) \(Active: .*, Source: pom\)", line)
                if m:
                    logging.info("adding profile: %s" % (m.group(1)))
                    profiles.add(m.group(1))
                elif not next_line_contains_answer:
                    m = re.search('Enter the Maven expression', line)
                    if m:
                        next_line_contains_answer = True
                elif not re.match('\[INFO\]', line):
                    if line == 'null object or invalid expression':
                        line = None
                    property = property_keys.pop()
                    logging.info("adding property %s = %s" % (property, line))
                    answers[property] = line
                    next_line_contains_answer = False
                line = ''
        return answers, profiles
    
    logging.info('process_POM()')
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
    logging.info('return: (%s, %s)' % (dbs, profiles))
    return dbs, profiles


def determine_POM(argv):

    def pom(file):
        ''' 
        Test that the file is a pom.xml file.
        '''
        if os.path.basename(file) == 'pom.xml' and os.path.isfile(file):
            pass
        else:
            raise argparse.ArgumentError('File "%s" should exist and its base name must be "pom.xml"' % file)
        return file

    logging.info('determine_POM()')
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='The POM file', type=pom)
    logging.info('argv: %s' % (argv))
    args = parser.parse_args(argv)
    logging.info('args: %s' % (args))
    pom_file = args.file
    logging.info('return: %s' % (pom_file))
    return pom_file


if __name__ == '__main__':
    logging.basicConfig(encoding='utf-8', level=logging.WARNING)
    logging.info('sys.argv: %s' % (sys.argv))
    # first argument is Python script: skip it
    # strip also -- arguments
    argv = [argc for argc in sys.argv[1:] if argc != '--']
    if len(argv) <= 1:
        pom_file = determine_POM(argv)
        dbs, profiles = process_POM(pom_file)
        run_POM_gui(argv, pom_file, dbs, profiles)
    else:
        run_POM(argv)
