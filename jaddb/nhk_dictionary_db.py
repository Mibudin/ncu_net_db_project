from dataclasses import dataclass
from enum import Enum
import sqlite3
from typing import Optional
from contextlib import closing

from definitions import *


class Pitch(Enum):
    LOW = 0
    HIGH = 1
    ACCENT = 2


@dataclass(frozen=True)
class NHKDictionaryEntry:
    nid: int
    aid: int
    kana_index_seq: tuple[int, int, int, int]
    kana_expr: str
    kana_std_expr: str
    nhk_expr: str
    kanji_expr: str
    nhk_noted_expr: str
    char_num: int
    accent_num: int
    accent_seq: list[Pitch]
    voiceless_pos: int  # TODO: Sequence split by 0
    nasal_pos: int  # TODO: Sequence split by 0
    phrase_status: bool
    phrase: str
    phrase_pos: int

    @classmethod
    def make_from_tuple(cls, db_tuple: tuple) -> "NHKDictionaryEntry":
        return cls(
            nid=db_tuple[0],
            aid=db_tuple[1],
            kana_index_seq=(int(db_tuple[2][-10]) if len(db_tuple[2]) > 9 else 0,
                            int(db_tuple[2][-9:-8]),
                            int(db_tuple[2][-8:-4]),
                            int(db_tuple[2][-4:])),
            kana_expr=db_tuple[3],
            kana_std_expr=db_tuple[4],
            nhk_expr=db_tuple[5],
            kanji_expr=db_tuple[6],
            nhk_noted_expr=db_tuple[7],
            char_num=db_tuple[8],
            accent_num=db_tuple[9],
            accent_seq=[Pitch(int(i))
                        for i in ("0" * (db_tuple[8] - len(db_tuple[10])) + db_tuple[10])],
            voiceless_pos=db_tuple[11],
            nasal_pos=db_tuple[12],
            phrase_status=(db_tuple[13] == 1),
            phrase=db_tuple[14],
            phrase_pos=db_tuple[15]
        )


@dataclass(frozen=True)
class NHKDictionaryCompoundEntry:
    # TODO: Duplicated equivalent entries
    pass


class NHKDictionaryDB:
    def __init__(self):
        self._conn: Optional[sqlite3.Connection] = None

    def connect(self):
        self._conn = sqlite3.connect(NHK_DATA_SQLITE_PATH)

    def disconnect(self):
        self._conn.close()
        self._conn = None

    def lookup(self, query: str, size: int = NHK_DATA_LOOKUP_SIZE) -> list[NHKDictionaryEntry]:
        # TODO: Duplicated equivalent entries
        #   https://stackoverflow.com/questions/23495734/sql-to-remove-rows-with-duplicated-value-while-keeping-one
        with closing(self._conn.cursor()) as cur:  # type: sqlite3.Cursor
            cur.execute("""
                SELECT *
                FROM Accents
                WHERE kana_expr LIKE ?;
                """, (query + "%",)
            )
            entries = cur.fetchmany(size if size > 0 else NHK_DATA_LOOKUP_SIZE)

        return [NHKDictionaryEntry.make_from_tuple(e) for e in entries]
