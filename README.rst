python-elastic-logstash
====================================================
Logstash dynamically ingests, transforms, and ships your data regardless of format or complexity. Derive structure from unstructured data with grok, decipher geo coordinates from IP addresses, anonymize or exclude sensitive fields, and ease overall processing.

Installation
=================

Using pip::

  pip install python-elastic-logstash

Usage
=================

For example::

  import logging
  import sys
  from python-elastic-logstash import ElasticHandler, ElasticFormatter

  logger = logging.getLogger('python-elastic-logstash')
  logger.setLevel(logging.DEBUG)

  elastic_handler = ElasticHandler('http://localhost:9200')
  elastic_handler.setFormatter(ElasticFormatter(logger.name))

  stream_handler = logging.StreamHandler()
  stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

  logger.addHandler(elastic_handler)
  logger.addHandler(stream_handler)

  extra = {
      'elastic_fields': {
          'version': 'python version: ' + repr(sys.version_info)
      }
  }

  logger.debug("Python elastic logstash configured", extra=extra)
