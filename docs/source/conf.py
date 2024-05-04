# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))


# -- Project information -----------------------------------------------------

project = 'pyscan'
copyright = '2023, Andrew Mounce'
author = 'Andrew Mounce'

# The full version, including alpha/beta/rc tags
release = '0.0.1'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'numpydoc',
    'nbsphinx',
    'nbsphinx_link',
    'myst_parser']
# myst_parser allows you to use .md and .rst files for pages


# numpydoc options
numpydoc_show_inherited_class_members = False
numpydoc_class_members_toctree = False

# autodoc options
autodoc_typehints = "none"
autodoc_docstring_signature = True
autodoc_default_options = {'members': None}

# myst_parser options
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'pydata_sphinx_theme'
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_theme_options = {
    "logo": {  # "link": "https://matplotlib.org/stable/",
        "image_light": "_static/pyscan logo v3.svg",
        "image_dark": "_static/pyscan logo v3.svg"},
    # collapse_navigation in pydata-sphinx-theme is slow, so skipped for local
    # and CI builds https://github.com/pydata/pydata-sphinx-theme/pull/386
    # "collapse_navigation": not is_release_build,
    "show_prev_next": True,
    "navbar_align": "left",
    # social media links
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/sandialabs/pyscan",
            "icon": "fab fa-github-square",
        }
    ],
    "primary_sidebar_end": [],
    "use_edit_page_button": True,
}

html_context = {
    # these seemed to be necessary in order to create proper links to "edit on github"
    # may reconsider at a later time to see if it's really necessary to add a user
    "doc_path": "docs/source/",
    "github_user": "plesiopterys",
    "github_repo": "https://github.com/sandialabs/pyscan",
    "github_version": "main",
}

html_sidebars = {
    # default is
    # "**": ["sidebar-nav-bs", "sidebar-ethical-ads"],
    "**": ["sidebar-nav-bs"]
}
