import pytest
from ape import networks
from ape.utils import ZERO_ADDRESS

from ape_llamarpc.provider import LlamaRPC


@pytest.mark.parametrize(
    "ecosystem,network",
    [
        # ("arbitrum", "mainnet"),
        ("bsc", "mainnet"),
        ("ethereum", "goerli"),
        ("ethereum", "mainnet"),
        # ("optimism", "mainnet"),
        ("polygon", "mainnet"),
    ],
)
def test_llamarpc(ecosystem, network):
    ecosystem_cls = networks.get_ecosystem(ecosystem)
    network_cls = ecosystem_cls.get_network(network)
    with network_cls.use_provider("llamarpc") as provider:
        assert isinstance(provider, LlamaRPC)
        assert provider.get_balance(ZERO_ADDRESS) > 0
        assert provider.get_block(0)
