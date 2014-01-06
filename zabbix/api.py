"""
A pythonic interface to the Zabbix API.
"""

import os
import sys
import requests
import json

__all__ = [
    'Api',
    'ApiException',
]


class ApiException(Exception):
    """
    Raised when bad reply from server or error msg in the reply.
    """
    INVALID_REPLY    = -1
    INVALID_VALUE    = -2
    FAILED_AUTH      = -32602

    def __init__(I, code, msg, data):
        I.code = code
        I.msg = msg
        I.data = data

    def __str__(I):
        return "{}: {}: {}".format(I.code, I.msg, I.data)


class Api(object):

    def __init__(I, server, session=None):
        if session is None:
            session = requests.session()
            session.headers['Content-Type'] = 'application/json-rpc'
        I._session = session
        I._endpoint = server + '/api_jsonrpc.php'
        I._id = 0
        I._auth = None


    def login(I, user, password):
        """
        Return true if able to authenticate, false otherwise.  Session
        key is saved in this object for future requests.
        """
        try:
            I._auth = I.response('user.login', user=user, password=password).get('result')
        except ApiException as e:
            if e.code != ApiException.FAILED_AUTH:
                raise
        return bool(I._auth)

           
    def response(I, method, **params):
        """
        Get "raw" response from zabbix server.

        [Zabbix API Docs](https://www.zabbix.com/documentation/2.2/manual/api/reference)
        """
        payload = dict(
            jsonrpc = '2.0',
            method = method,
            params = params,
            id = I._id,
            auth = I._auth,
        )
        response = I._session.post(I._endpoint, data=json.dumps(payload))
        I._id += 1

        if not response.text:
            raise ApiException(ApiException.INVALID_REPLY, 'empty reply', '')
        try:
            reply = json.loads(response.text)
            print("RESPONSE FROM {}: {}\n".format(method, json.dumps(reply, indent=2)))
        except ValueError:
            raise ApiException(ApiException.INVALID_REPLY, 'invalid json', response.text)

        if 'error' in reply:
            err = reply['error']
            raise ApiException(err['code'], err['message'], err['data'])

        return reply
