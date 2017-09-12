from connection import connection
from data_config import ad
from data_config import atDict
from data_config import ds

'''
tk.StringVar()
'''
status_message = None


LARGE_FONT= ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)


def populate_constants():
    ds.dict_state = connection.get_dict_states()
    atDict.atDict = connection.get_dict_acc_type()
    ad.adict = connection.get_users()
