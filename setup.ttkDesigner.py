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
    url="https://github.com/ceccopierangiolieugenio/pyTermTk/tree/main/apps/ttkDesigner",
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
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries :: Application Frameworks"],
    include_package_data=False,
    packages=['ttkDesigner','ttkDesigner.app', 'ttkDesigner.app.superobj'],
    package_data={'ttkDesigner': ['tui/*']},
    python_requires=">=3.9",
    install_requires=[
        'pyTermTk>="0.41.11-a.0"',
        'pyperclip',
        'Pillow'],
    entry_points={
        'console_scripts': [
            'ttkDesigner = ttkDesigner:main',
        ],
    },
)
