import soundfile as sf
import librosa
import numpy as np
from spleeter.separator import Separator

from exceptions.split_exception import SplitException


class AudioSplitter:
    def __init__(self, out_folder, seconds_per_segment):
        self.separator = Separator('spleeter:2stems')
        self.out_folder = out_folder
        self.seconds_per_segment = seconds_per_segment

    def split(self, path):
        out_dir_for_song = "{}/{}".format(self.out_folder, path.split("/")[-1].split(".")[0])
        self.separator.separate_to_file(path, self.out_folder, synchronous=True)
        self.clean_silence(out_dir_for_song)
        return out_dir_for_song

    def clean_silence(self, path_to_dir):
        track_path = "{}/vocals.wav".format(path_to_dir)
        wave, sr = librosa.load(track_path)
        rms = librosa.feature.rms(wave)

        non_silent_interval = librosa.effects.split(wave, top_db=35, hop_length=1000)
        result = list(wave[non_silent_interval[0][0]:non_silent_interval[0][1]])
        for i in range(1, len(non_silent_interval)):
            result = result + list(wave[non_silent_interval[i][0]:non_silent_interval[i][1]])
        if len(result) >= sr * self.seconds_per_segment and max(rms[0]) > 0.05:
            sf.write("{}/clean_vocals.wav".format(path_to_dir), np.array(result), sr)
            return True
        else:
            raise SplitException(
                "Not enough vocal information to process. The audio is too quiet or does not contain any vocals.")
