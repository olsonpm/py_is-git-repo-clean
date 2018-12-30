import os
from . import check, cli


def runTests():
    print("check")
    check.runTests()

    print(f"{os.linesep}cli")
    cli.runTests()
