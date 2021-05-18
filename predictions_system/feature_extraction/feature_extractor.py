import tensorflow as tf
from multiprocessing import Pool
import librosa

from predictions_system.feature_extraction.feature_function import FeatureFunction
from predictions_system.feature_extraction.segment_splitter import SegmentsSplitter


class FeaturesExtractor:
    def __init__(self, segments_splitter: SegmentsSplitter, feature_function: FeatureFunction,
                 load_sample_rate: int = 22050):
        self.segments_splitter = segments_splitter
        self.feature_function = feature_function
        self.load_sample_rate = load_sample_rate

    def extract(self, path):
        y, sr = librosa.load("{}/clean_vocals.wav".format(path), self.load_sample_rate)
        segments = self.segments_splitter.split(y, sr)
        if segments is None:
            raise Exception("Not enough vocal information to process")
        with Pool(4) as p:
            results = p.map(self.get_features, segments)
            return results

    def get_features(self, segment):
        feature = self.feature_function.feature_function(segment, **self.feature_function.arguments)
        if self.feature_function.requires_to_list is True:
            feature = feature.tolist()
        return tf.convert_to_tensor(feature, dtype=tf.double)
