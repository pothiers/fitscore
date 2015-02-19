#! /usr/bin/env python3
#
# SCAFFOLDING.  Not needed for regular use.
#
import os, sys, string, argparse, logging



import csv
import scipy.optimize
import numpy
import os.path
import itertools

import fitscore as fs

def tt_swim():
    fn = os.path.expanduser('~/sandbox/fitscore/data/swim-dtp.csv')
    popt = get_params(fn,swim_func, 2.378)
    print('val={}'.format(calc_value(swim_func, 1, 30, popt)))
    return popt

def tt_bike():
    fn = os.path.expanduser('~/sandbox/fitscore/data/bike-dtp.csv')
    popt = get_params(fn,bike_func, 25)
    print('val={}'.format(calc_value(bike_func, 22, 88, popt)))
    return popt

def tt_run():
    fn = os.path.expanduser('~/sandbox/fitscore/data/run-dtp.csv')
    popt = get_params(fn,run_func, 12)
    print('val={}'.format(calc_value(run_func, 9.3, 100, popt)))
    return popt
    
# In [165]: fitcurve.tt()
# D,T shape: (2, 184)
# perr=[ 26.60668929   2.47317076]
# val=24.1086288358
# Out[165]: array([ 404.52241871,  -20.03321641])
def swim_func(dt, c1, c2):
    (d,t) = dt
    return c1*d*d/t - c2

# In [177]: fitcurve.tt_bike()
# D,T shape: (2, 172)
# perr=[ 0.10698979  1.40342227]
# val=74.4832646726
# Out[177]: array([ 15.40226164,  10.22917434])
def bike_func(dt, c1,c2):
    (d,t) = dt
    return c1*d*d/t - c2

# for P1 (60d < 7t); r < 7mph
# In [173]: fitcurve.tt()
# D,T shape: (2, 417)
# perr=[ 0.7629971   0.49012066]
# val=109.505029064
# Out[173]: array([ 136.24096526,    8.32978179])
def run_func(dt, c1, c2):
    (d,t) = dt
    return c1*d*d/t - c2
 

# should use mask
def get_data(fname,maxRate):
    '''maxRate :: max reasonable rate (mph) for activity'''
    # Dist-min (miles), T-min(minutes)
    dt_list = list()
    p_list = list()
    with open(fname) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['P'] == '': continue
            d0, d1,t0,t1,p = [float(row[k]) for k in ['D0','D1','T0','T1','P']]
            if d0 == 0: continue
            if t0 < 0.1:
                 t0 = 60*d0/maxRate
            dt_list.append([d0,t0])
            p_list.append(p*100/30)
    return numpy.array(dt_list).T, numpy.array(p_list)

        
def apply_func(fname, func):
    dt_list = list()
    p_list = list()
    with open(fname) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            d0, d1,t0,t1,p = [float(row[k]) for k in ['D0','D1','T0','T1','P']]
            if p == 0: continue
            if t0 == 0: continue
            p2 = func(d0, t0) * 30/100
            print('D={:4.0f}, T={:4.0f}, Score error: {:.0%}'
                  .format(d0, t0, abs(p-p2)/p))


def get_params(fname, myfunc, maxRate):
    dt_ar,p_ar = get_data(fname, maxRate)
    print('D,T shape: {}'.format(dt_ar.shape))
    popt,pcov = scipy.optimize.curve_fit(myfunc, dt_ar, p_ar)
    perr = numpy.sqrt(numpy.diag(pcov))
    print('perr={}'.format(perr))
    return popt
    
def calc_value(myfunc,d,t,popt):
    return myfunc([d,t], *popt)


##############################################################################

def duration(minutes):
    'Return hh:mm:ss'
    seconds = int(minutes*60)
    h = seconds // (60*60)
    m = (seconds - h*60*60) // 60
    s = (seconds - h*60*60) % 60
    return('{:02d}:{:02d}:{:02d}'.format(h,m,s))

def run_grade(outfile):
    big = 1e9
    # distance (=miles x 10)
    for d10 in itertools.chain(range(10,50),
                               range(50,100,5),
                               range(100,270,10)):
        d = d10/10.0
        # slowest speeds: 0, 2, 3, 4, 5, 6, 7.5, 9, 10.5 
        # slowest speeds: 0,    3, 4, 5, 6, 7.5, 9, 10.5 (>= 2 miles)
        # max time (=seconds)
        if d < 2:        
            v_list = [2, 3, 4, 5, 6, 7.5, 9, 10.5, big]  #mph
        else:
            v_list = [3, 4, 5, 6, 7.5, 9, 10.5, big]     
        min_t = [60*d/v for v in v_list]
        max_t = [big] + [t for t in min_t[:-1]]
        print()
        for (min,max) in zip(min_t, max_t):
            print('{}\t{}\t{}'.format(d, duration(min), duration(max)))
    
def bike_grade(outfile):
    big = 1e9
    for d in itertools.chain(range(2,30), range(30,105,5)):
        v_list = [10,15,20, big]
        min_t = [60*d/v for v in v_list]
        max_t = [big] + [t for t in min_t[:-1]]
        print()
        for (min,max) in zip(min_t, max_t):
            print('{}\t{}\t{}'.format(d, duration(min), duration(max)))

def swim_grade(outfile):
    big = 1e9
    # distance (=yards)
    for d in itertools.chain(range(200,1900,50), range(1900,3001,100)):
        v_list = [1800, 2400, 3600, big] # yards/hour
        min_t = [60*d/v for v in v_list]
        max_t = [big] + [t for t in min_t[:-1]]
        print()
        for (min,max) in zip(min_t, max_t):
            print('{}\t{}\t{}'.format(d, duration(min), duration(max)))


def main():
    #!print('EXECUTING: {}\n\n'.format(' '.join(sys.argv)))
    parser = argparse.ArgumentParser(
        description='Grade fitness scores against expected',
        epilog='EXAMPLE: %(prog)s -a run scores.csv"'
        )
    #!parser.add_argument('infile',  help='Input file',
    #!                    type=argparse.FileType('r') )
    parser.add_argument('--csvfile', help='Output scores in CSV',
                        type=argparse.FileType('w') )
    parser.add_argument('-a', '--activity', help='Type of activity',
                        choices=['run','swim','bike'],
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


    if args.activity == 'run':
        run_grade(args.csvfile)
    elif args.activity == 'swim':
        swim_grade(args.csvfile)
    elif args.activity == 'bike':
        bike_grade(args.csvfile)

if __name__ == '__main__':
    main()
