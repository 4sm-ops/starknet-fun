# from starknet_py.contract import Contract


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

starknet_create_code()