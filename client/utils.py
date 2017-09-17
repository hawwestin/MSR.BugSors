from client.connection_module import com_switch
from client.data_config import dict_accounts
from client.data_config import dict_account_type
from client.data_config import dict_case_status
from client.data_config import dict_priority
from client.data_config import dict_step_assembly
from client.data_config import dict_step_type

'''
tk.StringVar()
'''
status_message = None

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)


def populate_constants():
    dict_case_status.data = com_switch.connection.get_dict(dict_case_status)
    dict_account_type.data = com_switch.connection.get_dict(dict_account_type)
    dict_accounts.data = com_switch.connection.get_dict(dict_accounts)
    dict_priority.data = com_switch.connection.get_dict(dict_priority)
    dict_step_assembly.data = com_switch.connection.get_dict(dict_step_assembly)
    dict_step_type.data = com_switch.connection.get_dict(dict_step_type)
