from mnemonic import Mnemonic
from eth_account import Account

# from ethers import utils
import eth_utils
from hdwallet import HDWallet
from hdwallet.symbols import DOGE as SYMBOL

def generate_ethereum_wallet_from_seed(seed_phrase):
    Account.enable_unaudited_hdwallet_features()
    account = Account.from_mnemonic(seed_phrase)
#    private_key = account._private_key.hex()
    private_key = account._private_key
    address = account.address
    return address, private_key


# const getStarkPair = (index, privateKey) => {
  # const masterNode = ethers.utils.HDNode.fromSeed(
  #   BigNumber.from(privateKey).toHexString()
  # );
#   const path = `${baseDerivationPath}/${index}`;
#   const childNode = masterNode.derivePath(path);
#   const groundKey =
#     "0x" +
#     starkutils.keyDerivation.grindKey(childNode.privateKey, starknet.ec.ec.n);
#   const starkPair = starknet.ec.getKeyPair(groundKey);
#   return starkPair;
# };


# def get_stark_pair(0, private_key):

mnemo = Mnemonic("english")

print(mnemo)

seed_phrase = mnemo.generate(strength=128)

print(seed_phrase)

seed = mnemo.to_seed(seed_phrase, passphrase="")

print(seed)

entropy = mnemo.to_entropy(seed_phrase)


address, private_key = generate_ethereum_wallet_from_seed(seed_phrase)

seed = str(eth_utils.big_endian_to_int(private_key))

print(seed)

hdwallet: HDWallet = HDWallet(symbol=SYMBOL)
wallet = hdwallet.from_seed(seed=seed)

# master_node = wallet._node

# # print()