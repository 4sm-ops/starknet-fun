from starknet_py.contract import Contract


# To declare through Contract class you have to compile a contract and pass it to the Contract.declare
declare_result = await Contract.declare(
    account=account, compiled_contract=compiled_contract, max_fee=int(1e16)
)
# Wait for the transaction
await declare_result.wait_for_acceptance()

# After contract is declared it can be deployed
deploy_result = await declare_result.deploy(max_fee=int(1e16))
await deploy_result.wait_for_acceptance()

# You can pass more arguments to the `deploy` method. Check `API` section to learn more

# To interact with just deployed contract get its instance from the deploy_result
contract = deploy_result.deployed_contract

# Now, any of the contract functions can be called