
from . import ApiObject


class HostGroup(ApiObject):
    """
    [Zabbix HostGroup](https://www.zabbix.com/documentation/2.2/manual/api/reference/hostgroup/object)
    """

    @classmethod
    def create(C, api, name):
        """
        Return id of new `HostGroup` with given `name`.
        """
        params = dict(
            name = name,
        )
        result = api.response('hostgroup.create', **params).get('result')
        return result.get('groupids')[0]


    @classmethod
    def by_name(C, api, name):
        """
        Return a new `HostGroup` with matching `name`.
        """
        params = dict(
            output = 'extend',
            filter = dict(name=name),
            selectHosts = True,
        )
        result = api.response('hostgroup.get', **params).get('result')
        if not result:
            return None
        return C(api, **result[0])


    def process_refs(I, attrs):
        I.hosts = {}
        if 'hosts' in attrs:
            for host in attrs['hosts']:
                I.hosts[host['name']] = Host(I._api, **host)


    # def hosts(I):
    #     """
    #     List of `Hosts` in this group.
    #     """
    #     return [Host(I._api, **host) for host in
    #             I._api.response('host.get', output='extend', groupids=I.id).get('result')]


    def add_host(I, host):
        """
        True if successfully added `host` to this group.
        """
        params = dict(
            groups = [dict(groupid = I.id)],
            hosts = [dict(hostid = host.id)],
        )
        reply = I._api.response('host.massadd', **params)

        return [host.id] == reply['result'].get('hostids', [])


    def __repr__(I):
        return "{}[{}]".format(I.__class__.__name__, I.name.val)


    PROPS = dict(
        groupid = dict(
            doc = "ID of the host group.",
            id = True,
            readonly = True,
        ),
        name = dict(
            doc = "Name of the host group.",
        ),
        flags = dict(
            doc = "Origin of the host group.",
            kind = int,
            readonly = True,
            vals = {
                0: 'a plain host group',
                4: 'a discovered host group',
            },
        ),
        internal = dict(
            doc = "Whether the group is used internally by the system. An internal group cannot be deleted.",
            kind = int,
            readonly = True,
            vals = {
                0: 'not internal (default)',
                1: 'internal',
            },
        ),
    )

# These import down here to work around circular imports.
from .host import Host
