import logging
import datetime
import json
import requests
import uuid


class ElasticHandler(logging.Handler):
    def __init__(self, url, token=False, elastic_index=False):
        """ It supports Basic Authentication only

        The <token> is computed as base64(USERNAME:PASSWORD)
        If elastic_index not provided then logger_name will be used for default index
        """
        super(ElasticHandler, self).__init__()
        self.url = url
        self.token = token
        self.elastic_index = elastic_index

    def emit(self, record):
        headers = {"Content-type": "application/json"}
        if self.token:
            headers['Authorization'] = 'Basic ' + self.token

        if not self.elastic_index:
            self.elastic_index = 'python-elastic-logstash' if record.__dict__['name'] == '__main__' else record.__dict__['name']

        self.url += '/' + self.elastic_index + '/_doc/' + str(uuid.uuid1())

        log_entry = self.format(record)
        response = ''

        try:
            response = requests.post(self.url, log_entry, headers=headers).content
        except requests.exceptions.ConnectionError:
            print('Unable to connect elastic host')

        return response


class ElasticFormatter(logging.Formatter):
    def __init__(self, logger_name=None):
        super(ElasticFormatter, self).__init__()
        self.logger_name = logger_name

    def format(self, record):
        data = {'message': record.msg,
                'timestamp': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')}

        if self.logger_name:
            data['logger_name'] = self.logger_name

        extra = record.__dict__.get('elastic_fields')
        if extra:
            for key, value in extra.items():
                data[key] = value

        return json.dumps(data)
