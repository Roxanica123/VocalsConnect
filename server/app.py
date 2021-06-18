import json

from flask import Flask, Response
from flask import request
from flask import render_template

from exceptions.split_exception import SplitException
from predictions_system.feature_extraction.feature_function import FeatureFunction
from predictions_system.feature_extraction.used_feature_function import get_mel_spec
from predictions_system.model.genres import genres
from predictions_system.prediction_system import PredictionSystem
from responses.bad_request import BadRequest
from responses.ok import Ok
from responses.server_error import ServerError
from song_collection.spotify_uri_collector import SpotifyURICollector

app = Flask(__name__)
UPLOADS_PATH = './temporary_uploads/'
prediction_system = PredictionSystem(input_shape=(646, 128, 1), output_size=24,
                                     load_path_weights="./predictions_system/model/model_weights/model",
                                     out_folder=UPLOADS_PATH + "split",
                                     genres_mapping=genres,
                                     predictions_path="./predictions_system/model/predictions_without_kids",
                                     feature_function=FeatureFunction(get_mel_spec, {"add_dimension": True}, "mel",
                                                                      requires_to_list=False),
                                     seconds_per_segment=15, additional_segments_seconds_delay=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
collection_system = SpotifyURICollector()


@app.route('/')
def hello_world():
    return render_template('upload.html', name="cv")


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files.keys():
        return BadRequest("A file was not provided")
    f = request.files['file']
    save_path = UPLOADS_PATH + request.files['file'].filename
    try:
        f.save(save_path)
        prediction_result = prediction_system.predict(path=save_path, filename=request.files['file'].filename)
        return Ok(prediction_result)
    except SplitException as e:
        return BadRequest(str(e))
    except:
        return ServerError("Something went wrong, maybe try again?")

