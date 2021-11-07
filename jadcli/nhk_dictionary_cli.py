import argparse
from typing import Optional
import cmd
import colorama as clr

from definitions import *

from jaddb.nhk_dictionary_db import NHKDictionaryEntry, Pitch
from jadapp.nhk_dictionary_app import NHKDictionaryApp


class InnerArgParser(argparse.ArgumentParser):
    def error(self, message: str):
        # Handle the real exit_on_error=False
        raise argparse.ArgumentError(None, message)

    def exit(self, status=0, message=None):
        # Handle the real exit_on_error=False
        raise argparse.ArgumentError(None, message)

    def print_error(self):
        import sys as _sys
        from gettext import gettext as _gettext

        message = str(_sys.exc_info()[1])
        self.print_usage(_sys.stderr)
        args = {'prog': self.prog, 'message': message}
        print(_gettext('%(prog)s: error: %(message)s') % args)

    def try_parse_args(self, args: tuple[str, ...]):
        try:
            return self.parse_args(args)
        except argparse.ArgumentError as e:
            if e.message is not None:
                self.print_error()
            return None


class JADCLI:
    def __init__(self, args: argparse.Namespace):
        self._args = args
        self._verbose = self._args.verbose
        self._color = self._args.color
        self._app = NHKDictionaryApp()

    def dict(self, args: tuple[str, ...]):
        dict_args = self._parse_dict_args(args)
        if dict_args is None:
            return

        es = self._app.lookup(dict_args.query, dict_args.number)
        if es:
            self._print_nhk_dict_entries(es)
        else:
            print("No Word found!")

    def _parse_dict_args(self, args: tuple[str, ...]) -> Optional[argparse.Namespace]:
        parser = InnerArgParser(prog="dict", description="Look up in the dictionary.", exit_on_error=False)
        parser.add_argument("query", type=str,
                            help="the query to be looked up")
        parser.add_argument("-n", "--number", type=int, default=NHK_DATA_LOOKUP_SIZE,
                            help="the maximal number of result entries to be looked up")
        return parser.try_parse_args(args)

    def _print_nhk_dict_entries(self, entries: list[NHKDictionaryEntry]):
        if self._color:
            print(f"Query result: {clr.Fore.CYAN}{len(entries)}{clr.Style.RESET_ALL} entry(ies).")
        else:
            print(f"Query result: {len(entries)} entry(ies).")
        for i, e in enumerate(entries):
            if self._verbose:
                if self._color:
                    print(f"[{clr.Fore.CYAN}{i + 1}{clr.Style.RESET_ALL}]:")
                    print(f"  Qry:  {clr.Fore.GREEN}{e.kana_expr}{clr.Style.RESET_ALL}")
                    print(f"  Expr: {clr.Style.BRIGHT}{clr.Fore.YELLOW}{e.nhk_expr}{clr.Style.RESET_ALL}"
                          f"｜{clr.Fore.YELLOW}{e.kanji_expr}{clr.Style.RESET_ALL}")
                    print(f"  Acc:  ", end="")
                    self._print_nhk_dict_accent(e)
                    print()
                    if e.phrase_status:
                        print(f"  Exmp: ", end="")
                        self._print_nhk_dict_phrase(e)
                        print()
                else:
                    print(f"[{i + 1}]:")
                    print(f"  Qry:  {e.kana_expr}")
                    print(f"  Expr: {e.nhk_expr}｜{e.kanji_expr}")
                    print(f"  Acc:  ", end="")
                    self._print_nhk_dict_accent(e)
                    print()
                    if e.phrase_status:
                        print(f"  Exmp: ", end="")
                        self._print_nhk_dict_phrase(e)
                        print()
            else:
                if self._color:
                    print(f"[{clr.Fore.CYAN}{i + 1}{clr.Style.RESET_ALL}]: "
                          f"{clr.Fore.YELLOW}{e.kana_expr}{clr.Style.RESET_ALL}｜"
                          f"{clr.Style.BRIGHT}{clr.Fore.YELLOW}{e.nhk_expr}{clr.Style.RESET_ALL}｜",
                          end="")
                    self._print_nhk_dict_accent(e)
                    print()
                else:
                    print(f"[{i + 1}]: {e.kana_expr}｜{e.nhk_expr}｜", end="")
                    self._print_nhk_dict_accent(e)
                    print()

    def _print_nhk_dict_accent(self, entry: NHKDictionaryEntry):
        acc_str = []
        for i, (k, p) in enumerate(zip(entry.kana_std_expr, entry.accent_seq)):
            acc_str += k
            if self._color:
                acc_str += clr.Style.BRIGHT + clr.Fore.RED
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
            if self._color:
                acc_str += clr.Style.RESET_ALL
        print("".join(acc_str), end="")

    def _print_nhk_dict_phrase(self, entry: NHKDictionaryEntry):
        phr_str = []
        phr_str += entry.phrase[:entry.phrase_pos]
        phr_str += clr.Style.BRIGHT + clr.Fore.BLUE if self._color else ""
        phr_str += entry.phrase[entry.phrase_pos:(entry.phrase_pos + entry.char_num)]
        phr_str += clr.Style.RESET_ALL if self._color else ""
        phr_str += entry.phrase[(entry.phrase_pos + entry.char_num):]
        print("".join(phr_str), end="")

    def opt(self, args: tuple[str, ...]):
        opt_args = self._parse_opt_args(args)
        if opt_args is None:
            return

        if opt_args.action == "set":
            if opt_args.verbose:
                self._verbose = True
            if opt_args.color:
                self._color = True
        elif opt_args.action == "unset":
            if opt_args.verbose:
                self._verbose = False
            if opt_args.color:
                self._color = False

        if self._color:
            print(f"verbose: {clr.Fore.GREEN if self._verbose else clr.Fore.RED}"
                  f"{self._verbose}{clr.Style.RESET_ALL}")
            print(f"color: {clr.Fore.GREEN if self._color else clr.Fore.RED}"
                  f"{self._color}{clr.Style.RESET_ALL}")
        else:
            print(f"verbose: {self._verbose}")
            print(f"color: {self._color}")
        # for k, v in vars(self._args).items():
        #     if self._color:
        #         print(f"{k}: {clr.Fore.GREEN if v else clr.Fore.RED}{v}{clr.Style.RESET_ALL}")
        #     else:
        #         print(f"{k}: {v}")

    def _parse_opt_args(self, args: tuple[str, ...]) -> Optional[argparse.Namespace]:
        parser = InnerArgParser(prog="set", description="Set and list the options.", exit_on_error=False)
        parser.add_argument("action", type=str, nargs="?", choices=["list", "set", "unset"], default="list",
                            help="the action to do")
        parser.add_argument("-v", "--verbose", action="store_true",
                            help="target the \"verbose\" argument to be set or unset")
        parser.add_argument("-c", "--color", action="store_true",
                            help="target the \"color\" argument to be set or unset")
        return parser.try_parse_args(args)

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

        parser.add_argument("-v", "--verbose", action="store_true",
                            help="use the verbose mode to show more information")
        parser.add_argument("-c", "--color", action="store_true",
                            help="use the colorized mode")

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
    def _split_args(arg: str) -> tuple[str, ...]:
        return tuple(arg.split())

    def do_opt(self, arg):
        """Set and list the options."""
        args = self._split_args(arg)
        self._cli.opt(args)

    def do_dict(self, arg):
        """Look up in the dictionary."""
        args = self._split_args(arg)
        self._cli.dict(args)

    def do_exit(self, arg):
        """Exit the application."""
        # if self._args.color:
        #     print(clr.Fore.GREEN + "Bye!" + clr.Style.RESET_ALL)
        # else:
        #     print("Bye!")
        print("Bye!")

        return True

    do_EOF = do_exit  # To support the EOF such as from Ctrl-D
    do_bye = do_exit
    do_q = do_exit

    def close(self):
        self._cli.close()
