from jadcli.nhk_dictionary_cli import JADCmd


def _main():
    jad_cmd = JADCmd()
    jad_cmd.cmdloop()
    jad_cmd.close()


if __name__ == "__main__":
    _main()
