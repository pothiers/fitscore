import csv
import scipy.optimize
import numpy
import os.path

def tt():
    fn = os.path.expanduser('~/Downloads/swim-dtp.csv')
    popt = get_params(fn,swim_func)
    print('val={}'.format(calc_value(swim_func, 0.45, 20.1, popt)))
    return popt
    
def bike_func((d,t), c1,c2):
    return c1*d*d/t - c2

# for P1 (60d < 7t); r < 7mph
def run_func((d,t), c1, c2):
    return c1*d*d/t - c2


# In [165]: fitcurve.tt()
# D,T shape: (2, 184)
# perr=[ 26.60668929   2.47317076]
# val=24.1086288358
# Out[165]: array([ 404.52241871,  -20.03321641])
def swim_func((d,t), c1, c2):
    return c1*d*d/t - c2


# should use mask
def get_data(fname):
    # Dist-min (miles), T-min(minutes)
    dt_list = list()
    p_list = list()
    with open(fname) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['P'] == '': continue
            d0, d1,t0,t1,p = [float(row[k]) for k in ['D0','D1','T0','T1','P']]
            if d0 == 0: continue
            #! if p == 0: continue
            if t0 == 0:
                #! t0 = 60*d0/30 # for last row in block for BIKE
                t0 = 60*d0/12 # for last row in block for RUN
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


def get_params(fname, myfunc):
    dt_ar,p_ar = get_data(fname)
    print('D,T shape: {}'.format(dt_ar.shape))
    popt,pcov = scipy.optimize.curve_fit(myfunc, dt_ar, p_ar)
    perr = numpy.sqrt(numpy.diag(pcov))
    print('perr={}'.format(perr))
    return popt
    
def calc_value(myfunc,d,t,popt):
    return myfunc([d,t], *popt)
