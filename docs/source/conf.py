# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
sys.path.insert(0, os.path.abspath('../../libs/pyTermTk'))
sys.path.insert(0, os.path.abspath('sphinx_modules'))

import TermTk as ttk

# -- Project information -----------------------------------------------------

project = 'pyTermTk'
copyright = '2021, Eugenio Parodi'
author = 'Eugenio Parodi'

# The full version, including alpha/beta/rc tags
release = ttk.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.viewcode',
    # 'sphinx.ext.linkcode', # Create a link to the source through linkcode_resolve
    'sphinx.ext.githubpages',
    #'sphinx.ext.intersphinx',
    #'sphinx.ext.ifconfig',
    #'sphinx.ext.autosectionlabel',
	#'sphinx_epytext',
    'sphinx.ext.autodoc',  # Core library for html generation from docstrings
    #'sphinx.ext.autosummary',  # Create neat summary tables

    # Personal extensions/hacks to overcome the
    # FUCKNG unwritten idiotic sphinx rules
    # Fuck you Sphinx!!!
    'sphinx_ext_autosummary_reworked',  # Create neat summary tables
    'sphinx_PyRefRole_hacked',          # Resolve Domainless TermTk Classes
    'method_signal',
    'sandbox_links',
]

templates_path = ['templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'alabaster'
# html_static_path = ['_static']

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['static']

html_css_files = [
    # Workaround for RTD 0.4.3 bug https://github.com/readthedocs/sphinx_rtd_theme/issues/117
    'theme_overrides.css',  # override wide tables in RTD theme
    'ttk.css'
]

html_favicon = "https://ceccopierangiolieugenio.github.io/pyTermTk-Docs/sandbox/www/favicon.ico"
# html_favicon = "_images/favicon.ico"
# html_favicon = "../images/favicon.ico"

# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-toc_object_entries_show_parents
# Use 'hide' to only show the name of the element without any parents (i.e. method()).
toc_object_entries_show_parents='hide'

# read-the-docs theme looks better than the default "classic" one but has bugs e.g. no table wrapping
# html_theme = 'sphinx_rtd_theme'
# html_theme_options = {
#     'display_version': True,
#     #'prev_next_buttons_location': 'bottom',
#     #'style_external_links': False,
#     #'vcs_pageview_mode': '',
#     #'style_nav_header_background': 'white',
#     # Toc options
#     'collapse_navigation': True,
#     'sticky_navigation': True,
#     #'navigation_depth': 4,
#     'includehidden': True,
#     #'titles_only': False
#     'flyout_display': 'attached',
# }

# html_theme = 'bizstyle'
# html_theme_options = {
#     "sidebar_width": '240px',
#     "stickysidebar": True,
#     "stickysidebarscrollable": True,
#     "contribute": True,
#     "github_fork": "useblocks/groundwork",
#     "github_user": "useblocks",
# }

# Nice theme but it does not allows full-width
# html_theme = 'furo'
# html_theme_options = {}

# html_theme = 'press'
# html_theme_options = {}

# html_theme = 'piccolo_theme'
# html_theme_options = {}

# extensions.append("sphinx_wagtail_theme")
# html_theme = 'sphinx_wagtail_theme'

# html_theme = 'sphinx_material'

# html_permalinks_icon = '<span>#</span>'
# html_theme = 'sphinxawesome_theme'

html_theme = 'sphinx_book_theme'
html_permalinks_icon = '<span>🌶️</span>'
# html_permalinks_icon = '<span><image src="/_images/favicon.png"></span>'
# html_permalinks_icon = '<span><image src="https://ceccopierangiolieugenio.github.io/pyTermTk-Docs/sandbox/www/favicon.ico"></span>'
html_theme_options = {
    "home_page_in_toc": True,
    "use_fullscreen_button": True,
    # "toc_title": "{your-title}",
    "show_toc_level": 3,
    "repository_url": "https://github.com/ceccopierangiolieugenio/pyTermTk",
}

add_module_names = False
autosummary_generate = True
autosummary_generate_overwrite = True
autosummary_imported_members = False

# autodoc_default_options = { 'inherited-members':True }
autodoc_default_options = {
    'exclude-members': ('as_integer_ratio , bit_count , bit_length , '
                        'conjugate , denominator , from_bytes , imag , '
                        'numerator , real , to_bytes')
}

# Mock pyodide to avoid autogen failure
class pyodideProxy(): pass
sys.modules['pyodideProxy'] = pyodideProxy

class pyodide(): __version__ = "NA"
sys.modules['pyodide'] = pyodide

class windll(): pass
sys.modules['ctypes.windll'] = windll


def linkcode_resolve(domain, info):
    if domain != 'py':
        return None
    if not info['module']:
        return None
    filename = info['module'].replace('.', '/')
    # print(f"{domain=} {info=}")
    # print(f"https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/{filename}.py")
    return f"https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/{filename}.py"