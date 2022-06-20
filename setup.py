from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"),
          encoding = "utf-8") as f:
    long_description = f.read()

setup(
    name = "biohub",
    version = "0.1.0",
    description = "Bioinformatic API",
    long_description = long_description,
    url = "",
    author = "Juan Antonio Marín Sanz",
    author_email = "b32masaj@gmail.com",
    license = "MIT",
    classifiers = [
        "Development Status :: 1 - Alpha",
        "Intended Audience :: Bioinformaticians",
        "Topic :: Bioinformatics",
        "License :: MIT",
        "Programming Language :: Python :: 3",
    ],
    keywords = "biohub bioinformatics api",
    packages = find_packages(),
    package_dir = {"biohub":"biohub"}
)