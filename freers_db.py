from db import get, set
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import config
import decode
import time
import threading
from platform import system as os_type
import logging
import tornado.ioloop
import tornado.web
import tornado.options
from tornado import gen
import json
from concurrent.futures import ThreadPoolExecutor


set.create_table()

if os_type() == "Windows":
    import asyncio

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


rpc_connection = AuthServiceProxy(config.config["rpc_server_uri"])
logging.basicConfig(level=logging.INFO)

last_blocks = []

current_work_block = ["Not Sync Done",-1,-1]

server_elapsed_time = time.time()

def insert_blk(blk_hash):
    if len(last_blocks) > config.BLOCK_HASH_CACHES:
        last_blocks.pop(0)
    last_blocks.append(blk_hash)

def revert_blk():
    if len(last_blocks) <= 1:
        return config.config["genesis_block"]
    last_blocks.pop(-1)
    last_blk = last_blocks[-1]

    return last_blk




def block_updater():
    logger = logging.getLogger('Block Updater')
    logger.setLevel(logging.INFO)
    if config.config["current_block"] == config.config["genesis_block"]:
        next_block_hash = config.config["genesis_block"]
    else:
        next_block_hash = config.config["current_block"]
    end_time = 0
    while 1:

        while 1:
            insert_blk(next_block_hash)

            block = rpc_connection.getblock(next_block_hash)

            if block["confirmations"] == -1:
                logger.warning(f"Detect Block Reverted!! Block hash {next_block_hash} invalid.")
                next_block_hash = revert_blk()
                logger.warning(f"Detect Block Reverted!! Revert block to {next_block_hash}.")
            if "nextblockhash" not in block:
                time.sleep(5)
                logger.debug("waiting new block arrive!")
            else:
                next_block_hash = block["nextblockhash"]
                config.config["current_block"] = next_block_hash
                config.save_config()
                global current_work_block
                current_work_block = [next_block_hash, block["height"], time.time()]
                break
        if next_block_hash == config.config["genesis_block"]:
            continue

        txs = block["tx"]
        first_tx = True
        if end_time == 0:
            start_time = 0
        logger.info(
            f"Receive new block {next_block_hash},Height {block['height']}. Cost {round((end_time - start_time) * 1000, 3)}ms")
        start_time = time.time()
        for i in txs:
            if first_tx:
                first_tx = False
                continue
            tx = rpc_connection.decoderawtransaction(rpc_connection.getrawtransaction(i))
            detail = decode.resove_trans(tx, rpc_connection)

            if detail is not None:
                address, name, tags, pubkey = tuple(detail)
                set.update_freer(address, name, tags, pubkey, block["height"])
                logger.info(f"Update new record.  Addr:{address},Username:{name},Tags:{tags},PublicKey:{pubkey}")
        end_time = time.time()


class AllFreers(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(10)
    logger = logging.getLogger('API.GetAllOfFreers')

    def get(self):
        self.write(json.dumps(get.get_all_freers(0,-1)))
        self.finish()

class GetFreers(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(10)
    logger = logging.getLogger('API.GetFreers')

    def get(self):
        addr = self.get_argument("address")
        result = get.get_freer_by_address(addr)
        if result is None:
            result = {"result":False}
        else:
            result["result"] = True



        self.write(result)
        self.finish()

class GetServiceStats(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(10)
    logger = logging.getLogger('API.GetServiceStats')

    def get(self):
        result = {
            "current_height": current_work_block[1],
            "current_hash": current_work_block[0],
            "last_block_update": current_work_block[2],
            "server_elapsed": time.time() - server_elapsed_time,

        }
        self.write(result)
        self.finish()


def run_api_server():
    app = tornado.web.Application([
        (r"/get_all_freer", AllFreers),
        (r"/get_freer_by_address", GetFreers),
        (r"/stats", GetServiceStats),
    ], autoreload=False)
    app.listen(8080, address="127.0.0.1")

    tornado.ioloop.IOLoop.current().start()



if __name__ == "__main__":
    threading.Thread(target=block_updater).start()
    run_api_server()