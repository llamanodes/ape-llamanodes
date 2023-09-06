# Quick Start

Use the [LlamaNodes](https://llamanodes.com/) provider plugin to interact with blockchains via APIs.
This plugin supports the following ecosystems:

- Ethereum (mainnet and goerli)
- Polygon
- BNB Smart Chain
- Arbitrum (currently in alpha testing)
- Optimism (currently in alpha testing)

## Dependencies

- [python3](https://www.python.org/downloads) version 3.8 up to 3.11.

## Installation

### via `pip`

You can install the latest release via [`pip`](https://pypi.org/project/pip/):

```bash
pip install ape-llamanodes
```

### via `setuptools`

You can clone the repository and use [`setuptools`](https://github.com/pypa/setuptools) for the most up-to-date version:

```bash
git clone https://github.com/ApeWorX/ape-llamanodes.git
cd ape-llamanodes
python3 setup.py install
```

## Quick Usage

First, make sure you have one of the following environment variables set (it doesn't matter which one):

- WEB3_LLAMANODES_API_KEY
- WEB3_LLAMANODES_PROJECT_ID
- WEB3_LLAMARPC_API_KEY
- WEB3_LLAMARPC_PROJECT_ID

Either in your current terminal session or in your root RC file (e.g. `.bashrc`), add the following:

```bash
export WEB3_LLAMANODES_API_KEY=MY_API_TOKEN
```

The provider will work without the environment variables, but it uses the free tier which has stricter limits.

To use the LlamaNodes provider plugin in most commands, set it via the `--network` option:

```bash
ape console --network ethereum:mainnet:llamanodes
```

To connect to LlamaNodes from a Python script, use the `networks` top-level manager:

```python
from ape import networks

with networks.parse_network_choice("ethereum:mainnet:llamanodes") as provider:
    ...
```
