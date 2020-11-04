import logging
import datetime
import json
import requests
import uuid
import socket


class ElasticHandler(logging.Handler):
    def __init__(self, url, token='', elastic_index=''):
        """ It supports Basic Authentication only

        The <token> is computed as base64(USERNAME:PASSWORD)
        If elastic_index not provided then logger_name will be used for default index
        """
        super(ElasticHandler, self).__init__()
        self.url = url
        self.url_duplicate = url
        self.token = token
        self.elastic_index = elastic_index

    def emit(self, record):
        headers = {"Content-type": "application/json"}
        if self.token:
            headers['Authorization'] = 'Basic ' + self.token

        if not self.elastic_index:
            self.elastic_index = 'python-elastic-logstash' if record.__dict__['name'] == '__main__' else record.__dict__['name']

        self.elastic_index = self.elastic_index.lower()
        for item in ['.', '#', '_', '+', '$', '@', '&', '*', '!', '(', ')', '=', '|']:
            self.elastic_index = self.elastic_index.replace(item, '-')

        self.url += '/' + self.elastic_index + '/_doc/' + str(uuid.uuid1())

        response, log_entry = '', self.format(record)

        if 'message' not in log_entry:
            log_entry = json.dumps({
                'message': log_entry,
                'source_host': socket.gethostbyname(socket.gethostname()),
                'timestamp': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            })

        try:
            response = requests.post(self.url, log_entry, headers=headers).json()
            if response.get('error'):
                print('Elastic Search Error: ' + str(response['error']['reason']))

        except requests.exceptions.ConnectionError:
            print('Unable to connect elastic host')

        self.url = self.url_duplicate

        return response


class ElasticFormatter(logging.Formatter):
    def __init__(self):
        super(ElasticFormatter, self).__init__()

    def format(self, record):
        data = {
            'message': record.msg,
            'logger_name': record.name,
            'source_host': socket.gethostbyname(socket.gethostname()),
            'timestamp': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        }

        extra = record.__dict__.get('elastic_fields')
        if extra:
            for key, value in extra.items():
                data[key] = value

        return json.dumps(data)
