# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'bench'
copyright = '2023, Arthur'
author = 'Arthur'

import os
import sys

sys.path.insert(0, os.path.abspath('../..'))


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.autosummary', 'myst_parser']

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'furo'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# colors
PURPLE = "#b536fb"
FIG = "#473351"
EGGPLANT = "#1a0016"
ASH = "#e4e0e4"
MINT = "#c7fdd1"
WHITE = "#ffffff"
BLUE = "#329ad7"
ORANGE = "#ff7c00"

# fonts
FONT_STACK = "Graphik, sans-serif"
FONT_STACK_MONOSPACE = "IBM Plex Mono, monospace"

# share sidebar configuration between light and dark
sidebar_theme_variables = {
        "color-sidebar-background": FIG,
        "color-sidebar-link-text": WHITE,
        "color-sidebar-link-text--top-level": MINT,
        "color-sidebar-item-background--hover": WHITE,
        "color-sidebar-text--hover": EGGPLANT,
        # search
        "color-sidebar-search-text": WHITE,
        "color-sidebar-search-border": ASH,
        "color-sidebar-search-foreground": EGGPLANT,
        "color-sidebar-search-foreground--inactive": ASH,
        "color-sidebar-search-background--focus": WHITE
}

# The light_logo and dark_logo properties take a file path relative to the _static folder
html_theme_options = {
    "light_logo": "img/dark-mode-logo.svg",
    "dark_logo": "img/dark-mode-logo.svg",
    "light_css_variables": {
        # define main base colors
        "color-foreground-primary": EGGPLANT,
        "color-foreground-secondary": FIG,
        "color-background-primary": WHITE,
        "color-background-secondary": FIG,
        "color-brand-primary": PURPLE,
        "color-api-background": ASH,

        "color-background-border": ASH,
        "color-inline-code-background": ASH,

        "color-icon": FIG,

        # table of contents (right)
        "color-toc-item-text": EGGPLANT,
        "color-toc-item-text--active": FIG,

        # body
        "color-highlight-on-target": MINT,
        "color-brand-content": BLUE,

        # sidebar
        **sidebar_theme_variables,

        # FONTS
        "font-stack": FONT_STACK,
        "font-stack--monospace": FONT_STACK_MONOSPACE,

        # TABLE
        "color-table-header-background": WHITE
    },
    "dark_css_variables": {
        # define main base colors
        "color-foreground-primary": WHITE,
        "color-foreground-secondary": ASH,
        "color-background-primary": EGGPLANT,
        "color-background-secondary": FIG,
        "color-brand-primary": PURPLE,
        "color-api-background": FIG,

        "color-background-border": FIG,
        "color-inline-code-background": FIG,

        "color-icon": ASH,

        # table of contents (right)
        "color-toc-item-text": WHITE,
        "color-toc-item-text--active": ASH,

        # body
        "color-highlight-on-target": FIG,
        "color-brand-content": BLUE,

        # sidebar
        **sidebar_theme_variables,

        "font-stack": FONT_STACK,
        "font-stack--monospace": FONT_STACK_MONOSPACE,

        # TABLE
        "color-table-header-background": FIG
    },
    "sidebar_hide_name": True,

}

# Custom CSS file in case we want to add more styling
html_css_files = [
    'custom_styles_20221207.css'
]
