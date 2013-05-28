#!/usr/bin/python

import os
import sys
import doctest


class stats(object):
    file_count = 0
    failed_files = 0


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

            stats.file_count += 1

            if r['passed']:
                # print status to stdout
                verbose and sys.stdout.write("{} passed".format(f))
                sys.stdout.write('\n')
            else:
                stats.failed_files += 1
                
                # print status to stdout
                verbose and sys.stdout.write("{}".format(path))
                sys.stdout.write("  ** FAILED **\n")

                # write the test's output to the log file
                outfile.write(r['output'] + 4 * '\n')
                outfile.flush()


def find_python_files():
    for root, dirs, files in os.walk('.'):
        for f in files:
            if f.endswith('.py'):
                yield os.path.join(root, f)
    raise StopIteration


class StdOut(object):
    """ simple helper to capture all 'print' output in a string """
    def __init__(self):
        self.data = []

    def write(self, d):
        self.data.append(d)

    def flush(self):
        pass

    def get_data(self):
        return ''.join(self.data)


def test_file(filename, verbose=False):
    dirname, f = os.path.split(filename)

    # import the module to test
    sys.path.insert(0, dirname)
    m = __import__(f[:-3])
    del sys.path[0]

    # test the module, using doctest.testmod()
    try:
        # temporarily change stdout
        sys.stdout = StdOut()

        # test this module
        failures, tests = doctest.testmod(m)

    finally:
        # record the test output
        output = sys.stdout.get_data()

        # restore stdout
        sys.stdout = sys.__stdout__

    return {
            'passed': not failures,
            'output': output,
            'filename': filename
            }

if __name__ == '__main__':
    try:
        parse_args()
    except KeyboardInterrupt:
        sys.stdout.write('\n')
    finally:
        sys.stdout.write('\n{} files processed; {} failed\n'.format(
            stats.file_count, stats.failed_files)
            )
