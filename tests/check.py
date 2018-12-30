# noqa: E501

from types import SimpleNamespace as obj
from tempfile import TemporaryDirectory, NamedTemporaryFile
from is_git_repo_clean import check, checkSync
from shutil import rmtree
from os import path
import asyncio
import subprocess


x = "\x1b[31m✘\x1b[0m"
o = "\x1b[32m✔\x1b[0m"


def runTests():
    return asyncio.run(_runTests())


async def _runTests():
    # sync tests
    with TemporaryDirectory() as tmpdirname:
        for step in makeSteps(tmpdirname):
            if not (await step()):
                return False

    return True


# ------- #
# Helpers #
# ------- #


def makeSteps(cwd):
    testIsClean = makeTestIsClean(cwd)
    runSync = makeRunSync(cwd)
    runGitInit = lambda: runSync(["git", "init"])
    runGitAddAll = lambda: runSync(["git", "add", "."])

    def runResetGitDir():
        rmtree(path.join(cwd, ".git"))
        runGitInit()

    async def beforeGitInit():
        isClean = makeIsClean(cwd)
        try:
            await isClean.nonsync()
            print(
                f"  {x} check({cwd}) did not raise an exception before git init"
            )
            return False
        except Exception as e:
            expected = "is not a git repository" in str(e)
            if not expected:
                print(
                    f"  {x} check({cwd}) raised an incorrect exception before"
                    " git init"
                )
                return False

        try:
            isClean.sync()
            print(
                f"  {x} checkSync({cwd}) did not raise an exception before"
                " git init"
            )
            return False
        except Exception as e:
            expected = "is not a git repository" in str(e)
            if not expected:
                print(
                    f"  {x} checkSync({cwd}) raised an incorrect exception"
                    " before git init"
                )
                return False

        print(f"  {o} before git init")
        return True

    async def gitInit():
        runGitInit()
        return await testIsClean(True, "a newly initialized repo")

    async def unstaged():
        with NamedTemporaryFile(dir=cwd):
            return await testIsClean(False, "unstaged changes")

    async def staged():
        with NamedTemporaryFile(dir=cwd):
            runGitAddAll()
            result = await testIsClean(False, "staged changes")

        runResetGitDir()
        return result

    async def committed():
        with NamedTemporaryFile(dir=cwd):
            runGitAddAll()
            runSync(["git", "commit", "-m", '"initial commit"'])
            result = await testIsClean(True, "committed changes")

        runResetGitDir()
        return result

    return [beforeGitInit, gitInit, unstaged, staged, committed]


def makeTestIsClean(cwd):
    isClean = makeIsClean(cwd)

    async def testIsClean(expected, context):
        method = "check"
        actual = await isClean.nonsync()
        if expected == actual:
            method = "checkSync"
            actual = isClean.sync()

        if expected != actual:
            print(f"  {x} {method}({cwd}) returned {actual} with {context}")
        else:
            print(f"  {o} {context}")

        return expected == actual

    return testIsClean


def makeIsClean(cwd):
    return obj(sync=lambda: checkSync(cwd), nonsync=lambda: check(cwd))


def makeRunSync(cwd):
    return lambda cmd: subprocess.run(
        cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=cwd
    )
