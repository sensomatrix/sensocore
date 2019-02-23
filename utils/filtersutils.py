from scipy import signal
from math import log

def estimate_order(pbdelta, sbdelta, normalized_bw):
    num = (-10*(log((pbdelta*sbdelta), 10))) - 13
    den = normalized_bw*14.6
    return abs(num/den)

def design_FIR_ls(numtaps, bands, desired, fs):
    return signal.firls(numtaps, bands, desired, fs=fs)

def design_FIR_parks(numtaps, bands, desired, fs):
    return signal.remez(numtaps=numtaps, bands=bands, desired=desired, Hz=fs)
