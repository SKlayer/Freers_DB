from peewee import *
import config

import os
from urllib.parse import urlparse, uses_netloc


if config.database == True:
    db = SqliteDatabase("db.sqlite3")
else:
    uses_netloc.append(config.database)
    url = urlparse(config.database_url)
    db = PostgresqlDatabase(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port,
    )



class Freer(Model):
    freer_address = CharField(max_length=34, unique=True, )
    freer_user_name = CharField(max_length=32)
    freer_tags = CharField(max_length=220)
    freer_suffix = CharField(max_length=33)
    freer_pubkey = CharField(max_length=66)
    freer_quit = IntegerField()
    freer_CID = CharField(max_length=67)

    freer_adviser = CharField(max_length=32)

    freer_regist_block = CharField()
    freer_lastest_block = CharField()

    class Meta:
        database = db

class Tag(Model):
    tag_name = CharField(max_length=34, unique=True, )
    tag_addr = Field

    class Meta:
        database = db




