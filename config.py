import decimal
import json

config = {}

def save_config():
    with open("config.json", mode='w', encoding='utf-8') as fp:
        json.dump(config, fp, ensure_ascii=False, indent=2)


def load_config():
    global config
    with open("config.json", mode='r', encoding='utf-8') as fp:
        config = json.load(fp)


load_config()

database = True if config["database"] == "" else config["database"]
database_url = "database://adin@bot:127.0.0.1:7180"
min_fee = decimal.Decimal(str(config["min_fee"]))


BLOCK_HASH_CACHES = 40

