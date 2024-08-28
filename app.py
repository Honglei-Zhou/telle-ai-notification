import logging
from server.redis_instance import r
from utils.worker import ThreadPool
from server.config import thread_number
from utils import handler
import time

import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)


if __name__ == '__main__':

    pool = ThreadPool(thread_number)

    while True:
        try:
            packed = r.blpop(['telle:queue:notification'], 30)

            if not packed:
                continue

            message = json.loads(packed[1])

            logger.info(message)

            func_name = message['type']
            if func_name in handler:
                pool.map(handler[func_name], [message])

            time.sleep(0.1)
        except Exception as e:
            # print(e)
            logger.info(e)
            # break
            continue




