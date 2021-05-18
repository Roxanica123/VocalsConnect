import json

from flask import Flask, Response
from flask import request
from flask import render_template

from predictions_system import FeatureFunction, get_mel_spec
from predictions_system.model.genres import genres
from predictions_system.prediction_system import PredictionSystem
from song_collection.spotify_uri_collector import SpotifyURICollector

app = Flask(__name__)
UPLOADS_PATH = './temporary_uploads/'
prediction_system = PredictionSystem(input_shape=(646, 128, 1), output_size=25,
                                     load_path_weights="./predictions_system/model/model_weights/model",
                                     out_folder=UPLOADS_PATH + "split",
                                     genres_mapping=genres,
                                     predictions_path="./predictions_system/model/predictions",
                                     feature_function=FeatureFunction(get_mel_spec, {"add_dimension": True}, "mel",
                                                                      requires_to_list=False),
                                     seconds_per_segment=15, additional_segments_seconds_delay=[5, 10])
collection_system = SpotifyURICollector()


@app.route('/')
def hello_world():
    return render_template('upload.html', name="cv")


@app.route('/upload', methods=['POST'])
def upload_file():
    f = request.files['file']
    save_path = UPLOADS_PATH + request.files['file'].filename
    f.save(save_path)
    prediction_result = prediction_system.predict(path=save_path, filename=request.files['file'].filename)

    response = Response(status=200)
    response.data = json.dumps(prediction_result)
    return response
