import datetime
import base64
import requests
from song_collection.credentials import CLIENT_ID, CLIENT_SECRET


class Authentication:
    def __init__(self):
        self.id = CLIENT_ID
        self.secret = CLIENT_SECRET
        self.bearer_token = None
        self.expiration_time = None
        self.token_duration = 3600

    def get_bearer_token(self):
        if self.token_is_invalid():
            self.generate_new_token()
        return "Bearer "+self.bearer_token

    def token_is_invalid(self):
        now = datetime.datetime.now()
        if self.bearer_token is None or self.expiration_time >= now:
            return True
        return False

    def generate_new_token(self):
        authorization_string = "{}:{}".format(self.id, self.secret)
        encoded_authorization_string = base64.b64encode(authorization_string.encode("ascii")).decode("ascii")
        headers = {"Authorization": "Basic " + encoded_authorization_string}
        data = {"grant_type": "client_credentials"}
        response = requests.post("https://accounts.spotify.com/api/token", data=data, headers=headers)
        self.bearer_token = response.json()["access_token"]
        self.expiration_time = datetime.datetime.now() + datetime.timedelta(seconds=self.token_duration)
