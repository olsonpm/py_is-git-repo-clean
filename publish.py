# ------- #
# Imports #
# ------- #

from glob import glob
from os import path
from textwrap import dedent
from zipfile import ZipFile
import is_git_repo_clean
import subprocess
import sys
import toml


# ---- #
# Init #
# ---- #


def printErr(msg):
    print(msg, file=sys.stderr)


# ---- #
# Main #
# ---- #

if not is_git_repo_clean.checkSync():
    printErr(
        dedent(
            """
            the git repo is not clean
            aborting publish\
            """
        )
    )
    exit(1)

with open("pyproject.toml", "r") as f:
    pyproject = toml.load(f)

    poetryConfig = pyproject["tool"]["poetry"]
    githubUrl = poetryConfig["repository"]
    moduleName = poetryConfig["name"]
    version = poetryConfig["version"]

pypiWarning = dedent(
    f"""\
    *Note: This document is best viewed [on github]({githubUrl}).
    Pypi's headers are all caps which presents inaccurate information*
    """
)
pypiWarnComment = "<!-- pypiwarn -->"

with open("./README.md", "r") as f:
    commentedWarn = f.read()

with open("./README.md", "w") as f:
    f.write(commentedWarn.replace(pypiWarnComment, pypiWarning, 1))

subprocess.run("poetry build".split(" "))

pathToTopLevel = f"{moduleName}/top_level.txt"
if not path.isfile(pathToTopLevel):
    raise Exception(f"top_level.txt must exist at '{pathToTopLevel}'")

topLevelDistInfo = f"{moduleName}-{version}.dist-info/top_level.txt"
pathToWheelZip = glob(f"dist/{moduleName}-{version}-*.whl")[0]
with ZipFile(pathToWheelZip, "a") as wheelZip:
    wheelZip.write(pathToTopLevel, topLevelDistInfo)

with open("README.md", "w") as f:
    f.write(commentedWarn)

subprocess.run(["poetry", "publish"])

print("donezo!")
