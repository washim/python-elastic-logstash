from setuptools import setup
setup(
    name='python_elastic_logstash',
    packages=['python_elastic_logstash'],
    version='0.2.1',
    description='Python logging handler for elastic search.',
    long_description=open('README.rst').read(),
    license='MIT',
    author='Washim Ahmed',
    author_email='washim.ahmed@gmail.com',
    python_requires='>=3',
    url='https://github.com/washim/python-elastic-logstash',
    setup_requires=[
        'requests'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Logging',
    ]
)
