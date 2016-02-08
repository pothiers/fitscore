#! /usr/bin/env python3
#
# SCAFFOLDING.  Not needed for regular use.
# TODO: refactor so trivial to add new ACTIVITY

import os, sys, string, argparse, logging



import csv
import scipy.optimize
import numpy
import os.path
import itertools as it
import decimal
import matplotlib.pylab as plt
#import matplotlib.pylab as pl
from mpl_toolkits.mplot3d import Axes3D

import fitscore as fs



def tt_swim():
    fn = os.path.expanduser('~/sandbox/fitscore/daata/swim-dtp.csv')
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
    yCalc = run_func(x, *popt)
    return popt
    
# In [165]: fitcurve.tt()
# D,T shape: (2, 184)
# perr=[ 26.60668929   2.47317076]
# val=24.1086288358
# Out[165]: array([ 404.52241871,  -20.03321641])
def swim_func(dt, c1, c2):
    (d,t) = dt
    return c1*d*d/t - c2

# D,T shape: (2, 172)
# perr=[ 0.10574954  1.38545338]
# val=74.60815965908817
# array([ 15.42056158,  10.20492902])
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
            d0, d1,t0,t1,p = [decimal.Decimal(row[k])
                              for k in ['D0','D1','T0','T1','P']]
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
            d0, d1,t0,t1,p = [decimal.Decimal(row[k])
                              for k in ['D0','D1','T0','T1','P']]
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


def read_expected(csvfilename):
    if csvfilename ==  None:
        return dict()
    expected = dict() # dict['{d0},{d1},{t0},{t1}'] = pscore
    keys = list()
    with open(csvfilename, newline='') as csvfile:
        for row in csv.reader(csvfile, strict=True):
            if row[4] == '': continue
            if row[4] == 'P': continue
            d0, d1,t0,t1,p = [decimal.Decimal(n) for n in row]
            if d0 == 0: continue
            #!key = ('{:.1f}\t{:.1f}\t{:.1f}\t{:.1f}'.format(d0,d1,t0,t1))
            key = (round(d0,1), round(d1,1), round(t0,1), round(t1,1))
            expected[key] = p
            keys.append(key)
    return expected,keys


def print_results(ordered, results, expected):
    #!missing_expected = set(expected.keys()) - set(results.keys())
    #!missing_results = set(results.keys()) - set(expected.keys())
    #!print('Missing expected {}/{}'
    #!      .format(len(missing_expected), len(expected),))
    #!print('Missing results {}/{}'
    #!      .format(len(missing_results),  len(results),))
    #!
    #!print ('Expected keys: {}'.format(sorted(expected.keys())[0:4]))
    #!print ('Results  keys: {}'.format(sorted(results.keys())[0:4]))

    #!print('Missing: Expected(d0,d1,t0,t1)  |       Results(d0,d1,t0,t1)')
    #!if True:
    #!    missed_e = sorted(missing_expected)
    #!    missed_r = sorted(missing_results)
    #!else:
    #!    missed_e = sorted(expected)
    #!    missed_r = sorted(results)
    #!for idx in range(min(70,len(missed_e))):
    #!    data = missed_e[idx] + missed_r[idx]
    #!    print('{:5.1f} {:5.1f} {:5.1f} {:5.1f}  | {:5.1f} {:5.1f} {:5.1f} {:5.1f}'.format(*data))


    prev_d0 = None
    zExpect = list()
    zActual = list()
    x = list()
    y = list()
    print('{:>5s} {:>5s}  {:>5s} {:>5s} | {:>6s}  |  {:>6s}'
          .format('D0','D1', 'T0', 'T1', 'Expect', 'Actual'))
    for idx,key in enumerate(ordered):
        d0,d1,t0,t1 = key
        if prev_d0 != d0:
            print()
        print('{:5.1f} {:5.1f}  {:5.1f} {:5.1f} | {:6.2f}  |  {:6.2f}'
              .format(d0,
                      d1,
                      t0,
                      t1,
                      expected[key],
                      results[key]*30/100,
                  ))
        prev_d0 = d0
        x.append(float(d0))
        y.append(float(t0))
        zExpect.append(float(expected[key]))
        zActual.append(float(results[key]*30/100))
        
    fig = plt.figure()
    plt.hold(True)
   
    ax = fig.add_subplot(111,projection='3d')
    plt.xlabel('Dist')
    plt.ylabel('Time')
    #!plt.zlabel('Pts')
    #!ax.bar(x, y, zExpect, color='r', alpha=0.7)
    ax.bar(x, y, zActual, color='g', alpha=0.7)

    #!pl.plot(x, zExpect, 'r.', label='Calculated Run Curve')
    #!pl.plot(x, zActual, 'g.', label='Actual Run Curve')
    #!pl.legend()
    plt.show()


def gen_index(activity):
    index_list = list()
    if activity == 'run':
        bigV = 12.0 # fasted speed to score (mph)
        bigT = 9*60 # longest time active (minutes)
        # distance (=miles x 10)
        ll0 = [d/10.0 for d in it.chain(range(10,50),
                                        range(50,100,5),
                                        range(100,280,10))]

        for d0,d1 in it.zip_longest(ll0[:-1], it.islice(ll0,1,None)):
            d = d0
            if d < 1.1:        
                v_list = [3, 4, 5, 6, 7.5, 9, 10.5, bigV]     #slowest mph
            if 1.1 <= d < 2:        
                v_list = [2, 3, 4, 5, 6, 7.5, 9, 10.5, bigV]  #slowest mph
            else:
                v_list = [3, 4, 5, 6, 7.5, 9, 10.5, bigV]     
            min_t = [60*d/v for v in v_list]  # minutes
            max_t = [bigT] + [t for t in min_t[:-1]]
            for (t0,t1) in zip(min_t, max_t):
                index_list.append((decimal.Decimal(round(d0,1)),
                                   decimal.Decimal(round(d1,1)),
                                   decimal.Decimal(round(t0,1)),
                                   decimal.Decimal(round(t1,1))
                               ))
    elif activity == 'bike':
        bigV = 25.0 # fasted speed to score (mph)
        bigT = 11*60 # longest time active (minutes)
        ll0 = list(it.chain(range(2,30), range(30,105,5)))
        for d0,d1 in it.zip_longest(ll0[:-1], it.islice(ll0,1,None)):
            v_list = [10,15,20, bigV]
            min_t = [60*d/v for v in v_list]
            max_t = [bigT] + [t for t in min_t[:-1]]
            for (t0, t1) in zip(min_t, max_t):
                index_list.append((decimal.Decimal(round(d0,1)),
                                   decimal.Decimal(round(d1,1)),
                                   decimal.Decimal(round(t0,1)),
                                   decimal.Decimal(round(t1,1))
                               ))
    elif activity == 'swim':
        bigV = 1e9 # fasted speed to score (years/hour)
        # distance (=yards)
        for d in it.chain(range(200,1900,50), range(1900,3001,100)):
            v_list = [1800, 2400, 3600, bigV] # yards/hour
            min_t = [60*d/v for v in v_list]
            max_t = [big] + [t for t in min_t[:-1]]
            for (t0, t1) in zip(min_t, max_t):
                index_list.append((decimal.Decimal(round(d0,1)),
                                   decimal.Decimal(round(d1,1)),
                                   decimal.Decimal(round(t0,1)),
                                   decimal.Decimal(round(t1,1))
                               ))
    else:
        error('Unknown activity: {}'.format(activity))

    return index_list
    
def run_results(expected_file=None, results_file=None):
    print('\nResults for RUN')
    if expected_file == None:
        keys = gen_index('run')
    else:
        expected,keys = read_expected(expected_file)

    results = dict() # results['{d0},{d1},{t0},{t1}'] = fscore
    for key in keys:
        (d0,d1,t0,t1) = key
        fscore = fs.run_fs(float(d0), float(t0))
        results[key] = fscore
    print_results(keys, results, expected)
    return results
        
def bike_results(expected_file=None, results_file=None):
    print('\nResults for: BIKE')
    if expected_file == None:
        keys = gen_index('bike')
    else:
        expected,keys = read_expected(expected_file)

    results = dict() # results['{d0},{d1},{t0},{t1}'] = fscore
    for key in keys:
        (d0,d1,t0,t1) = key
        fscore = fs.bike_fs(float(d0), float(t0))
        results[key] = fscore
    print_results(keys, results, expected)
    return results

def swim_results(expected_file=None, results_file=None):
    print('\nResults for: SWIM')
    if expected_file == None:
        keys = gen_index('swim')
    else:
        expected,keys = read_expected(expected_file)

    results = dict() # results['{d0},{d1},{t0},{t1}'] = fscore
    for key in keys:
        (d0,d1,t0,t1) = key
        fscore = fs.swim_fs(float(d0), float(t0))
        results[key] = fscore
    print_results(keys, results, expected)
    return results

def main():
    #!print('EXECUTING: {}\n\n'.format(' '.join(sys.argv)))
    parser = argparse.ArgumentParser(
        description='Grade fitness scores against expected',
        epilog='EXAMPLE: %(prog)s -a run scores.csv"'
        )
    parser.add_argument('-e', '--expected',
                        help='Expected values (CSV format)',
                        type=argparse.FileType('r') )
    parser.add_argument('-o', '--out',
                        help='Output scores (CSV format)',
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


    if args.expected:
        args.expected.close()
        args.expected = args.expected.name

    if args.activity == 'run':
        run_results(expected_file=args.expected, results_file=args.out)
    elif args.activity == 'swim':
        swim_results(expected_file=args.expected, results_file=args.out)
    elif args.activity == 'bike':
        bike_results(expected_file=args.expected, results_file=args.out)

if __name__ == '__main__':
    main()
