python-elastic-logstash
====================================================
Logstash dynamically ingests, transforms, and ships your data regardless of format or complexity. Derive structure from unstructured data with grok, decipher geo coordinates from IP addresses, anonymize or exclude sensitive fields, and ease overall processing.

Installation
=================

Using pip::

  pip install python-elastic-logstash

Features
=================
1. Sends Python logs in elasticsearch.
2. Works with Python Django.
3. Stop tolerance capability.
4. Overwrite index from custom fields.

If any issues please submit issues in https://github.com/washim/python-elastic-logstash/issues

Usage
=================

For example::

  import logging
  import sys
  from python_elastic_logstash import ElasticHandler, ElasticFormatter

  """
  Provide logger name simple without any special character
  Logger name will become as Elastic Search Index
  """
  logger = logging.getLogger('python-elastic-logstash')
  logger.setLevel(logging.DEBUG)

  elasticsearch_endpoint = 'http://localhost:9200' # No trailing slash

  elastic_handler = ElasticHandler(elasticsearch_endpoint, 'dev')  # Second argument is optional
  elastic_handler.setFormatter(ElasticFormatter())

  logger.addHandler(elastic_handler)

  # Extra is optional.
  extra = {
      'elastic_fields': {
          'version': 'python version: ' + repr(sys.version_info)
      }
  }

  logger.debug("Python elastic logstash configured", extra=extra)

Kibana Create Index Page
===============================

.. image:: https://raw.githubusercontent.com/washim/python-elastic-logstash/master/index.png
  :width: 780
  :align: center

Kibana Discover Page
===============================

.. image:: https://raw.githubusercontent.com/washim/python-elastic-logstash/master/discover.png
  :width: 780
  :align: center

Using Django
===============================
Modify your settings.py

Example::

  LOGGING = {
      ...
      'version': 1,
      'disable_existing_loggers': False,
      'handlers': {
          'elastic_handler': {
              'level': 'DEBUG',
              'class': 'python_elastic_logstash.ElasticHandler',
              'url': 'http://localhost:9200'
          },
          'console': {
              'class': 'logging.StreamHandler'
          },
      },
      'root': {
          'handlers': ['console'],
          'level': 'WARNING',
      },
      'loggers': {
          'django.request': {
              'handlers': ['elastic_handler'],
              'level': 'DEBUG',
              'propagate': True,
          },
          'python-elastic-logstash': {
              'handlers': ['elastic_handler'],
              'level': 'DEBUG',
              'propagate': True,
          },
      }
      ...
  }
