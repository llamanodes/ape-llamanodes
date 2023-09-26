#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

extras_require = {
    "test": [  # `test` GitHub Action jobs uses this
        "ape-arbitrum",
        "ape-base",
        "ape-bsc",
        "ape-optimism",
        "ape-polygon",
        "hypothesis>=6.2.0,<7.0",  # Strategy-based fuzzer
        "pytest-cov",  # Coverage analyzer plugin
        "pytest-xdist",  # multi-process runner
        "pytest>=6.0",  # Core testing package
    ],
    "lint": [
        "black>=23.3.0,<24",  # auto-formatter and linter
        "flake8>=6.0.0,<7",  # Style linter
        "isort>=5.10.1,<6",  # Import sorting linter
        "mdformat-frontmatter>=0.4.1",  # Needed for frontmatters-style headers in issue templates
        "mdformat-gfm>=0.3.5",  # Needed for formatting GitHub-flavored markdown
        "mdformat>=0.7.16",  # Auto-formatter for markdown
        "mypy>=0.991,<1",  # Static type analyzer
        "types-setuptools",  # Needed due to mypy typeshed
    ],
    "doc": [
        "Sphinx>=3.4.3,<4",  # Documentation generator
        "sphinx_rtd_theme>=0.1.9,<1",  # Readthedocs.org theme
        "towncrier>=19.2.0, <20",  # Generate release notes
    ],
    "release": [  # `release` GitHub Action job uses this
        "setuptools",  # Installation tool
        "setuptools-scm",  # Installation tool
        "twine",  # Package upload tool
        "wheel",  # Packaging tool
    ],
    "dev": [
        "IPython",  # Console for interacting
        "commitizen",  # Manage commits and publishing releases
        "ipdb",  # Debugger (Must use `export PYTHONBREAKPOINT=ipdb.set_trace`)
        "pre-commit",  # Ensure that linters are run prior to commiting
        "pytest-watch",  # `ptw` test watcher/runner
    ],
}

# NOTE: `pip install -e '.[dev]'` to install package
extras_require["dev"] = (
    extras_require["test"]
    + extras_require["lint"]
    + extras_require["doc"]
    + extras_require["release"]
    + extras_require["dev"]
)

with open("./README.md") as readme:
    long_description = readme.read()


setup(
    name="ape-llamanodes",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    description="""ape-llamanodes: LlamaNodes Provider plugins for Ethereum-based networks""",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="LlamaNodes",
    author_email="info@llamanodes.com",
    url="https://github.com/llamanodes/ape-llamanodes",
    include_package_data=True,
    install_requires=[
        "eth-ape>=0.6.5,<0.7",
    ],
    python_requires=">=3.8,<4",
    extras_require=extras_require,
    py_modules=["ape_llamanodes"],
    license="Apache-2.0",
    zip_safe=False,
    keywords="ethereum",
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_data={"ape_llamanodes": ["py.typed"]},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
