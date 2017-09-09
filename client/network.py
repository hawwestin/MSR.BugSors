import json
import socket
import time

from data_config import dd
from data_config import dc
from data_config import atDict
from user import user


class Connection:
    """
    todo read connection setting fromUI and set in innit.
    reset and change this value by Setters and getters methods.
    """

    def __init__(self, port=12345, servaddr="127.0.0.1"):
        self.port = port
        self.servaddr = servaddr

    # todo metoda na init słowników

    def configure(self, servaddr):
        # self.port = port
        self.servaddr = servaddr

    def _read_data(self, request):
        """
        send prepared request and return recived payload.

        Catch some exception and notify user about it.
        :param request: string json prapered to be send
        :return: recived payload.
        """
        request = json.loads(request)
        # if request.get("params", 0) == 0:
        #     request["params"] = {}
        request["token"] = user.token
        request = json.dumps(request)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                # todo spradzenie czy podane argumenty sąpoprawne.
                s.connect((self.servaddr, self.port))
            except socket.gaierror:
                # statsu bar Msg about connection cannot be established
                return ""
            except ConnectionRefusedError:
                #     status bar połączenie nie powiodło się z podanym serwerm
                return ""

            try:
                s.sendall(request.encode())
            except socket.gaierror:
                # Sending data was interrupt by network error.
                return ""

            data = self._receive_timeout(s, 1)
            if len(data) > 0:
                try:
                    payload = json.loads(data)
                except Exception:
                    # Returned Data are unreadable
                    return ''
                if payload.get("status", 0) == "200":
                    return payload["content"]
                elif payload.get("status", 0) == "400":
                    # set msg
                    return ''
                elif payload.get("status", 0) == "401":
                    # Unathorised
                    return ''
            else:
                # set status bar with msg. | No Content provided by server.
                return ''

    @staticmethod
    def _receive_timeout(the_sock, timeout=2):
        the_sock.setblocking(0)

        total_data = []
        begin = time.time()

        while 1:
            if total_data and time.time() - begin > timeout:
                break
            elif time.time() - begin > timeout:
                break

            try:
                result = the_sock.recv(4096)
                while (len(result) > 0):
                    total_data.append(result.decode())
                    result = the_sock.recv(4096)

                if len(total_data):
                    break
                    # begin = time.time()
                else:
                    time.sleep(0.1)
            except:
                pass

        return ''.join(total_data)

    def login(self):
        """
        Send crudential to fetch user data and communication token
        :return: json content
        """
        requestparams = {"login": user.login,
                         "password": user.password}

        request = {"method": "POST",
                   "path": "/users/login",
                   "params": requestparams}
        return self._read_data(json.dumps(request))

    def get_dict_states(self):
        request = {"method": "GET",
                   "path": "/dictionaries/states"}
        return self._read_data(json.dumps(request))

    def get_dict_acc_type(self):
        request = {"method": "GET",
                   "path": "/dictionaries/accounttypes"}
        return self._read_data(json.dumps(request))

    def get_delates(self):
        """
        Pobieranie wartosci dla wpisu o incydencie.
        """
        req = {"method": "GET",
               "path": "/delates"}
        return self._read_data(json.dumps(req))

    def get_delate_by_id(self, idx):
        """
        Po zapisaniu wpisu potrzeba go pobrac z serwera by dostac jego
        :param idx:
        :return:
        """
        request = {"method": "GET",
                   "path": "/delates/id/" + idx}
        return self._read_data(json.dumps(request))

    def GetDelateByAplicant(self, idx):
        request = {"method": "GET",
                   "path": "/delates/applicant/" + idx}
        return self._read_data(json.dumps(request))

    def GetDelateByAssign(self, idx):
        request = {"method": "GET",
                   "path": "/delates/assign/" + idx}
        return self._read_data(json.dumps(request))

    def get_comments(self, idx):
        request = {"method": "GET",
                   "path": "/comments/id/" + str(idx)}
        return self._read_data(json.dumps(request))

    def put_delate(self, delate):
        """
        Aktualizacja wpisu.
        :param delate:
        :return:
        """
        requestparams = {dd.NAME: delate.name,
                         dd.DESCRIPTION: delate.description,
                         dd.STATUS: str(delate.status)}
        if int(user.user_type) == int(atDict.admin) and str(delate.assigned) != "":
            requestparams[dd.ASSIGNED] = str(delate.assigned)

        request = {"method": "PUT",
                   "path": "/delates/id/" + delate.id,
                   "params": requestparams}
        return self._read_data(json.dumps(request))

    def post_delate(self, delate):
        """
        Stworzenie wpisu
        :param delate:
        :return: ID utworzonego wpisu
        """
        requestparams = {dd.NAME: delate.name,
                         dd.DESCRIPTION: delate.description,
                         dd.APPLICANT: str(user.user_id),
                         dd.STATUS: str(delate.status)}
        if int(user.user_type) == int(atDict.admin) and str(delate.assigned) != "":
            requestparams[dd.ASSIGNED] = str(delate.assigned)

        request = {"method": "POST",
                   "path": "/delates",
                   "params": requestparams}

        return self._read_data(json.dumps(request))

    def post_comment(self, comment):
        requestparams = {dc.COMMENT: comment[dc.COMMENT],
                         "delateid": comment[dc.DELATE_ID]}
        request = {"params": requestparams,
                   "method": "POST",
                   "path": "/comments"}

        return self._read_data(json.dumps(request))

    def put_comment(self, comment):
        requestparams = {dc.COMMENT: comment[dc.COMMENT]}
        request = {"params": requestparams,
                   "method": "PUT",
                   "path": "/comments/id/" + comment[dc.ID]}

        return self._read_data(json.dumps(request))

    def get_users(self):
        request = {"method": "GET",
                   "path": "/users"}
        return self._read_data(json.dumps(request))


if __name__ == '__main__':
    pass
else:
    con = Connection()
