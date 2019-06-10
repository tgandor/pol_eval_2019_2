import argparse
import os
import pprint
import subprocess
import sys

restart = False

try:
    import readline
except ImportError:
    pass

try:
    import morfeusz
except OSError:
    if not os.path.exists('libmorfeusz.so.0'):
        print('The Morfeusz .so is really missing.')
        exit(1)

    env = os.environ.copy()
    if 'LD_LIBRARY_PATH' in env:
        print('Path set, and import still failed...')
        exit(1)

    # just set flag, leave exception handler
    # else every exception is "during handling of OSError..."
    restart = True

if restart:
    # keyboard interrupts jump out here if raised in wrapper
    env['LD_LIBRARY_PATH'] = os.path.realpath(os.path.dirname(__file__))
    print('Restarting with LD_LIBRARY_PATH =', env['LD_LIBRARY_PATH'])
    subprocess.call([sys.executable] + sys.argv, env=env)
    exit()

parser = argparse.ArgumentParser()
parser.add_argument('--dag', action='store_true', help='use dag=True with morfeusz.analyze()')
args = parser.parse_args()

while True:
    try:
        data = input('morfeusz> ')
    except EOFError:
        print()
        break
    except KeyboardInterrupt:
        print()
        break

    if not data:
        break

    pprint.pprint(morfeusz.analyse(data, dag=args.dag))

print('bye')
