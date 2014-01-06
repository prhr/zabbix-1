
from zabbix import Host
from . import api_session


def test_items1():
    'Associated items for a host are loaded on-demand.'
    with api_session() as api:
        api.mock_reply(result=[{"hostid":"45","name":"MyHost","items":"42"}])
        host = Host.by_name(api, 'MyHost')
        api.mock_reply(result=[{"itemid":"1","key_":"Memory","value_type":"3"}])
        assert isinstance(host.items, dict)
        assert len(host.items) == 1
        assert 'Memory' in host.items
