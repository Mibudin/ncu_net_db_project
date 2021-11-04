import csv
import sqlite3
import pandas as pd

from definitions import *


def _rearrange_csv():
    #  1. NID
    #  2. ID
    #  3. WAVname
    #  4. K_FLD
    #  5. ACT
    #  6. katakana_reading
    #  7. nhk
    #  8. kanjiexpr
    #  9. NHKexpr
    # 10. numberchars
    # 11. devoiced_pos
    # 12. nasalsoundpos
    # 13. majiri
    # 14. kaisi
    # 15. KWAV
    # 16. katakana_reading_alt
    # 17. akusentosuu
    # 18. bunshou
    # 19. accent
    # ->
    #  1. [ 0] nid
    #  2. [ 1] aid
    #  3. [ 4] kana_index_seq
    #  4. [ 5] kana_expr
    #  5. [15] kana_std_expr
    #  6. [ 6] nhk_expr
    #  7. [ 7] kanji_expr
    #  8. [ 8] nhk_noted_expr
    #  9. [ 9] char_num
    # 10. [16] accent_num
    # 11. [18] accent_seq
    # 12. [10] voiceless_pos
    # 13. [11] nasal_pos
    # 14. [17] phrase_status
    # 15. [12] phrase
    # 16. [13] phrase_pos
    df = pd.read_csv(NHK_DATA_PATH, header=None, encoding="utf8")
    df = df[[0, 1, 4, 5, 15, 6, 7, 8, 9, 16, 18, 10, 11, 17, 12, 13]]
    df.fillna({10: -1, 11: -1}, inplace=True, downcast="infer")  # Avoid Pandas treating NaN as float
    df.to_csv(NHK_DATA_REV_PATH, header=None, encoding="utf8",
              index=False, line_terminator="\n")


def _csv_to_sqlite():
    conn = sqlite3.connect(NHK_DATA_SQLITE_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM Accents;")

    with open(NHK_DATA_REV_PATH, encoding="utf8") as csv_file:
        rows = csv.reader(csv_file)
        cur.executemany("INSERT INTO Accents "
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", rows)

    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    _rearrange_csv()
    _csv_to_sqlite()
    pass
