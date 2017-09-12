import json
import socket
import time

from connection.connect_base import ConnectBase
from data_config import CaseData
from data_config import StepData
from data_config import atDict
from user import user


class ServerConnection(ConnectBase):
    """
    todo read connection setting fromUI and set in innit.
    reset and change this value by Setters and getters methods.
    """

    def add_user(self, user):
        pass

    def __init__(self, **kwargs):
        """

        :param kwargs:
            adres - IP of remote server
            port - port number on remote server.
        """
        self.port = kwargs.get('port', 12345)
        self.adres = kwargs.get('adres', "127.0.0.1")

    # todo metoda na init słowników

    def configure(self, servaddr):
        # self.port = port
        self.adres = servaddr

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
                s.connect((self.adres, self.port))
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
               "path": "/case"}
        return self._read_data(json.dumps(req))

    def get_delate_by_id(self, idx):
        """
        Po zapisaniu wpisu potrzeba go pobrac z serwera by dostac jego
        :param idx:
        :return:
        """
        request = {"method": "GET",
                   "path": "/case/id/" + idx}
        return self._read_data(json.dumps(request))

    def get_case_by_applicant(self, idx):
        request = {"method": "GET",
                   "path": "/case/applicant/" + idx}
        return self._read_data(json.dumps(request))

    def get_delate_by_assign(self, idx):
        request = {"method": "GET",
                   "path": "/case/assign/" + idx}
        return self._read_data(json.dumps(request))

    def get_steps(self, idx):
        request = {"method": "GET",
                   "path": "/steps/id/" + str(idx)}
        return self._read_data(json.dumps(request))

    def put_case(self, delate):
        """
        Aktualizacja wpisu.
        :param delate:
        :return:
        """
        requestparams = {CaseData.NAME: delate.name,
                         CaseData.DESCRIPTION: delate.description,
                         CaseData.STATUS: str(delate.status)}
        if int(user.user_type) == int(atDict.admin) and str(delate.assigned) != "":
            requestparams[CaseData.ASSIGNED] = str(delate.assigned)

        request = {"method": "PUT",
                   "path": "/case/id/" + delate.id,
                   "params": requestparams}
        return self._read_data(json.dumps(request))

    def post_case(self, delate):
        """
        Stworzenie wpisu
        :param delate:
        :return: ID utworzonego wpisu
        """
        requestparams = {CaseData.NAME: delate.name,
                         CaseData.DESCRIPTION: delate.description,
                         CaseData.APPLICANT: str(user.user_id),
                         CaseData.STATUS: str(delate.status)}
        if int(user.user_type) == int(atDict.admin) and str(delate.assigned) != "":
            requestparams[CaseData.ASSIGNED] = str(delate.assigned)

        request = {"method": "POST",
                   "path": "/case",
                   "params": requestparams}

        return self._read_data(json.dumps(request))

    def post_step(self, comment):
        requestparams = {StepData.COMMENT: comment[StepData.COMMENT],
                         "delateid": comment[StepData.DELATE_ID]}
        request = {"params": requestparams,
                   "method": "POST",
                   "path": "/steps"}

        return self._read_data(json.dumps(request))

    def put_step(self, comment):
        requestparams = {StepData.COMMENT: comment[StepData.COMMENT]}
        request = {"params": requestparams,
                   "method": "PUT",
                   "path": "/steps/id/" + comment[StepData.ID]}

        return self._read_data(json.dumps(request))

    def get_users(self):
        request = {"method": "GET",
                   "path": "/users"}
        return self._read_data(json.dumps(request))

