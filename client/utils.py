from data_config import ds
from data_config import atDict
from data_config import ad
from network import con


'''
tk.StringVar()
'''
status_message = None


LARGE_FONT= ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)


def populate_constants():
    ds.dict_state = con.get_dict_states()
    atDict.atDict = con.get_dict_acc_type()
    ad.adict = con.get_users()
