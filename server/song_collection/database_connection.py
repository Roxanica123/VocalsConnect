import pymongo

from song_collection.credentials import MONGO_CONNECTION_URL


class DatabaseConnection:
    def __init__(self):
        self.client = pymongo.MongoClient(MONGO_CONNECTION_URL).Songs

    def insert_track_info(self, track_info):
        collection = self.client["tracks"]
        if self.is_song_in_database(track_info["song_id"]) is False:
            collection.insert_one(track_info)

    def is_song_in_database(self, song_id):
        collection = self.client["tracks"]
        return collection.count_documents({"song_id": song_id}) > 0

    def get_song_by_id(self, song_id):
        collection = self.client["tracks"]
        return collection.find_one({"song_id": song_id})
