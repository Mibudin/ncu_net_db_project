import argparse
from typing import Optional
import cmd
import colorama as clr

from jaddb.nhk_dictionary_db import NHKDictionaryEntry, Pitch
from jadcli.nhk_dictionary_cli import NHKDictionaryCLI
from jadapp.nhk_dictionary_app import NHKDictionaryApp


class JADCLI:
    def __init__(self, args: argparse.Namespace):
        self._args = args
        # self._nhk_dict_cli = NHKDictionaryCLI(self._args)
        self._app = NHKDictionaryApp()

    def dict(self, args: tuple[str]):  # TODO: lookup, verbose
        # self._nhk_dict_cli.dict(args)
        if len(args) == 0:
            print("No query string!")
            return

        es = self._app.lookup(args)
        if es:
            self._print_nhk_dict_entries(es)
        else:
            print("Word not found!")

    def _print_nhk_dict_entries(self, entries: list[NHKDictionaryEntry]):
        for i, e in enumerate(entries):
            print(f"[{i + 1}]:", e.nhk_expr, e.kana_expr, end=" ")
            self._print_nhk_dict_accent(e)
            print()

    def _print_nhk_dict_accent(self, entry: NHKDictionaryEntry):
        acc_str = []
        for i, (k, p) in enumerate(zip(entry.kana_std_expr, entry.accent_seq)):
            acc_str += k
            if self._args.color:
                acc_str += clr.Fore.RED
            if i == entry.nasal_pos - 1:
                acc_str += "゜"
            if i == entry.voiceless_pos - 1:
                acc_str += "Ｘ"
            if p == Pitch.ACCENT:
                acc_str += "＼"
            elif p == Pitch.HIGH and \
                    (i == entry.char_num - 1 or
                     (entry.char_num > i + 1 and entry.accent_seq[i + 1] == Pitch.LOW)):
                acc_str += "￣"
            if self._args.color:
                acc_str += clr.Style.RESET_ALL
        print("".join(acc_str), end="")

    def close(self):
        self._app.close()


class JADCmd(cmd.Cmd):
    intro = "JAD Application CLI Version."
    prompt = "[JAD]> "

    def __init__(self):
        super().__init__()
        self._args: Optional[argparse.Namespace] = None
        self._parse_args()
        self._colorize()

        self._cli = JADCLI(self._args)

    def _parse_args(self):
        parser = argparse.ArgumentParser(description="JAD Application CLI Version.")

        parser.add_argument("-v", "--verbose", action="store_true")
        parser.add_argument("-c", "--color", action="store_true")
        # TODO: CLI App arguments: --window

        self._args = parser.parse_args()

    def _colorize(self):
        if self._args.color:
            clr.init(convert=True)

    def emptyline(self) -> bool:
        return False  # Empty line does nothing

    def postcmd(self, stop: bool, line: str) -> bool:
        print()
        return stop

    @staticmethod
    def _split_args(arg: str) -> tuple[str]:
        return tuple(arg.split())

    def do_dict(self, arg):
        args = self._split_args(arg)
        self._cli.dict(args)

    def do_exit(self, arg):
        """Exit the application."""
        if self._args.color:
            print(clr.Style.BRIGHT + clr.Fore.GREEN + "Bye!" + clr.Style.RESET_ALL)
        else:
            print("Bye!")

        return True

    do_EOF = do_exit  # To support the EOF such as from Ctrl-D
    do_bye = do_exit
    do_q = do_exit

    def close(self):
        self._cli.close()


def _main():
    jad_cmd = JADCmd()
    jad_cmd.cmdloop()


if __name__ == "__main__":
    _main()
