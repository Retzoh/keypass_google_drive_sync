from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
from pathlib import Path

PROJECT_NAME = "keypass-sync"
PACKAGE_NAME = PROJECT_NAME
PACKAGE_PATH = PROJECT_NAME.replace('-', '_')


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup_params = dict(
    name=PACKAGE_NAME,

    description=PACKAGE_NAME + " Project",
    long_description=long_description,

    url="https://git.sr.ht/~retzoh/gtd_project_management",

    author="retzoh",
    author_email="comptes.hb+sr_hat@gmail.com",

    license="None",

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
    ],

    keywords="",

    package_dir={"": "src"},
    packages=find_packages("src", include=[PACKAGE_PATH, PACKAGE_PATH + ".*"]),
    include_package_data=True,

    tests_require=[
        "pytest>=3.*",
        "pytest-cov",
    ],
    install_requires=[
        "pathlib",
        "setuptools",
        "google_services",
    ],
)


# Version spec management:
# * if a "VERSION" file exists, the version is read directly from it and set
#   using the "version" key.
# * otherwise, the version is extracted from the VCS using `setuptools_scm`,
#   which is added to the "setup_requires" dependencies, and the
#   "use_scm_version" key is set to True.
version_file = Path("VERSION")
if version_file.exists():
    setup_params.update(dict(
        version=version_file.read_text().strip()))
else:
    setup_requires = list(setup_params.get("setup_requires", []))
    setup_requires.append("setuptools_scm")
    setup_params.update(dict(
        setup_requires=setup_requires,
        use_scm_version=True))


setup(**setup_params)
