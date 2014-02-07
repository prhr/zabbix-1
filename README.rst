zabbix
======

Home page: https://github.com/erik-stephens/zabbix 
 
.. image:: https://api.travis-ci.org/erik-stephens/zabbix.png?branch=master,develop
   :target: http://travis-ci.org/erik-stephens/zabbix
 

Pythonic interface to Zabbix API with the following goals:

- Be self-documenting.  Should not have to flip between the Zabbix API
  docs and the python console.

- Be discoverable.  Should not have to be familiar with the Zabbix API
  to get started.  Relationships between Zabbix objects should be easy
  and natural to discover.  Want to avoid being a thin wrapper around
  the JSON api like this::

    params = dict(...)
    group = api.response('hostgroup.get', params)
    hosts = api.response('host.get', groupids=group['result'][0]['groupid'])

  in favor of something more pythonic like this::

    group = api.get_hostgroup('name', 'MyGroup')
    hosts = group.hosts()

- Support adhoc analysis.  Zabbix is great at collecting data and
  triggering alerts, but makes it difficult to navigate the data.
  Coupled with the likes of IPython Notebook & Pandas, it should be
  easy to analyze and visual the data.  Even better, notebooks can be
  saved and shared as a kind of dashboard or report, which can be
  re-evaluated as needed or captured as a snapshot to PDF.

- Minimize server load and improve latency with aggressive caching of objects.
