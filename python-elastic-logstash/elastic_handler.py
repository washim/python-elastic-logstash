import logging
import requests

class ElasticHandler(logging.Handler):
    def __init__(self, url, token=False):
        """ It supports Basic Authentication only
        The <token> is computed as base64(USERNAME:PASSWORD)
        """
        super(ElasticHandler, self).__init__()
        self.url = url
        self.token = token

    def emit(self, record):
        headers = {"Content-type": "application/json"}
        if self.token:
            headers['Authorization'] = 'Basic ' + self.token

        log_entry = self.format(record)
        response = requests.post(self.url, log_entry, headers=headers)

        return response.content
