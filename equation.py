import math

AGE_CONST = {'UNDER25':    10, '25AND40': 8, '40AND60': 6, 'ABOVE60': 3}
GENDER_CONST = {'MALE': 1, 'FEMALE': 1.2}
TOLERANCE = {'HIGH': 0.8, 'MEDIUM': 1, 'LOW': 1.2}
PROXIMITIES = {'CLOSETOBAR': 4, 'CLOSETOOTHER': 2, 'FAR': 1}

def TOD(x):
    if -6 < x and x < 6:
        return math.exp(-1.0*x*x/20)*1.5
    return 0.1

BPM = {'FINE': 1, 'NOTFINE': 10}

DOW = {'FRIDAY': 1.5, 'SATURDAY': 1.25, 'OTHER': 1}

print AGE_CONST['UNDER25']*GENDER_CONST['FEMALE']*TOLERANCE['MEDIUM']*PROXIMITIES['FAR']*TOD(-0.5)*BPM['FINE']*DOW['SATURDAY']