from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

version = "__VERSION__"
name = "__NAME__"

print(f"Version: {version}")
print(f"Name: {name}")

setup(
    name=name,
    version=version,
    author='Eugenio Parodi',
    author_email='ceccopierangiolieugenio@googlemail.com',
    description='ttkDesigner is a terminal user interface designer for pyTermTk applications',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ceccopierangiolieugenio/pyTermTk",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Terminals",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Terminals",
        "Topic :: Text Editors :: Text Processing",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries :: Application Frameworks"],
    include_package_data=False,
    packages=['dumbPaintTool','dumbPaintTool.app'],
    package_data={'dumbPaintTool': ['tui/*']},
    python_requires=">=3.9",
    install_requires=[
        'pyTermTk>=0.39.0a116',
        'pyperclip',
        'Pillow'],
    entry_points={
        'console_scripts': [
            'dumbPaintTool = dumbPaintTool:main',
        ],
    },
)

# https://pypi.org/classifiers/
#
# INTENDED AUDIENCE :: EDUCATION
# INTENDED AUDIENCE :: END USERS/DESKTOP
#
# TOPIC :: ARTISTIC SOFTWARE
# TOPIC :: INTERNET
# TOPIC :: MULTIMEDIA :: GRAPHICS
# TOPIC :: MULTIMEDIA :: GRAPHICS :: EDITORS
# TOPIC :: MULTIMEDIA :: GRAPHICS :: EDITORS :: RASTER-BASED
# TOPIC :: SOFTWARE DEVELOPMENT :: LIBRARIES
# TOPIC :: SOFTWARE DEVELOPMENT :: LIBRARIES :: APPLICATION FRAMEWORKS
# TOPIC :: SOFTWARE DEVELOPMENT :: LIBRARIES :: PYTHON MODULES
# TOPIC :: SOFTWARE DEVELOPMENT :: USER INTERFACES
# TOPIC :: TERMINALS
# TOPIC :: TERMINALS :: SERIAL
# TOPIC :: TERMINALS :: TELNET
# TOPIC :: TERMINALS :: TERMINAL EMULATORS/X TERMINALS
# TOPIC :: TEXT EDITORS :: INTEGRATED DEVELOPMENT ENVIRONMENTS (IDE)
# TOPIC :: TEXT EDITORS :: TEXT PROCESSING
# TOPIC :: TEXT EDITORS :: WORD PROCESSORS