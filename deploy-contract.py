
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

from starknet_py.hash.address import compute_address


from starknet_py.constants import DEFAULT_DEPLOYER_ADDRESS, FIELD_PRIME

# from starknet_py.tests.e2e.fixtures.constants import MAX_FEE

from starknet_py.hash.transaction import (
    TransactionHashPrefix,
    compute_declare_transaction_hash,
    compute_deploy_account_transaction_hash,
    compute_transaction_hash,
)

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


## ДЕПЛОЙ ОБЫЧНОГО-КОНТРАКТА ##

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


## ДЕПЛОЙ АККАУНТА-КОНТРАКТА ##


# async def get_deploy_account_transaction(
#     *,
#     address: int,
#     key_pair: KeyPair,
#     salt: int,
#     class_hash: int,
#     network: Optional[Network] = None,
#     client: Optional[Client] = None,
# ) -> DeployAccount:
#     """
#     Get a signed DeployAccount transaction from provided details
#     """
#     if network is None and client is None:
#         raise ValueError("One of network or client must be provided.")

#     account = Account(
#         address=address,
#         client=client
#         or GatewayClient(
#             net=cast(
#                 Network, network
#             )  # Cast needed because pyright doesn't recognize network as not None at this point
#         ),
#         key_pair=key_pair,
#         chain=StarknetChainId.TESTNET,
#     )
#     return await account.sign_deploy_account_transaction(
#         class_hash=class_hash,
#         contract_address_salt=salt,
#         constructor_calldata=[key_pair.public_key],
#         max_fee=MAX_FEE,
#     )


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


    MAX_FEE = int(1e16)

    # :param class_hash: Class hash of account to be deployed
    # это, вроде, для контрактов-аккаунтов

    class_hash = "0x025ec026985a3bf9d0cc1fe17326b245dfdc3ff89b8fde106542a3ea56c5a918" # https://starkscan.co/class/0x025ec026985a3bf9d0cc1fe17326b245dfdc3ff89b8fde106542a3ea56c5a918

    # соль

    # salt = random.Random().randrange(0, FIELD_PRIME)
    salt = int(new_key_from_api["starkKeyPublic"], 16) # такая соль у Аргента

    contract_address=int(new_key_from_api["contractAddress"], 16)

    # print(contract_address)


    salt = int(new_key_from_api["starkKeyPublic"], 16)

    # salt = random.Random().randrange(0, FIELD_PRIME)
    # salt = 0



    constructor_calldata_js = [
      1449178161945088530446351771646113898511736767359683664273252560520029776866, # fixed value
      215307247182100370520050591091822763712463273430149262739280891880522753123, # fixed value
      2, # fixed value
      salt, # меняется
      0 # fixed value
    ]

    address = compute_address(
        salt=salt,
        class_hash=int(class_hash, 16),
        constructor_calldata=constructor_calldata_js,
        deployer_address=0,
    )

    # print(address)

    # # деплоим аккаунт как у Ивана

    # deploy_result = await Account.deploy_account(
    #     address=contract_address,
    #     key_pair=key_pair,
    #     salt=salt,
    #     class_hash=int(class_hash, 16),
    #     client=mainnet_client,
    #     chain=chain_id,
    #     max_fee=MAX_FEE,
    #     )

    # подписываем транзакцию

    account = Account(
        # address=address,
        address = contract_address,
        client=mainnet_client,
        key_pair=key_pair,
        chain=chain_id,
    )


    deploy_account_tx = await account.sign_deploy_account_transaction(
        class_hash=int(class_hash, 16),
        contract_address_salt=salt,
        constructor_calldata=constructor_calldata_js, 
        max_fee=MAX_FEE, 
    )
# у аргента вот что передаётся https://github.com/argentlabs/argent-x/blob/099b22927759b8fdf3b52c67a72e9072ac1289a0/packages/swap/src/sdk/hash.ts#L19

#     # у аргента   const CONTRACT_ADDRESS_PREFIX = number.toFelt("0x535441524b4e45545f434f4e54524143545f41444452455353",

#     # y python starknet либы : CONTRACT_ADDRESS_PREFIX = 523065374597054866729014270389667305596563390979550329787219


#     # https://github.com/software-mansion/starknet.py/blob/48fafd0b18bf43fbf1f472da5708c1d3cb247e00/starknet_py/hash/address.py 


    deploy_account_result = await account.client.deploy_account(deploy_account_tx)

    print("https://starkscan.co/tx/" + str(hex(deploy_account_result.transaction_hash)))

    await account.client.wait_for_tx(deploy_account_result.transaction_hash)


# # надо сюда compute_deploy_account_transaction_hash 


if __name__ == '__main__':

    # asyncio.run(deploy_contract())

    asyncio.run(deploy_account())



