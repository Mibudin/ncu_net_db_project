from definitions import *
from jaddb.nhk_dictionary_db import *


def _test_make_entry():
    nhk_dic = NHKDictionaryDB()
    nhk_dic.connect()
    es = nhk_dic._cur.execute("SELECT * FROM Accents").fetchall()
    nhk_dic.disconnect()
    print(es[44])
    print(type(es[44][11]))
    print(*es[44][:2])
    e = NHKDictionaryEntry.make_from_tuple(es[44])
    print(e)


def _test_lookup():
    nhk_dic = NHKDictionaryDB()
    nhk_dic.connect()
    es = nhk_dic.lookup("イキ")
    # es = nhk_dic.lookup("")
    # es = nhk_dic.lookup("; SELECT True; --")
    nhk_dic.disconnect()
    # print(es)
    for e in es:
        print(e)


def _test_accent():
    nhk_dic = NHKDictionaryDB()
    nhk_dic.connect()
    es = nhk_dic._conn.execute("SELECT * FROM Accents WHERE accent_seq LIKE '%2%2%'").fetchall()
    nhk_dic.disconnect()
    for e in es:
        print(e)


if __name__ == "__main__":
    # _test_make_entry()
    _test_lookup()
    # _test_accent()
