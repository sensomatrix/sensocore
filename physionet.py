from wfdb import rdrecord
from signalobject import Signal
from timeutils import generateTimeArrayFromNumberOfSamples
"""pb_dir: ex : if database is in https://physionet.org/physiobank/database/mghdb/, pb_dir will be mghdb
record_name is the name of the file without the extension ex: mgh002
"""
def import_from_physio(record_name, pb_dir):
    try:
        record = rdrecord(record_name, pb_dir=pb_dir)
    except:
        raise
    fs = record.fs
    comments = record.comments
    siglist = []
    for index, channel in enumerate(record.sig_name):
        sig_name = channel
        sig_samples = record.p_signal[:,index]
        sig_timearray = generateTimeArrayFromNumberOfSamples(fs, sig_samples.size)
        sig = Signal(sig_samples,
                     time_array=sig_timearray,
                     fs=fs,
                     name=sig_name,
                     type="notype")
        siglist.append(sig)
    return siglist, comments
