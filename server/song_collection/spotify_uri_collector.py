import requests

from song_collection.authentication import Authentication


class SpotifyURICollector:
    def __init__(self):
        self.authentication = Authentication()

    def get_albums_uri_for_genre(self, genre, limit=100):
        url = "https://api.spotify.com/v1/recommendations?limit={}&seed_genres={}".format(limit, genre)
        response = self.requests_get(url)
        return [track["album"]["uri"] for track in response.json()["tracks"]]

    def get_headers(self):
        headers = {"Authorization": self.authentication.get_bearer_token(), "Accept": "application/json",
                   "Content-Type": "application/json"}
        return headers

    def get_tracks_uris_from_ids(self, ids):
        url = "https://api.spotify.com/v1/tracks/"
        uris = []
        for track_id in ids:
            uris.append(self.requests_get(url + track_id).json()["uri"])
        return uris

    def requests_get(self, url):
        return requests.get(url, headers=self.get_headers())
