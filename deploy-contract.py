import json
import random
import asyncio

#from time import sleep

from starknet_py.net.models.chains import StarknetChainId
from starknet_py.net.gateway_client import GatewayClient
from starknet_py.net import AccountClient, KeyPair

# from starknet_py.proxy.contract_abi_resolver import ProxyConfig
# from starknet_py.proxy.proxy_check import ProxyCheck

# from starknet_py.net.client import Client
# from starknet_py.net.models import Address
# from starknet_py.net.client_models import Call

from starknet_py.contract import Contract

# from starkware.starknet.public.abi import (
#     get_selector_from_name,
#     get_storage_var_address,
# )

# import libstarknet


async def deploy_contract():


    #### choose account ####

    f = open("../../.starknet_accounts/starknet_mainnet_accounts.json")

    accounts_json = json.load(f)["mainnet"]


    random_key = random.choice(list(accounts_json.keys()))

    # while not accounts_json[random_key]["deployed"]:
    #     random_key = random.choice(list(accounts_json.keys()))

    # print(random_key)

    print("Wallet: " + accounts_json[random_key]["address"])

    # #### setup account ####

    mainnet = "mainnet"
    chain_id = StarknetChainId.MAINNET

    mainnet_client = GatewayClient("mainnet")

    key_pair = KeyPair.from_private_key(key=int(accounts_json[random_key]["private_key"], 16))

    account_client_mainnet = AccountClient(
        client=mainnet_client,
        address=int(accounts_json[random_key]["address"], 16),
        key_pair=key_pair,
        chain=chain_id,
        supported_tx_version=1,
    )

    # open previously compiled contract

    f = open("test-contract/compiled/Simple.json")

    compiled_contract = json.dumps(json.load(f))

    # declare

    print("Declaring contract ... ")

    # To declare through Contract class you have to compile a contract and pass it to the Contract.declare
    declare_result = await Contract.declare(
        account=account_client_mainnet, compiled_contract=compiled_contract, max_fee=int(1e16)
    )
    # Wait for the transaction
    await declare_result.wait_for_acceptance()

    print("Deploying contract ... ")

    # After contract is declared it can be deployed
    deploy_result = await declare_result.deploy(max_fee=int(1e16))
    await deploy_result.wait_for_acceptance()

    print("https://starkscan.co/tx/" + str(hex(deploy_result.hash)))


## MAIN ##

if __name__ == '__main__':

    asyncio.run(deploy_contract())
