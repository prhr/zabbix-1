
from datetime import datetime
from . import ApiObject


class Host(ApiObject):
    """
    [Zabbix Host](https://www.zabbix.com/documentation/2.2/manual/api/reference/host/object)
    """

    @classmethod
    def by_name(C, api, name):
        """
        Return a new `Host` with matching `name`.
        """
        params = dict(
            output = 'extend',
            filter = dict(name=name),
            selectGroups = True,
            selectItems = True,
        )
        result = api.response('host.get', **params).get('result')
        if not result:
            return None
        return C(api, **result[0])


    def process_refs(I, attrs):
        I.groups = {}
        if 'groups' in attrs:
            for group in attrs['groups']:
                I.groups[group['name']] = HostGroup(I._api, **group)

        I.items = {}
        if 'items' in attrs:
            for item in attrs['items']:
                I.items[item['key_']] = Item(I._api, **item)
                

    def items(I):
        """
        List of associated `Items`.
        """
        return [Item(I._api, **item) for item in
                I._api.response('item.get', output='extend', hostids=I.id).get('result')]


    def triggers(I):
        """
        List of associated `Triggers`.
        """
        return [Trigger(I._api, **trigger) for trigger in
                I._api.response('trigger.get', output='extend', hostids=I.id).get('result')]


    PROPS = dict(
        hostid = dict(
            doc = "ID of the host.",
            id = True,
            readonly = True,
        ),
        host = dict(
            doc = "Technical name of the host.",
        ),
        available = dict(
            doc = "Availability of the agent.",
            kind = int,
            readonly = True,
            vals = {
                0: 'unknown (default)',
                1: 'available',
                2: 'unavailable',
            },
        ),
        disable_until = dict(
            doc = "The next polling time of an unavailable Zabbix agent.",
            kind = datetime,
            readonly = True,
        ),
        error = dict(
            doc = "Error text if Zabbix agent is unavailable.",
            readonly = True,
        ),
        errors_from = dict(
            doc = "Time when Zabbix agent became unavailable.",
            kind = datetime,
            readonly = True,
        ),
        flags = dict(
            doc = "Origin of the host.",
            kind = int,
            readonly = True,
            vals = {
                0: 'a plain host',
                4: 'a discovered host',
            },
        ),
        ipmi_authtype = dict(
            doc = "IPMI authentication algorithm.",
            kind = int,
            vals = {
                -1: 'default',
                0 : 'none',
                1 : 'MD2',
                2 : 'MD5',
                4 : 'straight',
                5 : 'OEM',
                6 : 'RMCP+',
            },
        ),
        ipmi_available = dict(
            doc = "Availability of IPMI agent.",
            kind = int,
            readonly = True,
            vals = {
                0: 'unknown (default)',
                1: 'available',
                2: 'unavailable',
            },
        ),
        ipmi_disable_until = dict(
            doc = "The next polling time of an unavailable IPMI agent.",
            kind = datetime,
            readonly = True,
        ),
        ipmi_error = dict(
            doc = "Error text if IPMI agent is unavailable.",
            readonly = True,
        ),
        ipmi_errors_from = dict(
            doc = "Time when IPMI agent became unavailable",
            kind = datetime,
            readonly = True,
        ),
        ipmi_password = dict(
            doc = "IPMI password",
        ),
        ipmi_privilege = dict(
            doc = "IPMI privilege level.",
            kind = int,
            vals = {
                1: 'callback',
                2: 'user (default)',
                3: 'operator',
                4: 'admin',
                5: 'OEM',
            },
        ),
        ipmi_username = dict(
            doc = "IPMI username",
        ),
        jmx_available = dict(
            doc = "Availability of JMX agent.",
            kind = int,
            readonly = True,
            vals = {
                0: 'unknown (default)',
                1: 'available',
                2: 'unavailable',
            },
        ),
        jmx_disable_until = dict(
            doc = "The next polling time of an unavailable JMX agent.",
            kind = datetime,
            readonly = True,
        ),
        jmx_error = dict(
            doc = "Error text if JMX agent is unavailable.",
            readonly = True,
        ),
        jmx_errors_from = dict(
            doc = "Time when JMX agent became unavailable.",
            kind = datetime,
            readonly = True,
        ),
        maintenance_from = dict(
            doc = "Starting time of the effective maintenance.",
            kind = datetime,
            readonly = True,
        ),
        maintenance_status = dict(
            doc = "Effective maintenance status.",
            kind = int,
            readonly = True,
            vals = {
                0: 'no maintenance (default)',
                1: 'maintenance in effect',
            },
        ),
        maintenance_type = dict(
            doc = "Effective maintenance type.",
            kind = int,
            readonly = True,
            vals = {
                0: 'maintenance with data collection (default)',
                1: 'maintenance without data collection',
            },
        ),
        maintenanceid = dict(
            doc = "ID of the `Maintenance` that is currently in effect on the host.",
            readonly = True,
        ),
        name = dict(
            doc = "Visible name of the host, defaults to `host` property value.",
        ),
        proxy_hostid = dict(
            doc = "ID of the `Proxy` that is used to monitor the host.",
        ),
        snmp_available = dict(
            doc = "Availability of SNMP agent.",
            kind = int,
            readonly = True,
            vals = {
                0: 'unknown (default)',
                1: 'available',
                2: 'unavailable',
            },
        ),
        snmp_disable_until = dict(
            doc = "The next polling time of an unavailable SNMP agent.",
            kind = datetime,
            readonly = True,
        ),
        snmp_error = dict(
            doc = "Error text if SNMP agent is unavailable.",
            readonly = True,
        ),
        snmp_errors_from = dict(
            doc = "Time when SNMP agent became unavailable.",
            kind = datetime,
            readonly = True,
        ),
        status = dict(
            doc = "Status and function of the host.",
            kind = int,
            vals = {
                0: 'monitored host (default)',
                1: 'unmonitored host',
            },
        ),
    )

# These import down here to work around circular imports.
from .hostgroup import HostGroup
from .item import Item
from .trigger import Trigger
