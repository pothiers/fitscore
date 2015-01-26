#! /usr/bin/env python
## @package pyexample
#  Documentation for this module. (for DOXYGEN)
#
#  More details.

'''\
<<Python script callable from command line.  Put description here.>>
'''

import os, sys, string, argparse, logging


def swim_fs(d,t):
    # perr=[ 26.60668929   2.47317076]
    c1, c2 = [ 404.52241871,  -20.03321641]
    return c1*d*d/t - c2

def bike_fs(d,t):
    c1, c2 = [ 13.69764397,   3.22730112]
    return c1*d*d/t - c2

def run_fs(d,t):
    # perr=[ 0.7629971   0.49012066]
    c1, c2 = [ 136.24096526,    8.32978179]
    return c1*d*d/t - c2


## DOXYGEN documentation for a function.
#
# More details.
def run_pts(miles, minutes):
    pass


##############################################################################

def main_tt():
    cmd = 'MyProgram.py foo1 foo2'
    sys.argv = cmd.split()
    res = main()
    return res

def main():
    print('EXECUTING: {}\n\n'.format(' '.join(sys.argv)))
    parser = argparse.ArgumentParser(
        #!version='1.0.1',
        description='My shiny new python program',
        epilog='EXAMPLE: %(prog)s a b"'
        )
    parser.add_argument('infile',  help='Input file',
                        type=argparse.FileType('r') )
    parser.add_argument('outfile', help='Output output',
                        type=argparse.FileType('w') )
    parser.add_argument('-q', '--quality', help='Processing quality',
                        choices=['low','medium','high'], default='high')
    parser.add_argument('--loglevel',      help='Kind of diagnostic output',
                        choices = ['CRTICAL','ERROR','WARNING','INFO','DEBUG'],
                        default='WARNING',
                        )
    args = parser.parse_args()
    #!args.outfile.close()
    #!args.outfile = args.outfile.name

    #!print 'My args=',args
    #!print 'infile=',args.infile


    log_level = getattr(logging, args.loglevel.upper(), None)
    if not isinstance(log_level, int):
        parser.error('Invalid log level: %s' % args.loglevel) 
    logging.basicConfig(level = log_level,
                        format='%(levelname)s %(message)s',
                        datefmt='%m-%d %H:%M'
                        )
    logging.debug('Debug output is enabled!!!')


    myFunc(args.infile, args.outfile)

if __name__ == '__main__':
    main()
