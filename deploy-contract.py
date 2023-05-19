
import json
import random
import asyncio
import requests

#from time import sleep

from starknet_py.net.models.chains import StarknetChainId
from starknet_py.net.gateway_client import GatewayClient
# from starknet_py.net import KeyPair

from starknet_py.net.signer.stark_curve_signer import KeyPair

# from starknet_py.proxy.contract_abi_resolver import ProxyConfig
# from starknet_py.proxy.proxy_check import ProxyCheck

from starknet_py.net.client import Client
# from starknet_py.net.client import Account
from starknet_py.net.account.account import Account
# from starknet_py.net.models import Address
# from starknet_py.net.client_models import Call

from starknet_py.contract import Contract


from starknet_py.constants import DEFAULT_DEPLOYER_ADDRESS, FIELD_PRIME

# from starknet_py.tests.e2e.fixtures.constants import MAX_FEE

SRC_FOLDER = "src/"
import random
import string

def starknet_get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def starknet_create_code():

    random_num = random.randint(10000,99000)

    random_func_name = starknet_get_random_string(random.randint(4,10))

    code = (
        f"%lang starknet\n"
        f"\n"
        f"@view\n"
        f"func {random_func_name}() -> (value: felt) {{\n"
        f"  return (value={random_num});\n"
        f"}}\n"
        )

    file_name = f"text_{random_num}.cairo"

    with open(SRC_FOLDER+file_name, "w") as f:
        f.writelines(code)

    return file_name


# # To declare through Contract class you have to compile a contract and pass it to the Contract.declare
# declare_result = await Contract.declare(
#     account=account, compiled_contract=compiled_contract, max_fee=int(1e16)
# )
# # Wait for the transaction
# await declare_result.wait_for_acceptance()

# # After contract is declared it can be deployed
# deploy_result = await declare_result.deploy(max_fee=int(1e16))
# await deploy_result.wait_for_acceptance()

# # You can pass more arguments to the `deploy` method. Check `API` section to learn more

# # To interact with just deployed contract get its instance from the deploy_result
# contract = deploy_result.deployed_contract

# # Now, any of the contract functions can be called

# starknet_create_code()



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

async def deploy_account():

    #  class starknet_py.net.client.Client

    # abstract async deploy_account(transaction: DeployAccount) → DeployAccountTransactionResponse

    # Deploy a pre-funded account contract to the network

    # Parameters:

    #     transaction – DeployAccount transaction

    # берем новый набор сид, приватник, адрес контракта
    # эту штуку можно поднять локально, тогда надо поменять на localhost:3000
    # https://github.com/hodlmod/starknet-tools

    key_req = requests.get('https://starknet-tools.vercel.app/new-keys')

    new_key_from_api = key_req.json()

    # это тестовый, для удобства

    new_key_from_api = {'seed phrase': 'section uncover spawn crush scissors swing stick tooth dynamic guide heavy protect', 'starkKeyPublic': '0x03b7ac9fbacf53a5a81412526bed51dfc9e2203637deb46d893f5fda38d3c434', 'contractAddress': '0x318726948f47eed756762d8c8a8ca7bb0d346d87bf6d068e9fd43de03eb1450', 'starkKeyPrivate': '2320948549485454276660840915673692268195936808424252306996566055748919968437'}


    # логируем, 
    print(new_key_from_api)

    mainnet = "mainnet"
    chain_id = StarknetChainId.MAINNET

    mainnet_client = GatewayClient("mainnet")

    key=int(new_key_from_api["starkKeyPrivate"])

    key_pair = KeyPair.from_private_key(key=key)

    # создаём аккаунт

    account = Account(
        address=key_pair.public_key,
        client=mainnet_client,
        key_pair=key_pair,
        chain=chain_id,
    )

    MAX_FEE = int(1e16)

    # :param class_hash: Class hash of account to be deployed
    # это, вроде, для контрактов-аккаунтов

    class_hash = 0x025ec026985a3bf9d0cc1fe17326b245dfdc3ff89b8fde106542a3ea56c5a918 # https://starkscan.co/class/0x025ec026985a3bf9d0cc1fe17326b245dfdc3ff89b8fde106542a3ea56c5a918

    # соль

    salt = random.Random().randrange(0, FIELD_PRIME)

    # подписываем транзакцию

    deploy_account_tx = await account.sign_deploy_account_transaction(
        class_hash=class_hash,
        contract_address_salt=salt,
        constructor_calldata=[key_pair.public_key],
        max_fee=MAX_FEE,
    )

    # деплоим аккаунт

    deploy_account_result = await account.client.deploy_account(deploy_account_tx)

    print(deploy_account_result.transaction_hash)

    print("https://starkscan.co/tx/" + str(hex(deploy_account_result.transaction_hash)))

    await account.client.wait_for_tx(deploy_account_result.transaction_hash)





if __name__ == '__main__':

    # asyncio.run(deploy_contract())

    asyncio.run(deploy_account())



