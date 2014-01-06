
from zabbix import Host, HostGroup
from . import api_session


def test_add_host1():
    'Can add a host to a group.'
    with api_session() as api:
        api.mock_reply(result=[{
            "hostid" : "45",
            "name": "MyHost",
            "items": "42",
        }])
        host = Host.by_name(api, 'MyHost')
        api.mock_reply(result=[{
            "hosts": [], 
            "internal": "0", 
            "flags": "0", 
            "groupid": "14", 
            "name": "Puppetized",
        }])
        group = HostGroup.by_name(api, 'MyGroup')
        api.mock_reply(result={
            "hostids": ["40"],
        })
        assert not group.add_host(host)
        api.mock_reply(result={
            "hostids": ["45"],
        })
        assert group.add_host(host)
