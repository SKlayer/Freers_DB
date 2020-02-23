from .models import db, Freer

def get_freer_by_address(address):
    result = Freer.get_or_none(Freer.freer_address == address)
    if result is None:
        return None
    freer = Freer.get_by_id(result)

    freer = {
        "address": freer.freer_address,
        "name": freer.freer_user_name,
        "tags": freer.freer_tags,
        "suffix": freer.freer_suffix,
        "fullname": f"{freer.freer_user_name}_{freer.freer_suffix}",
        "public_key": freer.freer_pubkey,
        "registe_block": freer.freer_regist_block,
        "latest_block": freer.freer_lastest_block
    }
    return freer

def get_freer_by_pubkey(pubkey):
    result = Freer.get_or_none(Freer.freer_pubkey == pubkey)
    if result is None:
        return None
    freer = Freer.get_by_id(result)

    freer = {
        "address": freer.freer_address,
        "name": freer.freer_user_name,
        "tags": freer.freer_tags,
        "suffix": freer.freer_suffix,
        "fullname": f"{freer.freer_user_name}_{freer.freer_suffix}",
        "public_key": freer.freer_pubkey,
        "registe_block": freer.freer_regist_block,
        "latest_block": freer.freer_lastest_block
    }
    return freer



def get_all_freers(start,end):
    ids = Freer.select().count()
    end = ids if end < 0 else end if end < ids else ids
    start = 1 if start <= 0 else start if start < end else end
    datas = {}
    for i in range(start, end+1):
        freer = Freer.get_by_id(i)
        address = freer.freer_address
        suffix = freer.freer_suffix
        name = freer.freer_user_name
        tags = freer.freer_tags
        pubkey = freer.freer_pubkey
        regist_block = freer.freer_regist_block
        lastest_block = freer.freer_lastest_block
        freer = {
            "address": address,
            "name": name,
            "tags": tags,
            "suffix": suffix,
            "fullname": f"{name}_{suffix}",
            "public_key": pubkey,
            "registe_block": regist_block,
            "latest_block": lastest_block
        }
        datas[i] = freer
    return datas












