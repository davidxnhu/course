import itertools
from fractions import Fraction

sex='BG'
day='SMTWtFs'

def product(*variables):
    return map(''.join, itertools.product(*variables))

two_kids=product(sex,day,sex,day)

def two_boys(s): return s.count('B')==2

one_boy=[s for s in two_kids if 'B' in s]


def condP(predicate,event):
    pred=[s for s in event if predicate(s)]
    return Fraction(len(pred),len(event))


boy_tuesday=[s for s in two_kids if 'BT' in s]



print condP(two_boys,boy_tuesday)
    
