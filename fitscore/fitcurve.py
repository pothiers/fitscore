import csv
import os.path
import scipy.optimize
import numpy

def get_lists():
    # Dist (miles), T-min(minutes
    with open(os.path.expanduser('~/Downloads/run-dtp.csv')) as csvfile:
        reader = csv.reader(csvfile)
        tab = [(float(d), float(t0), float(p))
               for (d,t0,p) in list(reader)
               if (p !='') and (float(p) > 0) ]
    return numpy.array(tab).T  

        
def new_get_lists():
    # Dist (miles), T-min(minutes
    with open(os.path.expanduser('~/Downloads/run-dttp.csv')) as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        tab = [(float(d), float(t0), float(t1), float(p))
               for (d,t0,t1,p) in list(reader)
               if (p !='') and (float(p) > 0) ]
    return numpy.array(tab).T  

        
    
def func2(d_t, n, c):
    d = d_t[0]
    t = d_t[1]
    return n*d*d/(t*c)

def func1(d_t, n, c):
    d = d_t[0]
    t = d_t[1]
    return c+ n*d*d/t

def func(d_t, n, c, m):
    d = d_t[0]
    t = d_t[1]
    return c+ n*d*d/t + m*d


def get_params(myfunc):
    print('dbg2')
    dtp_ar = get_lists()
    print(dtp_ar.shape)
    dt_ar = dtp_ar[0:2]
    p_ar = dtp_ar[2]
    popt,pcov = scipy.optimize.curve_fit(myfunc, dt_ar, p_ar)
    perr = numpy.sqrt(numpy.diag(pcov))
    print('perr={}'.format(perr))
    return popt
    
def get_pts(myfunc,d,t,popt):
    return myfunc([d,t], *popt)
