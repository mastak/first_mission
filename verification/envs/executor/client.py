import os
import pwd
import sys
import json
import socket
import cgi
import telnetlib

from executor.execs import Runner


class RefereeClient(object):

    TIMEOUT_SOCKET = 12000000
    RECV_DATA_SIZE = 100000000
    DEFAULT_CONNECTION_HOST = '127.0.0.1'
    TERMINATOR = b'\0'

    def __init__(self, connect_port, connection_host=None):
        if connection_host is None:
            connection_host = self.DEFAULT_CONNECTION_HOST
        self._client = telnetlib.Telnet(connection_host, connect_port)

    @property
    def socket(self):
        return self._client.get_socket()

    def request(self, data, skipp_result=None):
        data_json = self._to_json(data)
        self._write(data_json)
        if skipp_result is None:
            result = self._get_response()
            # print("=-"*40)
            # print(result)
            return json.loads(result)

    def _to_json(self, data):
        try:
            return json.dumps(data)
        except TypeError:
            result = data.get('result')
            error = u'TypeError: {0} is wrong data type'.format(cgi.escape(str(type(result))))
            return json.dumps({
                'do': 'exec_fail',
                'text': error
            })

    def _get_response(self):
        data_response = ''
        no_data_counter = 100
        while True:
            new_data = self._recive_data()
            if not new_data:
                no_data_counter -= 1
                if not no_data_counter:
                    raise ValueError('No data')
            data_response += new_data
            if self.TERMINATOR in new_data:
                recv = data_response.split(self.TERMINATOR)[0]
                return recv

    def _write(self, data):
        self._client.write(data.encode() + self.TERMINATOR)

    def _recive_data(self, tries=4):
        self.socket.settimeout(self.TIMEOUT_SOCKET)
        try:
            return self.socket.recv(self.RECV_DATA_SIZE)
        except socket.error as e: # TODO: (errno, msg):
            # if errno != 4:
            #     tries -= 1
            #     if not tries:
            #         raise
            raise
            # return self._recive_data(tries=tries)


def start():
    try:
        robot_uid, robot_gid = pwd.getpwnam('robot')[2:4]
    except KeyError:
        pass  # for dev version
    else:
        try:
            os.setgid(robot_gid)
            os.setuid(robot_uid)
        except OSError:
            pass  # for dev version

    connect_port = int(sys.argv[1])
    exec_name = sys.argv[2]

    client = RefereeClient(connect_port)
    execution_data = client.request({
        'status': 'connected',
        'exec_name': exec_name,
        'pid': os.getpid(),
    })
    runner = Runner()
    while True:
        results = runner.execute(execution_data)
        execution_data = client.request(results)


if __name__ == '__main__':
    start()
