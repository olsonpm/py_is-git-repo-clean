import setuptools
from is_git_repo_clean.meta import version

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="is_git_repo_clean",
    version=version,
    author="phil",
    author_email="philip.olson@pm.me",
    description="A simple function to test whether your git repo is clean",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/olsonpm/py_is-git-repo-clean",
    packages=setuptools.find_packages(),
    scripts=["bin/is-git-repo-clean"],
    include_package_data=True,
    python_requires=">=3.7",
    license="WTFNMFPL-1.0",
)
