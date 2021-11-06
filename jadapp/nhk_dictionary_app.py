from jaddb.nhk_dictionary_db import NHKDictionaryDB, NHKDictionaryEntry


class NHKDictionaryApp:
    def __init__(self):
        self._db = NHKDictionaryDB()
        self._db.connect()

    def lookup(self, args: tuple[str]) -> list[NHKDictionaryEntry]:
        return self._db.lookup(args[0])

    def close(self):
        self._db.disconnect()
