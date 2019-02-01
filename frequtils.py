from scipy.signal import welch, spectrogram


def compute_psd(samplesarray, fs):
    fbins, pxx = welch(samplesarray, fs=fs, nperseg=int(min((fs, len(samplesarray)))))
    return fbins, pxx


def compute_time_freq(samplesarray, fs):
    f, t, Sxx = spectrogram(samplesarray, fs)
    return f, t, Sxx
