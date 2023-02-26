import os
from codecs import open
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))

os.chdir(here)

with open(
    os.path.join(here, "LONG_DESCRIPTION.rst"), "r", encoding="utf-8"
) as fp:
    long_description = fp.read()

version_contents = {}
with open(
    os.path.join(here, "src", "reportyy", "version.py"), encoding="utf-8"
) as f:
    exec(f.read(), version_contents)

setup(
    name="reportyy",
    version=version_contents["VERSION"],
    description="Python client for the Reportyy API",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author="Reportyy",
    author_email="engineering@reportyy.com",
    readme="README.md",
    url="https://github.com/Reportyy/reportyy-client-python",
    license="Apache License, Version 2.0",
    keywords="reportyy api",
    packages=find_packages(exclude=["tests", "tests.*"]),
    zip_safe=False,
    install_requires=[
        'requests >= 2.20; python_version >= "3.0"',
        'requests[security] >= 2.20; python_version < "3.0"',
    ],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*",
    project_urls={
        "Bug Tracker": "https://github.com/Reportyy/reportyy-client-python/issues",
        "Documentation": "https://docs.reportyy.com",
        "Source Code": "https://github.com/Reportyy/reportyy-client-python",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    setup_requires=["wheel"],
)
