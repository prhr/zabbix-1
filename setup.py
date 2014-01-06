
from setuptools import setup

setup(
    name = 'zabbix',
    version = '0.0.1',
    author = 'Erik Stephens',
    author_email = 'erik@tfks.net',
    description = 'A Pythonic interface to the Zabbix API',
    license = 'MIT',
    keywords = 'zabbix api',
    url = 'http://github.com/erik-stephens/zabbix',
    packages = ['zabbix', 'zabbix.objects'],
    long_description = open('README.rst').read(),
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'License :: OSI Approved :: MIT License',
    ],
)
