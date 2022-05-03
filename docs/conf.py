# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import scanspec

# -- General configuration ------------------------------------------------

# General information about the project.
project = "scanspec"

# The full version, including alpha/beta/rc tags.
release = scanspec.__version__

# The short X.Y version.
if "+" in release:
    # Not on a tag
    version = "master"
else:
    version = release

extensions = [
    # Use this for generating API docs
    "sphinx.ext.autodoc",
    # This can parse google style docstrings
    "sphinx.ext.napoleon",
    # For linking to external sphinx documentation
    "sphinx.ext.intersphinx",
    # Add links to source code in API docs
    "sphinx.ext.viewcode",
    # Adds the inheritance-diagram generation directive
    "sphinx.ext.inheritance_diagram",
    # Adds plotting directives
    "matplotlib.sphinxext.plot_directive",
    # Graphiql directive
    "sphinx_graphql.graphiql",
    # Makes autodoc understand apischema annotated classes/functions
    "sphinx_apischema",
    # Add example_spec directive
    "scanspec.sphinxext",
]

# If true, Sphinx will warn about all references where the target cannot
# be found.
nitpicky = True

# A list of (type, target) tuples (by default empty) that should be ignored when
# generating warnings in "nitpicky mode". Note that type should include the
# domain name if present. Example entries would be ('py:func', 'int') or
# ('envvar', 'LD_LIBRARY_PATH').
nitpick_ignore = [
    ("py:func", "int"),
    ("py:class", "Axis"),
    ("py:class", "AxesPoints"),
    ("py:class", "np.ndarray"),
]

# Both the class’ and the __init__ method’s docstring are concatenated and
# inserted into the main body of the autoclass directive
autoclass_content = "both"

# Order the members by the order they appear in the source code
autodoc_member_order = "bysource"

# Don't inherit docstrings from baseclasses
autodoc_inherit_docstrings = False

# Insert inheritance links
autodoc_default_options = {"show-inheritance": True}

# A dictionary for users defined type aliases that maps a type name to the
# full-qualified object name.
autodoc_type_aliases = dict(AxesPoints="scanspec.core.AxesPoints")

# Include source in plot directive by default
plot_include_source = True

# Output graphviz directive produced images in a scalable format
graphviz_output_format = "svg"

# The name of a reST role (builtin or Sphinx extension) to use as the default
# role, that is, for text marked up `like this`
default_role = "any"

# The suffix of source filenames.
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# These patterns also affect html_static_path and html_extra_path
exclude_patterns = ["_build"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# This means you can link things like `str` and `asyncio` to the relevant
# docs in the python documentation.
intersphinx_mapping = dict(
    python=("https://docs.python.org/3/", None),
    numpy=("https://numpy.org/doc/stable/", None),
)

# Common links that should be available on every page
rst_epilog = """
.. _Diamond Light Source:
    http://www.diamond.ac.uk
"""

# Ignore localhost links for period check that links in docs are valid
linkcheck_ignore = [r"http://localhost:\d+/"]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme_github_versions"

# Options for the sphinx rtd theme, use DLS blue
html_theme_options = dict(style_nav_header_background="rgb(7, 43, 93)")

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
html_show_sphinx = False

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
html_show_copyright = False

# Add some CSS classes for columns and other tweaks in a custom css file
html_css_files = ["theme_overrides.css"]

# Logo
html_logo = "images/scanspec-logo.svg"
html_favicon = "images/scanspec-logo.ico"
