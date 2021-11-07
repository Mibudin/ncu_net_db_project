from jaddb.nhk_dictionary_db import NHKDictionaryDB, NHKDictionaryEntry


class NHKDictionaryApp:
    _hiragana = "がぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽ" \
                "あいうえおかきくけこさしすせそたちつてと" \
                "なにぬねのはひふへほまみむめもやゆよらりるれろ" \
                "わをんぁぃぅぇぉゃゅょっ"
    _katakana = "ガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポ" \
                "アイウエオカキクケコサシスセソタチツテト" \
                "ナニヌネノハヒフヘホマミムメモヤユヨラリルレロ" \
                "ワヲンァィゥェォャュョッ"
    _kata_hira_table = dict(zip([ord(c) for c in _katakana], _hiragana))
    _hira_kata_table = dict(zip([ord(c) for c in _hiragana], _katakana))

    def __init__(self):
        self._db = NHKDictionaryDB()
        self._db.connect()

    def lookup(self, query: str, size: int) -> list[NHKDictionaryEntry]:
        nq = self._format_query(query)

        return self._db.lookup(nq, size)

    @classmethod
    def _format_query(cls, query: str) -> str:
        nq = query.strip().translate(cls._hira_kata_table)
        return nq

    def close(self):
        self._db.disconnect()
