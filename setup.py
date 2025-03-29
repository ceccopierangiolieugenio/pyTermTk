import setuptools, os
from TermTk import version

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

_name="pyTermTk"
_version=version

print(f"Name: {_name}")
print(f"Version: {_version}")

setuptools.setup(
    name=_name,
    version=_version,
    author='Eugenio Parodi',
    author_email='ceccopierangiolieugenio@googlemail.com',
    description='Python Terminal Toolkit',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ceccopierangiolieugenio/pyTermTk",
    classifiers=[
        # https://pypi.org/classifiers/
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Terminals",
        "Topic :: Text Editors :: Text Processing",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries :: Application Frameworks"],
    # packages=setuptools.find_packages(),
    packages = setuptools.find_packages(where="."),
    package_dir = {"":"."},
    python_requires=">=3.9",
)
