#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division

import logging
import os
import json

from lib.routes import r_map
from lib.network import net_request
from lib.db import echo
from lib import config
from lib.network import mserver
import f_modules

config = config.EnvConfig()  # config.JsonConfig('./config.json')
SERVER_ADDRESS = (HOST, PORT) = '', config.m_ports.auth
REQUEST_QUEUE_SIZE = 1

log = logging.getLogger(__name__)
logging.basicConfig(level='DEBUG')


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
        route_function = r_map.search_route(input_dictionary=request_json,
                                            routes=f_modules.routes,
                                            request_schemas=f_modules.schemas)
        if route_function:
            result = route_function(request_json, ldb)
        else:
            result = net_request.make_answer_json(answer_code=net_request.answer_codes['failed'],
                                                  body='request format error')

        # send answer to request
        result = json.dumps(result)
        resp = result.encode('utf-8')
        client.send(resp)

    log.info("Closed connection")
    client.close()


if __name__ == '__main__':
    ldb = echo.EchoDB(db_host=config.get('DB_HOST'),
                      db_name=config.get('DB_NAME'),
                      db_user=config.get('DB_USER'),
                      db_pass=config.get('DB_PASS'))
    mserver.micro_server(SERVER_ADDRESS, handle_request)
