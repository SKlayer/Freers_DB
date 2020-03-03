from .models import db, Freer

def asm_freer(freer):
    return {
        "address": freer.freer_address,
        "name": freer.freer_user_name,
        "tags": freer.freer_tags,
        "suffix": freer.freer_suffix,
        "fullname": freer.freer_CID,
        "public_key": freer.freer_pubkey,
        "registe_block": freer.freer_regist_block,
        "latest_block": freer.freer_lastest_block,
        "quit": freer.freer_quit,
        "adviser": freer.freer_adviser,

    }



def get_freer_by_address(address):
    result = Freer.get_or_none(Freer.freer_address == address)
    if result is None:
        return None
    freer = Freer.get_by_id(result)
    return asm_freer(freer)

def get_freer_by_adv(cid):
    freers = {}
    for i in Freer.select().where(Freer.freer_adviser == cid):
        freers[int(i.id)] = asm_freer(i)

    return freers




def get_freer_by_CID(cid):
    result = Freer.get_or_none(Freer.freer_CID == cid)
    if result is None:
        return None
    freer = Freer.get_by_id(result)

    return asm_freer(freer)


def get_freer_by_pubkey(pubkey):
    result = Freer.get_or_none(Freer.freer_pubkey == pubkey)
    if result is None:
        return None
    freer = Freer.get_by_id(result)

    return asm_freer(freer)


def get_all_freers(start, end):
    ids = Freer.select().count()
    end = ids if end < 0 else end if end < ids else ids
    start = 1 if start <= 0 else start if start < end else end
    datas = {}
    for i in range(start, end + 1):
        freer = Freer.get_by_id(i)
        datas[i] = asm_freer(freer)
    return datas
