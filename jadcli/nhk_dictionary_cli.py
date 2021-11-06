import colorama as clr
import argparse


class NHKDictionaryEntryCLI:
    def __init__(self, args: argparse.Namespace):
        self._args = args


class NHKDictionaryCLI:
    def __init__(self, args: argparse.Namespace):
        self._args = args
        self._entry_cli = NHKDictionaryEntryCLI(self._args)

    def dict(self, args: tuple[str]):

        pass  # TODO
