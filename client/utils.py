from connection_module import com_switch
from data_config import ad
from data_config import atDict
from data_config import CS

'''
tk.StringVar()
'''
status_message = None

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)


def populate_constants():
    CS.data = com_switch.connection.get_dict_states()
    atDict.data = com_switch.connection.get_dict_acc_type()
    ad.data = com_switch.connection.get_users()
