import argparse

_parser = argparse.ArgumentParser()
_parser.add_argument("-d",
                    "--develop",
                    help="run in develop mode",
                    action="store_true")
CLI = _parser.parse_args()
