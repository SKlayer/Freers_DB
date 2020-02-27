import binascii
import config
import decimal

def start_with(string, start):
    if len(start) > len(string):
        return False
    if start.lower() == string[0:len(start)].lower():
        return True
    return False

def resolve_feip(opreturn):
    if opreturn.count("|") != 4:
        return None
    opreturn = opreturn.split("|")
    username = opreturn[3]
    tags = opreturn[4]
    return [username, tags]




def get_tx_addr_value_by_id(rpc_connection, tx, num):
    tx = rpc_connection.decoderawtransaction(rpc_connection.getrawtransaction(tx))

    val = tx["vout"][num]["value"]
    addr = tx["vout"][num]["scriptPubKey"]["addresses"][0]
    return addr, val

def resove_trans(tx, rpc):
    #tx = {'txid': 'a050417770bdb4bceda2baa4cb0bbb7900ad35e9c6958784fabf57ec608ffea3', 'hash': 'a050417770bdb4bceda2baa4cb0bbb7900ad35e9c6958784fabf57ec608ffea3', 'version': 2, 'size': 297, 'locktime': 0, 'vin': [{'txid': '1bef3cf334d52faac212699c05480a37ad3321a1bbceed5b6b6c6ad3b70522d1', 'vout': 0, 'scriptSig': {'asm': 'e35951ed6a58625474dcc58f14b5c00cf60d24c28ed4ecc68a33e1e6d255a7af138850772b46c13390ef02af402eb64dc1cb82155c2b8d229eca3996ea61f405[ALL|FORKID] 03f1af10342bfac3b06f2088e1340941d70e27aa8adecdfe24f6f1ba1e334c6eaa', 'hex': '41e35951ed6a58625474dcc58f14b5c00cf60d24c28ed4ecc68a33e1e6d255a7af138850772b46c13390ef02af402eb64dc1cb82155c2b8d229eca3996ea61f405412103f1af10342bfac3b06f2088e1340941d70e27aa8adecdfe24f6f1ba1e334c6eaa'}, 'sequence': 4294967295}], 'vout': [{'value': 0.01000000, 'n': 0, 'scriptPubKey': {'asm': 'OP_DUP OP_HASH160 4b8f75e517c7d9a0f9c8746b7d524e934ff31ed4 OP_EQUALVERIFY OP_CHECKSIG', 'hex': '76a9144b8f75e517c7d9a0f9c8746b7d524e934ff31ed488ac', 'reqSigs': 1, 'type': 'pubkeyhash', 'addresses': ['FCidzzzzzzzzzzzzzzzzzzzzzzzzwZWbWK']}}, {'value': 0, 'n': 1, 'scriptPubKey': {'asm': 'OP_RETURN 464549507c337c317c6379746573747c23667265656361736823e887aae794b1e78eb0e9879123e8baabe4bbbde799bbe8aeb02363727970746f206964656e74697479', 'hex': '6a43464549507c337c317c6379746573747c23667265656361736823e887aae794b1e78eb0e9879123e8baabe4bbbde799bbe8aeb02363727970746f206964656e74697479', 'type': 'nulldata'}}, {'value': 0.01000000, 'n': 2, 'scriptPubKey': {'asm': 'OP_DUP OP_HASH160 bff35cb6b032194a8cb6fb85578054a0378db03d OP_EQUALVERIFY OP_CHECKSIG', 'hex': '76a914bff35cb6b032194a8cb6fb85578054a0378db03d88ac', 'reqSigs': 1, 'type': 'pubkeyhash', 'addresses': ['FPL44YJRwPdd2ipziFvqq6y2tw4VnVvpAv']}}]}

    for i in tx["vout"]:
        if i["scriptPubKey"]["type"] == "nulldata":
            script_hex = i["scriptPubKey"]["hex"]
            if start_with(script_hex,"6a"):
                # OP_RETURN
                pubkey = tx["vin"][0]["scriptSig"]["asm"].split("[ALL|FORKID] ")[-1]

                op_return_msg = binascii.a2b_hex(script_hex[2:]).decode("UTF-8")
                op_return_msg = resolve_feip(op_return_msg)
                if op_return_msg is None:
                    return None
                vin_total = 0
                for j in range(-1,len(tx["vin"])):
                    if j == 0:
                        input_txid = tx["vin"][0]["txid"]
                        input_vout = tx["vin"][0]["vout"]

                        address, inval = get_tx_addr_value_by_id(rpc, input_txid, input_vout)
                        vin_total = inval
                    else:
                        adr, val = get_tx_addr_value_by_id(rpc, tx["vin"][j]["txid"], tx["vin"][j]["vout"])
                        vin_total += val
                vout_total = decimal.Decimal("0")
                for j in tx["vout"]:
                    vout_total += decimal.Decimal(str(j["value"]))

                mining_fee = vin_total-vout_total
                if mining_fee < config.min_fee:
                    return None

                return [address,op_return_msg[0],op_return_msg[1],pubkey]

    return None

def transaction_caller(tx, rpc):
    try:
        pubkey = tx["vin"][0]["scriptSig"]["asm"].split("[ALL|FORKID] ")[-1]
    except:
        pubkey = None
    op_return_msg = None
    for i in tx["vout"]:
        if i["scriptPubKey"]["type"] == "nulldata":
            script_hex = i["scriptPubKey"]["hex"]
            if start_with(script_hex,"6a"):
                # OP_RETURN
                op_return_msg = binascii.a2b_hex(script_hex[2:]).decode("UTF-8")

    return rpc,tx,op_return_msg,pubkey






