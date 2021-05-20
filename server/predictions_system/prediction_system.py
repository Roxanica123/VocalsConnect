import shutil

import tensorflow as tf
import numpy as np
import os
from typing import List

from predictions_system.feature_extraction.audio_splitter import AudioSplitter
from predictions_system.feature_extraction.feature_extractor import FeaturesExtractor
from predictions_system.feature_extraction.feature_function import FeatureFunction
from predictions_system.feature_extraction.segment_splitter import SegmentsSplitter
from predictions_system.model.cnn_lstm_model import CNNLSTMModel
from predictions_system.model.kdtree import KDTree


class PredictionSystem:
    def __init__(self, input_shape, output_size, load_path_weights, out_folder: str, feature_function: FeatureFunction,
                 predictions_path, genres_mapping, seconds_per_segment: int = 15, number_of_neighbours_per_segment=3,
                 additional_segments_seconds_delay: List[int] = None, load_sample_rate=22050, number_of_neighbours=12):
        self.input_shape = input_shape
        self.output_size = output_size
        self.load_path_weights = load_path_weights
        self.genres_mapping = genres_mapping
        self.split_out_folder = out_folder
        self.audio_splitter = AudioSplitter(out_folder=out_folder,
                                            seconds_per_segment=seconds_per_segment)
        self.feature_extractor = FeaturesExtractor(
            segments_splitter=SegmentsSplitter(seconds_per_segment=seconds_per_segment,
                                               additional_segments_seconds_delay=additional_segments_seconds_delay),
            feature_function=feature_function, load_sample_rate=load_sample_rate)
        self.tree = KDTree(number_of_neighbours=number_of_neighbours,
                           number_of_neighbours_for_segment=number_of_neighbours_per_segment,
                           predictions_path=predictions_path)

    def predict(self, path, filename):
        vocals_path = self.audio_splitter.split(path=path)
        features = self.feature_extractor.extract(vocals_path)
        predictions = CNNLSTMModel(input_shape=self.input_shape, output_size=self.output_size,
                                   load_path_weights=self.load_path_weights).predict(tf.stack(features))
        similar_ids = self.tree.get_neighbours(predictions)
        similar_ids = ["https://open.spotify.com/embed/track/" + similar_id for similar_id in similar_ids]
        prediction_mapped = [self.genres_mapping[np.argmax(prediction)] for prediction in predictions]
        self.remove_temporary_files(path, filename)
        return {"genre_predictions": list(set(prediction_mapped)), "similar_songs_ids": list(set(similar_ids))}

    def remove_temporary_files(self, path, filename):
        os.remove(path)
        shutil.rmtree("{}/{}".format(self.split_out_folder, filename.rsplit(".", 1)[0]))
