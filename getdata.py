import time
import os
import sys
import random
import numpy as np
import arguments


args = arguments.parser()
print("> Setting:", args)


LIB_PATH = "./pyslopes/src/apis"
sys.path.insert(1, LIB_PATH)


from platform_pchain import api as platform
from keystore import api as keystore
from avm import api as avm
from admin import api as admin


API_NODE_IP = "http://" + args.ip + ":" + args.port

station_addrs = ["X-A9e3iJbYC4tRdhGV56QPjHNuWyE7Ao7jG",
                 "X-FC1R55muJFHuTHtMGbvENkNGLCqks1fVZ",
                 "X-8qozToj6mrGWuGMqD2gy9xySvj68nsBnZ",
                 "X-3gemEc753hjpWDe4TWFg65xx8xc6MzwvE",
                 "X-AkpWeXduP5Xkio1ouu1bytH6ksMiNue7D",
                 "X-BBZpBYNqdWiFmv3PB1fZSBawCDKByhisv",
                 "X-KvojiLf6QvQPsikFY3WEKbKFED7eA6MAQ",
                 "X-HRbnGVZEzN774JeSkbRzLQtYRz7wkkUNQ",
                 "X-9TH3dun9M71g1ymXX4pCJJxpkvMemrMGS",
                 "X-gRUq2JVEyTmUbxg7zkBzLwqfoshVao5r",
                 "X-LZCgKuqqRB9s5zHH1nbJc4TCiKcMm9ZKk",
                 "X-N5APzZUVyitRdQGtLm6cUhfW9K6vRb2KZ",
                 "X-Ji7DGdcjX9muM1W6hrbexQe4AKDzGU9ua",
                 "X-AQfdthXkvhA4ohL6rBGSEcwVXyc61YAHS",
                 "X-81TkjECnMzh8GXNs9WgDT7nG8rcswVtav",
                 "X-MrdJVdqgE8N7ta3taan9hmv8wDjBGmGGY",
                 "X-P3Km8LoMKGYZEA2Y789SofjL7oJtp4XVU",
                 "X-8C9cbgFGckdZnwfA9kufYanrfao6svKfY",
                 "X-8TwxXH8SUM6xQjqQVx9dQFnoMcNHxZufQ",
                 "X-4ZcBs4D9fEw5kSBmpSn1toWfec1RHPYva"]

usernames = list(["genesis", "host", "user1"])

balances = []
for idx, addr in enumerate(station_addrs):
    # print(usernames[1], "balance:", avm.getAllBalances(API_NODE_IP, addr))
    balances.append((idx, addr, int(avm.getAllBalances(API_NODE_IP, addr)[0]['balance'])))

balances = np.array(balances)
print(balances)
