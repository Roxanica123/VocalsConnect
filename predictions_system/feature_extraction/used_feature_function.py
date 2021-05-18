import librosa
import numpy as np


def get_mel_spec(segment, sample_rate=22050, num_fft=2048, hop_length=512, add_dimension=False):
    spec = librosa.feature.melspectrogram(segment, sr=sample_rate, n_fft=num_fft, hop_length=hop_length)
    spec_db = librosa.power_to_db(spec, ref=np.max)
    spec_db = spec_db.T
    if add_dimension is True:
        spec_db = spec_db[..., np.newaxis]
    return spec_db.tolist()
