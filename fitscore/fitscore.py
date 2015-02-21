#! /usr/bin/env python

import os, sys, string, argparse, logging


def swim_fs(d,t):
    # perr=[ 26.60668929   2.47317076]
    c1, c2 = [ 404.52241871,  -20.03321641]
    return max(c1*d*d/t - c2,0)

def bike_fs(d,t):
    # perr=[ 0.80264855  8.44697716]
    c1, c2 = [ 16.58767938,  -7.88430268]
    return max(c1*d*d/t - c2,0)


def run_fs(d,t):
    # perr=[ 0.60349473  0.77871181]
    c1, c2 = [ 133.74408607,    9.63067614]
    return max(c1*d*d/t - c2,0)



##############################################################################


def main():
    #!print('EXECUTING: {}\n\n'.format(' '.join(sys.argv)))
    parser = argparse.ArgumentParser(
        description='Calculate fitness score',
        epilog='EXAMPLE: %(prog)s -a run -d 3.2 -t 32"'
        )
    #!parser.add_argument('infile',  help='Input file',
    #!                    type=argparse.FileType('r') )
    #!parser.add_argument('--csvfile', help='Output scores in CSV',
    #!                    type=argparse.FileType('w') )
    parser.add_argument('-d', '--distance',
                        help='Distance  in miles',
                        type=float)
    parser.add_argument('-t', '--time',
                        help='Time in minutes',
                        type=float)
    parser.add_argument('-a', '--activity', help='Type of activity',
                        choices=['ruk','swim','bike'],
                        default='run')
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


    d = args.distance
    t = args.time
    if args.activity == 'run':
        run_fs(d, t)
    elif args.activity == 'swim':
        swim_fs(d, t)
    elif args.activity == 'bike':
        bike_fs(d, t)

if __name__ == '__main__':
    main()
