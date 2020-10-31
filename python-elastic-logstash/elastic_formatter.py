import logging
import datetime
import json

class ElasticFormatter(logging.Formatter):
    def __init__(self, task_name=None):
        super(ElasticFormatter, self).__init__()
        self.task_name = task_name

    def format(self, record):
        data = {'message': record.msg,
                'timestamp': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')}

        if self.task_name:
            data['task_name'] = self.task_name

        extra = record.__dict__.get('elastic_fields')
        if extra:
            for key, value in extra.items():
                data[key] = value

        return json.dumps(data)
