from scipy.signal import welch, spectrogram


def compute_psd(samples_array, fs):
    fbins, pxx = welch(samples_array, fs=fs, nperseg=int(min((fs, len(samples_array)))))
    return fbins, pxx


def compute_time_freq(samples_array, fs):
    f, t, Sxx = spectrogram(samples_array, fs)
    return f, t, Sxx
