from ape import plugins

from .provider import LlamaRPC

NETWORKS = {
    "ethereum": [
        "mainnet",
    ],
    "bsc": [
        "mainnet",
    ],
    "polygon": [
        "mainnet",
    ],
}


@plugins.register(plugins.ProviderPlugin)
def providers():
    for ecosystem_name in NETWORKS:
        for network_name in NETWORKS[ecosystem_name]:
            yield ecosystem_name, network_name, LlamaRPC
