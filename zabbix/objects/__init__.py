"""
Implementation of Zabbix API objects.
"""

import json
from datetime import datetime
from ..api import ApiException

__all__ = [
    'ApiObject',
]


class ApiObject(object):
    """
    Base class for all Zabbix objects.
    """

    @property
    def id(I):
        return I._id


    def __init__(I, api, **attrs):
        I._id = None
        I._api = api
        I._props = dict()
        for name in attrs:
            if name not in I.PROPS:
                pass # print("UNKNOWN PROP:", name, attrs[name])
            else:
                spec = I.PROPS[name]
                if spec.get('id'):
                    I._id = attrs[name]
                prop = Property(
                    name = name,
                    val = attrs[name],
                    doc = spec.get('doc'),
                    kind = spec.get('kind', str),
                    readonly = spec.get('readonly'),
                    vals = spec.get('vals'),
                )
                setattr(I, name, prop)
                I._props[name] = prop
        I.process_refs(attrs)

    def process_refs(I, attrs):
        """
        A hook to process object-specific references.
        """
        pass


    def __unicode__(I):
        return json.dumps(I.json(), indent=2, ensure_ascii=False)

    def __str__(I):
        return json.dumps(I.json(), indent=2, encoding='utf-8')

    def __repr__(I):
        return "{}[{}]".format(I.__class__.__name__, I.id)

    def json(I):
        """
        Return all properties as a dict suitable for JSON.
        """
        d = dict()
        for name in I._props:
            prop = getattr(I, name)
            if prop.kind == datetime:
                d[name] = prop.val.isoformat()
            else:
                d[name] = prop.val
            
        return d

    def save(I):
        """
        Publish any changes to zabbix server.
        """
        dirty = dict()
        for name, prop in I._props.items():
            if prop.dirty:
                dirty[name] = prop.val
        if dirty:
            pass # I._api.response('update', params)
        

    def _repr_html_(I):
        rows = [
            '<table><thead><tr><th>Name</th><th>Value</th><th>Type</th><th>Dirty</th><th>Read-Only</th><th>Description</th></tr></thead><tbody>',
        ]
        for name in sorted(I._props):
            prop = I._props[name]
            val = prop.val
            if prop.vals and val in prop.vals:
                val = "{}: {}".format(val, prop.vals[val])
            rows.append("<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(
                name, val, prop.kind.__name__, prop.dirty, prop.readonly, prop.__doc__))
        rows.append('</tbody></table>')

        return '\n'.join(rows)


class Property(object):
    """
    Each attribute of an `ApiObject` is wrapped by this class.
    """

    @property
    def val(I):
        """
        The property's actual value.
        """
        return I._val

    @val.setter
    def val(I, val):
        """
        Set val, ensuring coerced to correct type and dirty flag set when changed.
        """
        if val == I._val:
            return
        if I.readonly and I._val is not None:
            raise ApiException(
                ApiException.INVALID_VALUE,
                'read-only property',
                "already defined as: {}".format(I._val),
            )
        try:
            for xform in I._xforms:
                val = xform(val)
        except Exception as e:
            raise ApiException(
                ApiException.INVALID_VALUE,
                'invalid value',
                "{}: {}: {}".format(I.name, val, e),
            )
        if not isinstance(val, I.kind):
            raise ApiException(
                ApiException.INVALID_VALUE,
                'invalid type',
                "{}: {} is not a {}".format(I.name, val, I.kind.__name__),
            )
        if I.vals is not None and val not in I.vals:
            raise ApiException(
                ApiException.INVALID_VALUE,
                'invalid value',
                "{}: {} not in {}".format(I.name, val, I.vals.keys()),
            )
        I._val = val
        I._dirty = True

    @property
    def dirty(I):
        """
        True if this property's value has been modified.
        """
        return I._dirty


    def __init__(I, name='', doc='', val=None, kind=str, readonly=False, vals=None):
        I.name = name
        I.__doc__ = doc
        if kind == datetime:
            I._xforms = [int, datetime.utcfromtimestamp]
        else:
            I._xforms = [kind]
        I.kind = kind
        I.readonly = readonly
        I.vals = vals
        # Now set the value so that type checking happens
        I._val = None
        I.val = val 
        I._dirty = False


    def __unicode__(I):
        return u"{} [dirty={}, readonly={}]".format(I.val, I.dirty, I.readonly)

    def __str__(I):
        return str(unicode(I))

    def __repr__(I):
        return str(I.val)


    def _repr_html_(I):
        return """
            <table>
              <thead>
                <tr>
                  <th>Value</th>
                  <th>Type</th>
                  <th>Dirty</th>
                  <th>Read-Only</th>
                  <th>Description</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>{}</td>
                  <td>{}</td>
                  <td>{}</td>
                  <td>{}</td>
                  <td>{}</td>
                </tr>
              </tbody>
            </table>
        """.format(I.val, I.kind.__name__, I.dirty, I.readonly, I.__doc__)
