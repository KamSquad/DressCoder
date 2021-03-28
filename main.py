#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division

import logging
import os
import json

from lib.network import request
from lib.db import database
from lib import config
from lib.network import mserver

config = config.JsonConfig('./config.json')
log = logging.getLogger(__name__)
SERVER_ADDRESS = (HOST, PORT) = '', config.value['mservice']['port']
REQUEST_QUEUE_SIZE = 1


def handle_request(client):
    """
    Main microservice function to parse input requests
    :param client:
    :return:
    """
    log.debug('Child PID: {pid}. Parent PID {ppid}'.format(
        pid=os.getpid(),
        ppid=os.getppid()
    ))
    while True:
        request_obj = client.recv(1024)
        if not request_obj:
            break

        # print('ok')
        request_json = json.loads(request_obj.decode('utf-8'))
        # print(request_json)

        if 'request' in request_json:  # check request object exist
            # TEST
            if request_json['request'] == 'test':
                result = request.make_answer_json(answer_code=request.answer_codes['success'],
                                                  body='ping: ok')
            # USER TOKEN CHECK REQUEST
            # request_json = {'request': 'auth',
            #                 'value': 'aaaa-bbbb-cccc-dddd'
            #                 }
            elif request_json['request'] == 'auth' and 'body' in request_json:
                # print(request_json)
                user_token = db.check_user_token(user_token=request_json['body'])
                if user_token:
                    result = request.make_answer_json(answer_code=request.answer_codes['success'],
                                                      body=user_token)
                else:
                    result = request.make_answer_json(answer_code=request.answer_codes['login_failed'],
                                                      body='token invalid')
            else:
                result = request.make_answer_json(answer_code=request.answer_codes['failed'],
                                                  body='request format error')
        else:
            # fail
            result = request.make_answer_json(answer_code=request.answer_codes['failed'],
                                              body='no request header')

        # send answer to request
        result = json.dumps(result)
        resp = str(result).encode('utf-8')
        client.send(resp)

    log.info("Closed connection")
    client.close()


if __name__ == '__main__':
    logging.basicConfig(level='DEBUG')
    db = database.Database()
    mserver.micro_server(SERVER_ADDRESS, handle_request)
