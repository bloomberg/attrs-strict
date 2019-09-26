import os
import sys

from attrs_strict import __version__

sys.path.insert(0, os.path.abspath("../.."))

project = ""
copyright = "2019, Bloomberg"
author = "Erik-Cristian Seulean"

release = "2019"

extensions = [
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
]

templates_path = ["_templates"]
language = "python"

exclude_patterns = []

html_theme = "alabaster"
html_static_path = []

master_doc = "index"

version = u".".join(__version__.split(".")[:2])
release = __version__
