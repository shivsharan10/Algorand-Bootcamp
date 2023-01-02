import json
import base64
from algosdk import account, mnemonic, constants
from algosdk.v2client import algod
from algosdk.future import transaction
from algosdk.future.transaction import AssetConfigTxn, wait_for_confirmation
from algosdk.mnemonic import to_private_key


def generate_algorand_keypair():
    private_key, address = account.generate_account()
    print("My address: {}".format(address))
    print("My private key: {}".format(private_key))
    print("My passphrase: {}".format(mnemonic.from_private_key(private_key)))


generate_algorand_keypair()
# Write down the address, private key, and the passphrase for later usage
# generate_algorand_keypair()

algod_address = "https://testnet-api.algonode.cloud"
algod_client = algod.AlgodClient("", algod_address)

asset_creator_address = "PYIBR3IFQD5PHMIYMU5H2K56CJRBL2DZISMQRGQYQJ666GTR5PFUOCZXNA"
passphrase = ""
private_key = to_private_key(passphrase)

# create the asset LATINUM

txn = AssetConfigTxn(
    sender=asset_creator_address,
    sp=algod_client.suggested_params(),
    total=1000,
    default_frozen=False,
    unit_name="LATINUM",
    asset_name="latinum",
    manager=asset_creator_address,
    reserve=asset_creator_address,
    freeze=asset_creator_address,
    clawback=asset_creator_address,
    url="https://path/to/my/asset/details",
    decimals=0)
# Sign with secret key of creator
stxn = txn.sign(private_key)
# Send the transaction to the network and retrieve the txid.
try:
    txid = algod_client.send_transaction(stxn)
    print("Signed transaction with txID: {}".format(txid))
    # Wait for the transaction to be confirmed
    confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(
        confirmed_txn['confirmed-round']))
except Exception as err:
    print(err)
# Retrieve the asset ID of the newly created asset by first
# ensuring that the creation transaction was confirmed,
# then grabbing the asset id from the transaction.
print("Transaction information: {}".format(
    json.dumps(confirmed_txn, indent=4)))
# print("Decoded note: {}".format(base64.b64decode(
#     confirmed_txn["txn"]["txn"]["note"]).decode()))


def first_transaction_example(my_mnemonic, my_address):
    algod_address = "https://testnet-api.algonode.cloud"
    algod_client = algod.AlgodClient("", algod_address)

    print("My address: {}".format(my_address))
    private_key = mnemonic.to_private_key(my_mnemonic)
    print(private_key)
    account_info = algod_client.account_info(my_address)
    print("Account balance: {} microAlgos".format(account_info.get('amount')))

    # build transaction
    params = algod_client.suggested_params()
    # comment out the next two (2) lines to use suggested fees
    params.flat_fee = constants.MIN_TXN_FEE
    params.fee = 1000
    receiver = "OAYXRIBEDXGVWNVEFCZQKTQ5JGRVXNV7HWN6HXCBOHIR6BZ6YECDKQMR64"
    amount = 100000
    note = "Hello Friend! Initiated this txn by Shivsharan".encode()

    unsigned_txn = transaction.PaymentTxn(
        my_address, params, receiver, amount, None, note)

    # sign transaction
    signed_txn = unsigned_txn.sign(private_key)

    # submit transaction
    txid = algod_client.send_transaction(signed_txn)
    print("Signed transaction with txID: {}".format(txid))

    # wait for confirmation
    try:
        confirmed_txn = transaction.wait_for_confirmation(
            algod_client, txid, 4)
    except Exception as err:
        print(err)
        return

    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
    print("Decoded note: {}".format(base64.b64decode(
        confirmed_txn["txn"]["txn"]["note"]).decode()))

    print("Starting Account balance: {} microAlgos".format(
        account_info.get('amount')))
    print("Amount transfered: {} microAlgos".format(amount))
    print("Fee: {} microAlgos".format(params.fee))

    account_info = algod_client.account_info(my_address)
    print("Final Account balance: {} microAlgos".format(
        account_info.get('amount')) + "\n")


private_key = ""
my_mnemonic = ""
my_address = "PYIBR3IFQD5PHMIYMU5H2K56CJRBL2DZISMQRGQYQJ666GTR5PFUOCZXNA"
first_transaction_example(my_mnemonic, my_address)



