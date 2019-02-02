from scipy import signal

def design_FIR_ls(numtaps, bands, desired, fs):
    return signal.firls(numtaps, bands, desired, fs=fs)