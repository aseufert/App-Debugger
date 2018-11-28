#! /usr/bin/env python3

import sys
import re
import os
import subprocess

'''
Use for coloring output. For example:
print(bcolors.HEADER, "Example string", bcolors.ENDC)
'''
class bcolors:
    HEADER = '\033[95m'
    OKCYAN = '\033[36m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BACKCYAN = '\033[46m'


# MAIN COMMAND STARTS HERE
# Conditional to determine if script was run in pseudo-terminal
if os.isatty(sys.stdin.fileno()):

    # Looks for argument. If there isn't one, it prompts the user for one.
    argu_param = sys.argv[1].lower() if len(sys.argv) > 1 else ''

    if argu_param == 'version':
        print('Version 1.0')
        sys.exit()

    elif argu_param != 'android' and argu_param != 'ios':
        try:
            argu_param = ''
            while argu_param != 'android' and argu_param != 'ios':
                print('Are you testing Android or iOS?')
                argu_param = str(input()).lower()
        except (KeyboardInterrupt, EOFError):
            print('\nClosing the debugger...')
            sys.exit()

    else:
        pass


    # Prompt user for filter options
    print('Enter search criteria below (Case sensitive):')

    try:
        regex_input = str(input())
        search_regex = re.compile(regex_input, re.VERBOSE)

    except (KeyboardInterrupt, EOFError):
        print('\nClosing the debugger...')
        sys.exit()

    # Run idevicesyslog or adb logcat depending on user input
    if argu_param == 'ios':
        linux_cmd = subprocess.Popen(['idevicesyslog'], stdout=subprocess.PIPE, bufsize=0, universal_newlines=True, errors='replace')

    elif argu_param == 'android':
        try:
            subprocess.run(['adb', 'logcat', '-c'])

        except (KeyboardInterrupt, EOFError):
            print('\nClosing the Debugger...')
            sys.exit()

        linux_cmd = subprocess.Popen(['adb', 'logcat'], stdout=subprocess.PIPE, bufsize=0, universal_newlines=True, errors='replace')

    cmd_input = linux_cmd.stdout

else:
    search_regex = re.compile('')
    cmd_input = sys.stdin


# Read from the command as cmd_input
try:
    with cmd_input as p:
        print('Running...')

        while True:
            try:

                # For loop reads stdout piped from linux_cmd above
                for line in iter(p.readline, ''):
                    regex_filter = search_regex.search(line)

                    if regex_filter:
                        ''' 
                        Simply print line here or pass data to a function
                        for further logic
                        '''

                        print(line, end='')

                else:
                    break

            except KeyboardInterrupt:
                print('\nClosing the Debugger...')
                sys.exit()
            except Exception as e:
                print(e)
                continue

except (KeyboardInterrupt, EOFError):
    print('\nClosing the Debugger...')
    sys.exit()

except:
    print('Unexpected Error. Please rerun the program.')
