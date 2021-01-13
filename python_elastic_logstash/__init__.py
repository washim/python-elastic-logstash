import logging
import datetime
import json
import requests
import uuid
import socket
import os


class ElasticHandler(logging.Handler):
    def __init__(self, url, environment='dev', token='', elastic_index=''):
        """ It supports Basic Authentication only

        The <token> is computed as base64(USERNAME:PASSWORD)
        If elastic_index not provided then logger_name will be used for default index
        """
        super(ElasticHandler, self).__init__()
        self.url = url
        self.environment = environment
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

        url = self.url + '/' + self.elastic_index + '/_doc/' + str(uuid.uuid1())

        response, log_entry = '', self.format(record)

        log_entry['source_host'] = socket.gethostbyname(socket.gethostname())
        log_entry['source_environment'] = self.environment
        log_entry['timestamp'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        backup_logs_path = os.path.join(os.getcwd(), '.python_elastic_logstash')

        try:
            response = requests.post(url, json.dumps(log_entry), headers=headers).json()
            if response.get('error'):
                print('Elastic Search Error: ' + str(response['error']['reason']))

            if os.path.exists(backup_logs_path):
                with open(backup_logs_path, 'r') as fp:
                    log_data = fp.read()

                bres = requests.post(f'{self.url}/_bulk', data=log_data, headers={'Content-Type': 'application/json'}).json()
                if bres.get('errors') is False:
                    log_entry['message'] = '%d items recovered from previously failed logstash.' % len(bres['items'])
                    requests.post(url, json.dumps(log_entry), headers=headers).json()
                    os.remove(backup_logs_path)

        except requests.exceptions.ConnectionError:
            print('Unable to connect elastic host. Logstash will restore when available.')
            with open(backup_logs_path, 'a+') as fp:
                fp.write("""{"index":{"_index":"%s","_id":"%s"}}""" % (self.elastic_index, str(uuid.uuid1())) + "\n")
                fp.write(json.dumps(log_entry) + "\n")

        return response


class ElasticFormatter(logging.Formatter):
    def __init__(self):
        super(ElasticFormatter, self).__init__()

    def format(self, record):
        data = dict(message=record.msg, logger_name=record.name)
        extra = record.__dict__.get('elastic_fields')
        if extra:
            for key, value in extra.items():
                data[key] = value

        return data
