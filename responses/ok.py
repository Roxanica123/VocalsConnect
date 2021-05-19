import json

from flask import Response


class Ok(Response):
    def __init__(self, message: dict, status_code=200):
        super().__init__(status=status_code)
        self.headers['Access-Control-Allow-Origin'] = '*'
        self.data = json.dumps(message)
