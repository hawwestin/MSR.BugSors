from tkinter import filedialog
from data_config import ds
from data_config import atDict
from data_config import ad
from network import con

statusmsg = None
statusbar = None


"""
Zmienna do przechowywania galeri tabulatorów.
Tabulator jest obiektm classy : XYZ
"""
gallery = {}

LARGE_FONT= ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)


def add_img(tab, obj):
    """

    :param tab:  value of tkController.notebook.select() for that new tab. its frame._w
    :param img:  Vision(frame, controller, path)
    :return:
    """
    global gallery
    gallery[tab] = obj

def close_img(img):
    """

    :param img: img index in gallery , Key to pop
    :return:
    """
    global gallery
    gallery.pop(img)
    # item = sorted(self.gallery)[-1] + 1
    # print("\nitem after close : %d"% item)


def get_path():
    # todo potrzeba blokowac i sprawdzac czy wybrany plik jest obrazkiem o dozwolonym typie
    # todo path do obrazka powinien byc storowany by moc go zapisac
    return filedialog.askopenfilename()


def populate_constants():
    ds.dict_state = con.get_dict_states()
    atDict.atDict = con.get_dict_acc_type()
    ad.adict = con.get_users()
