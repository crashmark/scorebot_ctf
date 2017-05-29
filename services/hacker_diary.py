#!/usr/bin/env python3
# hacker_diary_interface by Gabriele Musco (GabMus)
"""
Copyright (C) 2017 Gabriele Musco

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

from urllib.parse import urlencode
import requests
import time
import hashlib

from random import randint, choice

token=None
flags=dict()

def _makeRequest(server, uri, method, data=None, textOnly=False, token=None):
    if data and method=='POST':
        if token:
            r = requests.post(server+uri, data=data, headers={'Authorization': 'JWT '+token})
        else:
            r = requests.post(server+uri, data=data)
    else:
        if token:
            r = requests.get(server+uri, headers={'Authorization': 'JWT '+token})
        else:
            r = requests.get(server+uri)
    if textOnly:
        return r.text
    else:
        return r.json()

def _register(server, username, password, first_name=None, last_name=None, email=None):
    data={'username':username, 'password':password}
    if first_name:
        data['first_name']=first_name
    if last_name:
        data['last_name']=last_name
    if email:
        data['email']=email
    return _makeRequest(server, '/register/', 'POST', data=data)

def _login(server, username, password):
    data={'username': username, 'password': password}
    return _makeRequest(server, '/login/', 'POST', data=data)

def _getEntry(server, entryid, token):
    return _makeRequest(server, '/entries/'+entryid, 'GET', token=token)

def _entriesPost(server, token, entry):
    data={'entry': entry}
    return makeRequest('/entries/', 'POST', data=data, token=token)

def setFlag(host, port, flag):
    global token
    global flags
    server=':'.join([host, port])
    username=''.join(choice(string.ascii_letters + string.digits) for _ in range(20))
    password=''.join(choice(string.ascii_letters + string.digits) for _ in range(20))
    _register(server, 'scorebot_'+ username, password)
    token = _login(username, password)['token']
    flag = hashlib.sha1(''.join(choice(string.ascii_letters + string.digits) for _ in range(20)).encode()).hexdigest()
    entry = _entriesPost(server, token, flag)
    flags[entry['id']] = entry['hash']
    return {'flag_id': entry['id'], 'token': token}

def getFlag(host, port, flag_id, token):
    server=':'.join([host, port])
    return _getEntry(server, flag_id, token)['hash']
