import os
from typing import Dict, Tuple

from ape.api import UpstreamProvider, Web3Provider
from ape.exceptions import ContractLogicError, ProviderError, VirtualMachineError
from ape.logging import logger
from web3 import HTTPProvider, Web3
from web3.exceptions import ContractLogicError as Web3ContractLogicError
from web3.gas_strategies.rpc import rpc_gas_price_strategy
from web3.middleware import geth_poa_middleware

_ENVIRONMENT_VARIABLE_NAMES = ("WEB3_LAMMARPC_PROJECT_ID", "WEB3_LAMMARPC_API_KEY")


def standard_llamarpc_subdomain(ecosystem_name, network_name):
    if network_name == "mainnet":
        return ecosystem_name

    return f"{ecosystem_name}-{network_name}"


class LlamaProviderError(ProviderError):
    """
    An error raised by the LlamaRPC provider plugin.
    """


class LlamaRPC(Web3Provider, UpstreamProvider):
    network_uris: Dict[Tuple[str, str], str] = {}

    subdomains = {
        ("arbitrum", "mainnet"): "arbitrum",
        ("bsc", "mainnet"): "binance",
        ("ethereum", "mainnet"): "ethereum",
        ("ethereum", "goerli"): "ethereum-goerli",
        ("optimism", "mainnet"): "optimism",
        ("polygon", "mainnet"): "polygon",
    }

    @property
    def uri(self) -> str:
        ecosystem_name = self.network.ecosystem.name
        network_name = self.network.name
        if (ecosystem_name, network_name) in self.network_uris:
            return self.network_uris[(ecosystem_name, network_name)]

        key = None
        for env_var_name in _ENVIRONMENT_VARIABLE_NAMES:
            env_var = os.environ.get(env_var_name)
            if env_var:
                key = env_var
                # TODO: verify that env_var is a UUID or ULID
                break

        subdomain = self.subdomains.get((ecosystem_name, network_name))
        if not subdomain:
            subdomain = standard_llamarpc_subdomain(ecosystem_name, network_name)
            logger.warning(
                "Unsupported ecosystem: %s. Trying subdomain: %s", ecosystem_name, subdomain
            )

        network_uri = f"https://{subdomain}.llamarpc.com"

        if key:
            network_uri += f"/rpc/{key}"

        self.network_uris[(ecosystem_name, network_name)] = network_uri
        return network_uri

    @property
    def connection_str(self) -> str:
        return self.uri

    def connect(self):
        self._web3 = Web3(HTTPProvider(self.uri))

        # Any chain that *began* as PoA needs the middleware for pre-merge blocks
        ethereum_goerli = 5
        optimism = (10, 420)
        polygon = (137, 80001)
        bsc = (56, 97)

        if self._web3.eth.chain_id in (ethereum_goerli, *optimism, *polygon, *bsc):
            self._web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        self._web3.eth.set_gas_price_strategy(rpc_gas_price_strategy)

    def disconnect(self):
        self._web3 = None

    def get_virtual_machine_error(self, exception: Exception, **kwargs) -> VirtualMachineError:
        txn = kwargs.get("txn")
        if not hasattr(exception, "args") or not len(exception.args):
            return VirtualMachineError(base_err=exception, txn=txn)

        args = exception.args
        message = args[0]
        if (
            not isinstance(exception, Web3ContractLogicError)
            and isinstance(message, dict)
            and "message" in message
        ):
            # Is some other VM error, like gas related
            return VirtualMachineError(message["message"], txn=txn)

        elif not isinstance(message, str):
            return VirtualMachineError(base_err=exception, txn=txn)

        # If get here, we have detected a contract logic related revert.
        message_prefix = "execution reverted"
        if message.startswith(message_prefix):
            message = message.replace(message_prefix, "")

            if ":" in message:
                # Was given a revert message
                message = message.split(":")[-1].strip()
                return ContractLogicError(revert_message=message, txn=txn)
            else:
                # No revert message
                return ContractLogicError(txn=txn)

        return VirtualMachineError(message, txn=txn)
