import logging
import sys
from python_elastic_logstash import ElasticHandler, ElasticFormatter

"""
Provide logger name simple without any special character
Logger name will become as Elastic Search Index
"""
logger = logging.getLogger('python-elastic-logstash')
logger.setLevel(logging.DEBUG)

elasticsearch_endpoint = 'http://localhost:9200'  # No trailing slash

elastic_handler = ElasticHandler(elasticsearch_endpoint, 'dev')  # Second argument is optional
elastic_handler.setFormatter(ElasticFormatter())

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

logger.addHandler(elastic_handler)
logger.addHandler(stream_handler)

# Extra is optional.
extra = {
    'elastic_fields': {
        'version': 'python version: ' + repr(sys.version_info)
    }
}

logger.debug("Python elastic logstash configured", extra=extra)
