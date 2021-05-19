import json

from flask import Response


class ServerError(Response):
    def __init__(self, message: str, status_code=500):
        super().__init__(status=status_code)
        self.headers['Access-Control-Allow-Origin'] = '*'
        self.data = json.dumps({"error": message})
