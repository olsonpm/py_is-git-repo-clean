import sys
from .cli import getIsGitRepoClean


def printErr(msg):
    print(msg, file=sys.stderr)


result = getIsGitRepoClean(sys.argv[1:])

if result.stdout:
    print(result.stdout)

if result.stderr:
    print(result.stderr)

exit(result.code)
