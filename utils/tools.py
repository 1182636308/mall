from datetime import datetime
import random


def gen_trans_id():
    #  生成交易的流水ID
    now = datetime.now()
    date_str = now.strftime('%Y%m%d%H%M%S%f')
    return date_str + str(random.randint(10000, 99999))
