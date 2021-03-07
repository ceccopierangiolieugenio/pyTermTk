import setuptools, os, subprocess

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Retrieve the version
out = subprocess.Popen(
        ['git','describe'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
version, stderr = out.communicate()
version = version.decode("utf-8").strip()

print(f"Version: {version}")

setuptools.setup(
    name='pyTermTk',
    # name='example-pkg-ceccopierangiolieugenio',
    version=version,
    # version="0.1.0a2",
    author='Eugenio Parodi',
    author_email='ceccopierangiolieugenio@googlemail.com',
    # packages=['TermTk'],
    description='Python Terminal Toolkit',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ceccopierangiolieugenio/pyTermTk",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Terminals",
        "Topic :: Software Development :: User Interfaces"],
    # packages=setuptools.find_packages(),
    packages = setuptools.find_packages(),
        #where = '.',
        #include = ['TermTk',]),
    python_requires=">=3.6",
)