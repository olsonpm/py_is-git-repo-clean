# ------- #
# Imports #
# ------- #

from is_git_repo_clean import version
from is_git_repo_clean.utils import iif
from is_git_repo_clean.cli import getIsGitRepoClean, usage
from tempfile import TemporaryDirectory, NamedTemporaryFile
import os
import subprocess


# ---- #
# Init #
# ---- #

x = "\x1b[31m✘\x1b[0m"
o = "\x1b[32m✔\x1b[0m"


def runSync(cmd):
    return subprocess.run(
        cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )


# ---- #
# Main #
# ---- #


def runTests():
    with TemporaryDirectory() as tmpdirname:
        result = getIsGitRepoClean(["--invalid"])
        expectedStderr = "invalid option '--invalid'" + os.linesep + usage
        icon = getIcon(result.stderr == expectedStderr and result.code == 2)
        print(f"  {icon} --invalid")

        result = getIsGitRepoClean(["--silent", "--help"])
        expectedStderr = (
            "'--help' must be the only argument when passed"
            + os.linesep
            + usage
        )
        icon = getIcon(result.stderr == expectedStderr and result.code == 2)
        print(f"  {icon} --silent --help")

        result = getIsGitRepoClean(["--dir"])
        expectedStderr = "'--dir' must be given a value" + os.linesep + usage
        icon = getIcon(result.stderr == expectedStderr and result.code == 2)
        print(f"  {icon} --dir")

        os.chdir(tmpdirname)

        result = getIsGitRepoClean(["--help"])
        icon = getIcon(result.stdout == usage and result.code == 0)
        print(f"  {icon} --help")

        result = getIsGitRepoClean(["--version"])
        icon = getIcon(result.stdout == version and result.code == 0)
        print(f"  {icon} --version")

        result = getIsGitRepoClean([])
        icon = getIcon(
            result.stderr == "dir is not a git repository" and result.code == 3
        )
        print(f"  {icon} not a git repo")

        runSync(["git", "init"])

        result = getIsGitRepoClean([])
        icon = getIcon(result.stdout == "yes" and result.code == 0)
        print(f"  {icon} is a clean git repo")

        result = getIsGitRepoClean(["--dir", tmpdirname])
        icon = getIcon(result.stdout == "yes" and result.code == 0)
        print(f"  {icon} is a clean git repo --dir <path>")

        with NamedTemporaryFile(dir=tmpdirname):
            result = getIsGitRepoClean([])
            icon = getIcon(result.stderr == "no" and result.code == 1)
            print(f"  {icon} not a clean git repo")

        result = getIsGitRepoClean(["--silent"])
        icon = getIcon(result.stdout is None and result.code == 0)
        print(f"  {icon} is a clean git repo --silent")


# ------- #
# Helpers #
# ------- #


def getIcon(condition):
    return iif(condition, o, x)
