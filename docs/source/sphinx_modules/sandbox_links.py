"""Sphinx extension to handle the signal directive in the method."""

__version__ = '2024.10'

from typing import get_overloads
from typing import TYPE_CHECKING, Any, ClassVar, NamedTuple, cast

from sphinx.util.inspect import signature, stringify_signature

from sphinx import addnodes
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.domains.python import PyMethod, PyObject

if True or TYPE_CHECKING:
    from collections.abc import Sequence

    from docutils.nodes import Node, system_message

    from sphinx.application import Sphinx
    from sphinx.extension import Extension
    from sphinx.util.typing import ExtensionMetadata, OptionSpec
    from sphinx.writers.html5 import HTML5Translator

def demo_link_role_int(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """
    Custom role to generate GitHub and TryItOnline links with optional prefix removal.
    """
    base_github_url = "https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/"

    # Split text into prefix and actual file path

    file_name = text.split(',')[-1].strip()
    file_path = '/'.join([s.strip() for s in text.split(',')])

    # Generate GitHub and TryItOnline links
    github_url = f"{base_github_url}{file_path.strip()}"

    # Format the output
    paragraph_node = nodes.inline()
    github_link = nodes.reference(rawtext, file_name    , refuri=github_url, **options)

    # Add links and combine
    paragraph_node += github_link

    return [paragraph_node], []

def demo_link_role_int_sb(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """
    Custom role to generate GitHub and TryItOnline links with optional prefix removal.
    """
    base_github_url = "https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/"
    base_tio_url = "https://ceccopierangiolieugenio.github.io/pyTermTk/sandbox/sandbox.html?filePath="

    # Split text into prefix and actual file path

    file_name = text.split(',')[-1].strip()
    file_path = '/'.join([s.strip() for s in text.split(',')])

    # Generate GitHub and TryItOnline links
    github_url = f"{base_github_url}{file_path.strip()}"
    tio_url = f"{base_tio_url}{file_path.strip()}"

    # Format the output
    paragraph_node = nodes.inline()
    github_link = nodes.reference(rawtext, file_name    , refuri=github_url, **options)
    tio_link    = nodes.reference(rawtext, "tryItOnline", refuri=tio_url   , **options)

    # Add links and combine
    paragraph_node += github_link
    paragraph_node += nodes.Text(" ")
    paragraph_node += nodes.Text("(")
    paragraph_node += tio_link
    paragraph_node += nodes.Text(")")

    return [paragraph_node], []

def demo_link_role_ext_sb(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """
    Custom role to generate GitHub and TryItOnline links with optional prefix removal.
    """
    base_tio_url = "https://ceccopierangiolieugenio.github.io/pyTermTk/sandbox/sandbox.html?fileUri="

    # Split text into prefix and actual file path

    file_name = text.split(',')[-1].strip()
    file_uri = '/'.join([s.strip() for s in text.split(',')])

    # Generate GitHub and TryItOnline links
    tio_url = f"{base_tio_url}{file_uri.strip()}"

    # Format the output
    paragraph_node = nodes.inline()
    github_link = nodes.reference(rawtext, file_name    , refuri=file_uri, **options)
    tio_link    = nodes.reference(rawtext, "tryItOnline", refuri=tio_url   , **options)

    # Add links and combine
    paragraph_node += github_link
    paragraph_node += nodes.Text(" ")
    paragraph_node += nodes.Text("(")
    paragraph_node += tio_link
    paragraph_node += nodes.Text(")")

    return [paragraph_node], []

# Register the custom role
def setup(app):
    app.add_role("ttk:ghIntLink", demo_link_role_int)
    app.add_role("ttk:sbIntLink", demo_link_role_int_sb)
    app.add_role("ttk:sbExtLink", demo_link_role_ext_sb)