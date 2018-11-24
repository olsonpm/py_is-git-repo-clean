import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="is_git_repo_clean",
    version="0.1.6",
    author="phil",
    author_email="philip.olson@pm.me",
    description="A simple function to test whether your git repo is clean",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/olsonpm/py_is-git-repo-clean",
    packages=setuptools.find_packages(),
    scripts=["bin/is-git-repo-clean"],
    license="WTFNMFPL-1.0",
)
