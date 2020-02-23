from .models import db, Freer


def create_table():
    db.connect(reuse_if_open=True)
    db.create_tables([Freer,])




def update_freer(address,name,tags,pubkey,height):
    db.connect(reuse_if_open=True)
    freer = Freer.get_or_none(Freer.freer_address == address)
    if freer is None:
        freer_suffix = ""
        for i in range(4,34):
            freer_suffix = address[34-i:34]
            try:
                Freer.select().where(Freer.freer_address.endswith(freer_suffix)).get()
            except:
                break

        Freer.create(
            freer_address=address,
            freer_user_name=name,
            freer_tags=tags,
            freer_quit=0,
            freer_suffix = freer_suffix,
            freer_pubkey = pubkey,
            freer_regist_block = str(height),
            freer_lastest_block = str(height)
        )

    else:
        Freer.update(
            freer_user_name=name,
            freer_tags=tags,
            freer_lastest_block=str(height),
            freer_quit=0).where(Freer.freer_address == address).execute()


def set_quit_freer(address):
    db.connect(reuse_if_open=True)
    exists = Freer.get_or_none(Freer.freer_address == address)
    if not exists is None:
        Freer.update(freer_quit=1).where(Freer.freer_address == address).execute()

    return True


