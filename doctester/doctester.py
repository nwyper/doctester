#!/usr/bin/python

import os
import subprocess
import sys
import time


def parse_args():
    """ parse the command line options """
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--root',
            help="path to project root",
            default='.'
            )
    parser.add_argument('--logfile',
            help="file to record results into",
            default='doctest.log'
            )
    parser.add_argument('--verbose', '-v',
            help="show output as tests are running",
            action='store_true'
            )

    args = parser.parse_args()
    main(root=args.root, logfile=args.logfile, verbose=args.verbose)


def main(root='.', logfile='doctest.log', verbose=False):
    start_path = os.getcwd()

    with open(logfile, 'w') as outfile:
        os.chdir(root)

        for f in find_python_files():
            # print status message, using a path relative to the calling 
            # directory
            path = os.path.relpath(os.path.join(root, f), start_path)
            sys.stdout.write("Testing {}".format(path))

            verbose and sys.stdout.write('\n')
            sys.stdout.flush()

            # run the test
            r = test_file(f, verbose=verbose)

            # write the filename to the log file
            outfile.write(60 * '=' + '\n\n')
            outfile.write(r['filename'] + '\n')
            outfile.write(60 * '-' + '\n\n')

            if r['passed']:
                # print status to stdout
                verbose and sys.stdout.write("{} passed".format(f))
                sys.stdout.write('\n')
            else:
                # add a banner to the log file highlighting the failed test
                outfile.write(60 * '*' + '\n')
                outfile.write("   FAILED   ".center(60, '*') + '\n')
                outfile.write(60 * '*' + '\n\n')
                
                # print status to stdout
                verbose and sys.stdout.write("{}".format(path))
                sys.stdout.write("  ** FAILED **\n")

            # write the test's output to the log file
            outfile.write(r['output'] + 4 * '\n')
            outfile.flush()


def find_python_files():
    for root, dirs, files in os.walk('.'):
        for f in files:
            if '/_tests' in root:
                continue

            if f.endswith('.py'):
                yield os.path.join(root, f)
    raise StopIteration


def test_file(filename, verbose=False):
    command = 'python -m doctest -v "{}"'.format(filename)

    retval = {'filename':filename}

    proc = subprocess.Popen(command, shell=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE)

    stdout = []
    while True:
        # readline blocks waiting for input
        new = proc.stdout.readline()

        if verbose:
            sys.stdout.write(new)
            sys.stdout.flush()

        stdout.append(new)

        # at the end of the process, poll() returns the returncode
        if proc.poll() is not None:
            break

    stdout.append('\n')

    # reconstruct the output, and save it
    retval['output'] = ''.join(stdout)

    proc.poll()
    if proc.returncode == 0:
        retval['passed'] = True
    else:
        retval['passed'] = False

    return retval


if __name__ == '__main__':
    try:
        parse_args()
    except KeyboardInterrupt:
        sys.exit(0)
